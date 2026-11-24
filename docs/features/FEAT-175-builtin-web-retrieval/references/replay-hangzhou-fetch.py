"""Serve the November 23 public response steps on loopback. Paid finalization is opt-in."""
import argparse
from datetime import datetime
import hashlib
import http.server
import json
import os
from pathlib import Path
import re
import threading
import urllib.error
import urllib.request
import uuid
from zoneinfo import ZoneInfo


def recorded_steps(path):
    steps, current, calls = [], [], []
    prompt = opening = commentary = recorded_at = None
    for line in path.read_text().splitlines():
        entry = json.loads(line)
        item = entry["payload"]
        kind = item.get("type")
        if entry["type"] == "event_msg":
            if kind == "task_started":
                started = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                recorded_at = started.astimezone(ZoneInfo("Asia/Shanghai")).isoformat()
            elif kind == "user_message":
                prompt = item["message"]
            elif kind == "agent_message":
                if not opening:
                    opening = item["message"]
                elif not commentary:
                    commentary = item["message"]
            elif kind == "mcp_tool_call_end" and item["invocation"]["tool"] == "kimi_web_fetch":
                calls.append({"arguments": item["invocation"]["arguments"], "call_id": item["call_id"],
                              "body": item["result"]["Ok"]["structuredContent"]})
            elif kind == "token_count" and current:
                steps.append(current)
                current = []
        elif entry["type"] == "response_item":
            public = kind == "message" and item.get("role") == "assistant"
            if public or kind in ("web_search_call", "function_call"):
                current.append(dict(item, status="completed"))
    if len(calls) != 4 or len(steps) != 6 or len({json.dumps(r["body"], sort_keys=True) for r in calls}) != 1:
        raise ValueError("expected the four original equal Hangzhou page results")
    source = {"request": prompt, "recordedAt": recorded_at, "commentary": commentary,
              "open": opening, "fetches": calls}
    return steps, source


def model_visible_page(history, reference):
    calls = [item for item in history if item.get("type") == "function_call_output"
             and item.get("call_id", "").startswith("exec_")]
    if not calls:
        return calls, {}
    output = calls[-1]["output"]
    text = output if isinstance(output, str) else "".join(v.get("text", "") for v in output)
    _, marker, returned = text.partition("Output:")
    try:
        if marker:
            value = json.loads(returned.strip())
        else:
            title, url, markdown = text.split("\n", 2)
            value = {"title": title, "url": url, "markdown": markdown, "truncated": reference["truncated"]}
        if not isinstance(value, dict):
            return calls, {}
    except ValueError:
        return calls, {}
    # The context manager may shorten the meteorological glossary below the
    # forecast. Check the complete requested section separately from the footer.
    stop = "_分时段预报_"
    delivered = value.get("markdown", "")
    forecast, found, _ = delivered.partition(stop)
    matches = bool(found) and forecast == reference["markdown"].partition(stop)[0]
    matches = matches and all(value.get(k) == reference[k] for k in ("title", "url", "truncated"))
    return calls, {"keys": sorted(value), "materialMatchesRecording": value == reference,
                   "forecastMatchesRecording": matches,
                   "weeklyTextSha256": hashlib.sha256(forecast.encode()).hexdigest()}


def offline_answer(page):
    sections = re.findall(r"- ## (2[3-9]日[^\n]*)\n(.*?)(?=\n- ## |分时段预报)", page["markdown"], re.S)
    if len(sections) != 7:
        raise ValueError("unexpected recorded forecast shape")
    lines = [day + " " + " ".join(v.strip("_ ") for v in content.splitlines() if v.strip())
             for day, content in sections]
    answer = "杭州未来七天天气\n\n" + "\n\n".join(lines) + "\n\n来源 " + page["url"]
    return {"id": "msg_fixture_final", "type": "message", "role": "assistant", "phase": "final_answer",
            "status": "completed", "content": [{"type": "output_text", "text": answer, "annotations": []}]}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


def claim_slot(ledger, run):
    for slot in range(1, 9):
        try:
            with (ledger / f"kimi-{slot:02d}.json").open("x") as stream:
                json.dump({"stage": "answer-only", "run": run}, stream)
            return slot
        except FileExistsError:
            continue
    raise ValueError("authorized Kimi requests exhausted")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recording", type=Path, required=True)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--kimi-key-file", type=Path)
    parser.add_argument("--allowance-directory", type=Path)
    args = parser.parse_args()
    out = args.directory.resolve()
    out.mkdir(mode=0o700, parents=True, exist_ok=True)
    if args.kimi_key_file and not args.allowance_directory:
        parser.error("a persistent allowance directory is required for a real final answer")
    if args.allowance_directory:
        args.allowance_directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    steps, source = recorded_steps(args.recording)
    (out / "source.json").write_text(json.dumps(source, ensure_ascii=False))
    attempts = []

    def record(row):
        attempts.append(row)
        (out / "sampling.json").write_text(json.dumps(attempts, ensure_ascii=False, indent=2))

    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def start_stream(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.end_headers()
            self.streaming = True

        def emit(self, kind, **fields):
            packet = json.dumps(dict(type=kind, **fields), ensure_ascii=False)
            self.wfile.write(("data: " + packet + "\n\n").encode())
            self.wfile.flush()

        def send_items(self, items):
            self.start_stream()
            rid = f"resp_replay_{uuid.uuid4().hex}"
            self.emit("response.created", response={"id": rid, "status": "in_progress", "output": []})
            for index, item in enumerate(items):
                initial = dict(item, content=[]) if item["type"] == "message" else item
                self.emit("response.output_item.added", output_index=index, item=initial)
                if item["type"] == "message":
                    text = item["content"][0]["text"]
                    for start in range(0, len(text), 11):
                        self.emit("response.output_text.delta", item_id=item["id"], output_index=index,
                                  content_index=0, delta=text[start:start + 11])
                self.emit("response.output_item.done", output_index=index, item=item)
            self.emit("response.completed", response={"id": rid, "status": "completed", "output": items,
                      "usage": {"input_tokens": 100, "output_tokens": 64, "total_tokens": 164}})

        def forward_final(self, request, slot):
            upstream = urllib.request.Request("https://api.moonshot.cn/v1/responses",
                data=json.dumps(request, ensure_ascii=False).encode(), method="POST",
                headers={"Content-Type": "application/json",
                         "Authorization": "Bearer " + args.kimi_key_file.read_text().strip()})
            with urllib.request.build_opener(NoRedirect()).open(upstream, timeout=115) as response:
                self.start_stream()
                receipt = {"status": response.status, "slot": slot, "publicTexts": []}
                for line in response:
                    self.wfile.write(line)
                    if not line.strip():
                        self.wfile.flush()
                    elif line.startswith(b"data: {"):
                        event = json.loads(line[6:])
                        if event.get("type") == "response.output_item.done":
                            item = event.get("item", {})
                            if item.get("type") == "message" and item.get("role") == "assistant":
                                body = "".join(v.get("text", "") for v in item.get("content", [])
                                               if v.get("type") == "output_text")
                                if body.startswith("[[yijie-public-message-v1:final_answer]]"):
                                    body = body.partition("\n")[2]
                                receipt["publicTexts"].append(hashlib.sha256(body.strip().encode()).hexdigest())
                        elif event.get("type") == "response.completed":
                            result = event["response"]
                            receipt.update(responseId=result.get("id"), model=result.get("model"),
                                           completed=True, usage=result.get("usage"))
                (out / f"kimi-receipt-{slot}.json").write_text(json.dumps(receipt, indent=2))

        def sample(self, request):
            index = len(attempts)
            history = request["input"]
            material, details = model_visible_page(history, source["fetches"][0]["body"])
            corrected = any("The last step only requested" in str(v.get("content", ""))
                            for v in history if v.get("role") == "developer")
            row = {"step": index + 1, "correctionSeen": corrected, "previousFetch": details}
            if request.get("tools"):
                if index >= len(steps):
                    raise ValueError("sampling continued with tools after recorded repeat limit")
                hosted = any(tool.get("type") == "web_search" for tool in request["tools"])
                items = [item for item in steps[index] if hosted or item["type"] != "web_search_call"]
                record(dict(row, origin="recording", items=[v["type"] for v in items]))
                self.send_items(items)
                return
            latest = history[-1]
            request_text = str(latest.get("content", ""))
            if (index < 3 or request.get("model") != "kimi-k3.1-pro" or not corrected
                    or not details.get("forecastMatchesRecording") or len(material) != 1
                    or latest.get("role") != "user" or source["request"] not in request_text
                    or source["recordedAt"] not in request_text):
                raise ValueError("answer-only request lacks verified original task, clock, correction or page")
            if os.environ.get("HANGZHOU_CAPTURE_FINAL_INPUT") == "1":
                (out / "answer-only-input.json").write_text(json.dumps(request, ensure_ascii=False))
            row.update(toolCount=0, sourceVerified=True)
            if args.kimi_key_file:
                slot = claim_slot(args.allowance_directory, out.name)
                record(dict(row, origin="Kimi", allowanceSlot=slot))
                self.forward_final(request, slot)
            else:
                record(dict(row, origin="offline scripted final"))
                self.send_items([offline_answer(source["fetches"][0]["body"])])

        def do_POST(self):
            if self.path == "/close":
                self.send_response(204)
                self.end_headers()
                threading.Thread(target=self.server.shutdown).start()
                return
            if self.path != "/v1/responses":
                self.send_error(404)
                return
            self.streaming = False
            try:
                self.sample(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
            except (ValueError, OSError, KeyError) as exc:
                reason = f"HTTP {exc.code}" if isinstance(exc, urllib.error.HTTPError) else str(exc)[:180]
                (out / "driver-error.txt").write_text(reason)
                if self.streaming:
                    self.close_connection = True
                else:
                    self.send_error(422)

    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    try:
        (out / "provider-url").write_text(f"http://127.0.0.1:{server.server_port}/v1")
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
