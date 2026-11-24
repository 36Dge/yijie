"""Replay the November 24 turn through the real Host and Runtime. Live mode is opt-in."""

import argparse
from collections import Counter
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import threading
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[5]
GAP = "request_followup_search"
SOURCE = json.loads(
    Path(__file__).with_name("hangzhou-hosted-source-20261124.json").read_text()
)


def recording(path):
    steps, step, pro, progress = [], [], [], []
    prompt = None
    for entry in map(json.loads, path.read_text().splitlines()):
        q = entry["payload"]
        kind = q.get("type")
        if entry["type"] == "response_item":
            if (
                kind in ("web_search_call", "function_call")
                or kind == "message"
                and q["role"] == "assistant"
            ):
                item = {
                    k: v
                    for k, v in q.items()
                    if k != "internal_chat_message_metadata_passthrough"
                }
                if kind == "web_search_call" and item.get("status") != "completed":
                    raise ValueError("expected a completed native provider search")
                item.setdefault("status", "completed")
                step.append(item)
        elif entry["type"] == "event_msg":
            if kind == "token_count" and step:
                steps.append(step)
                step = []
            elif kind == "user_message":
                if prompt is not None:
                    raise ValueError("expected one user submission")
                prompt = q["message"]
            elif kind == "agent_message" and q["phase"] == "commentary":
                progress.append(q["message"])
            elif (
                kind == "mcp_tool_call_end"
                and q["invocation"]["tool"] == "kimi_web_search_pro"
            ):
                pro.append(q["result"]["Ok"])
    ids = [i["id"] for batch in steps for i in batch if i["type"] == "web_search_call"]
    assert len(set(ids)) == len(ids) == 5 and len(steps) == 6 and len(pro) == 2
    receipts = [r["_meta"]["ai.yijie/deep-search-receipt"] for r in pro]
    assert [r["relation"] for r in receipts] == ["first", "reused"]
    assert len({r["operation_id"] for r in receipts}) == 1
    assert all(r["dispatch"] == "responded" for r in receipts)
    assert sorted(Counter(progress).values()) == [1, 4]
    return prompt, steps, pro, progress


def function(name, call_id, arguments):
    return {
        "type": "function_call",
        "id": "fc_" + call_id,
        "call_id": call_id,
        "name": name,
        "arguments": json.dumps(arguments, ensure_ascii=False),
        "status": "completed",
    }


def answer(text):
    return {
        "type": "message",
        "id": "msg_recorded_result",
        "role": "assistant",
        "status": "completed",
        "content": [
            {
                "type": "output_text",
                "text": "[[yijie-public-message-v1:final_answer]]\n" + text,
            }
        ],
    }


def day_line(row):
    return f"11月{row['day']}日 {row['condition']}，{row['low']}～{row['high']}℃"


def input_text(item):
    value = item.get("output", "")
    if isinstance(value, str):
        return value
    return "\n".join(x.get("text", "") for x in value)


class Replay:
    def __init__(self, mode, steps, pro):
        self.mode, self.steps, self.pro = mode, steps, pro
        self.calls = Counter()

    def tool(self, name, params):
        self.calls[name] += 1
        if name == "kimi_web_search_pro" and self.calls[name] <= len(self.pro):
            return self.pro[self.calls[name] - 1]
        if name != "kimi_web_fetch" or params["url"] != SOURCE["url"]:
            raise ValueError("unexpected retrieval operation")
        rows = SOURCE["rows"][:-1] if self.mode == "gap" else SOURCE["rows"]
        body = {
            "url": SOURCE["url"],
            "title": "杭州天气预报",
            "markdown": "\n".join(map(day_line, rows)),
            "truncated": self.mode == "gap",
        }
        return {
            "isError": False,
            "content": [{"type": "text", "text": json.dumps(body, ensure_ascii=False)}],
            "structuredContent": body,
        }

    def sample(self, request, index):
        tools = {tool.get("name", tool["type"]) for tool in request.get("tools", [])}
        history = request["input"]
        calls = {
            i["call_id"]: input_text(i)
            for i in history
            if i.get("type") == "function_call_output"
        }
        page = calls.get("known_weather_page", "")
        all_days = [day_line(r) for r in SOURCE["rows"]]
        emitted = "\n".join(all_days) + "\n" + SOURCE["url"]
        if index == 2:
            goal_id = next(
                i["call_id"] for i in self.steps[1] if i["type"] == "function_call"
            )
            assert '"goal":null' in calls.get(goal_id, ""), (
                "original empty get_goal result did not reach the next sample"
            )
        if self.mode == "baseline":
            assert GAP not in tools and "web_search" in tools
            return self.steps[index]
        if index < 2:
            assert "web_search" in tools and GAP not in tools
            return self.steps[index]
        if self.mode == "stalled":
            if index == 2:
                assert GAP in tools and "web_search" not in tools
                # The old model's third identical summary and second empty goal read.
                return [i for i in self.steps[3] if i["type"] != "web_search_call"]
            assert index == 3 and not tools
            return [
                answer("已取得杭州本周以晴到多云为主的趋势，尚缺可核实的逐日数据。")
            ]
        if not page:
            assert index == 2 and GAP in tools and "web_search" not in tools
            assert any(
                SOURCE["url"] in str(i.get("action", {}))
                for i in history
                if i.get("type") == "web_search_call"
            )
            js = (
                "const page = await tools.mcp__yijie_web__kimi_web_fetch({url:"
                + json.dumps(SOURCE["url"])
                + "}); text(page.structuredContent.markdown);"
            )
            return [function("exec", "known_weather_page", {"input": js})]
        if all(line in page for line in all_days):
            assert index == 3 and GAP in tools and "web_search" not in tools
            return [answer(emitted)]
        if not all(line in page for line in all_days[:-1]) or all_days[-1] in page:
            raise ValueError(
                "incomplete fixture did not deliver the expected six source rows"
            )
        if "one_missing_day" not in calls:
            assert index == 3 and GAP in tools and "web_search" not in tools
            return [
                function(
                    GAP,
                    "one_missing_day",
                    {
                        "missing_fact": "杭州11月30日的天气和高低温",
                        "query": "杭州 11月30日 晴雨 最高最低气温",
                    },
                )
            ]
        assert index == 4 and GAP not in tools and "web_search" in tools
        assert "next request may use hosted search" in calls["one_missing_day"]
        # The local provider serves the held-out source row inside this focused search.
        # Its terminal response may use precisely the material this sample received.
        lookup = {
            "id": "ws_missing_day",
            "type": "web_search_call",
            "status": "completed",
            "action": {
                "type": "search",
                "query": "杭州 11月30日 晴雨 最高最低气温",
                "sources": [
                    {"type": "url", "url": SOURCE["url"], "title": "杭州天气预报"}
                ],
            },
        }
        return [lookup, answer(emitted)]


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


def run(args):
    prompt, steps, pro, progress = recording(args.recording)
    directory = args.directory.resolve()
    directory.mkdir(mode=0o700, parents=True, exist_ok=False)
    live = args.mode == "live"
    if live and (not args.key_file or not args.allowance):
        raise ValueError(
            "live run requires an explicit key file and a fresh task allowance directory"
        )
    if live:
        # A run is one user turn, even if a caller restarts this script.
        args.allowance.mkdir(mode=0o700, parents=True, exist_ok=False)
    replay = Replay(args.mode, steps, pro)
    credentials = secrets.token_hex(32)
    attempts = []
    fatal = []
    grant_lock = threading.Lock()
    descriptors = json.loads(
        (ROOT / "yijie-contracts/sdks/go/builtinweb/tools.json").read_text()
    )

    def persist():
        (directory / "requests.json").write_text(
            json.dumps(attempts, ensure_ascii=False, indent=2)
        )

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def json_response(self, obj):
            raw = json.dumps(obj, ensure_ascii=False).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def mcp(self, req):
            if live:
                raise ValueError("live test only enables Kimi hosted search")
            method = req["method"]
            if "id" not in req:
                self.send_response(202)
                self.end_headers()
                return
            if method == "initialize":
                result = {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "recorded-web", "version": "1"},
                }
            elif method == "tools/list":
                result = {"tools": descriptors}
            elif method == "ping":
                result = {}
            elif method == "tools/call":
                params = req["params"]
                result = replay.tool(params["name"], params["arguments"])
            else:
                raise ValueError("unexpected MCP method " + method)
            self.json_response({"jsonrpc": "2.0", "id": req["id"], "result": result})

        def start_stream(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.end_headers()

        def emit(self, kind, **data):
            event = json.dumps(dict(type=kind, **data), ensure_ascii=False)
            self.wfile.write(("data: " + event + "\n\n").encode())
            self.wfile.flush()

        def serve_recording(self, request, row):
            items = replay.sample(request, row["n"] - 1)
            rid = f"resp_offline_{row['n']}"
            self.start_stream()
            self.emit(
                "response.created",
                response={"id": rid, "status": "in_progress", "output": []},
            )
            for i, item in enumerate(items):
                self.emit(
                    "response.output_item.added",
                    output_index=i,
                    item=dict(item, content=[]) if item["type"] == "message" else item,
                )
                if item["type"] == "message":
                    self.emit(
                        "response.output_text.delta",
                        item_id=item["id"],
                        output_index=i,
                        content_index=0,
                        delta=item["content"][0]["text"],
                    )
                self.emit("response.output_item.done", output_index=i, item=item)
                observe(row, item)
            self.emit(
                "response.completed",
                response={
                    "id": rid,
                    "status": "completed",
                    "output": items,
                    "usage": {
                        "input_tokens": 10,
                        "output_tokens": 10,
                        "total_tokens": 20,
                    },
                },
            )
            row["completed"] = True

        def forward(self, req, row):
            if (
                req.get("model") != "kimi-k3.1-pro"
                or req.get("stream") is not True
                or req.get("store") is True
            ):
                raise ValueError("unexpected live request shape")
            if row["n"] == 1 and not row["offered"]:
                raise ValueError(
                    "Kimi hosted search was unavailable at the start of the live turn"
                )
            # Reserve a model slot and, if offered, one possible provider pre-search
            # before sending. Unknown outcomes retain the reservation. The Kimi
            # Responses pre-search produces one web_search_call per searched request.
            if row["n"] > 6 or (
                row["offered"]
                and sum(
                    len(r["searchIDs"]) if r["completed"] else int(r["offered"])
                    for r in attempts
                )
                > 2
            ):
                raise ValueError("live allowance reached before dispatch")
            with (args.allowance / f"request-{row['n']}.json").open("x") as f:
                json.dump({"model": req["model"], "hostedOffered": row["offered"]}, f)
            target = Request(
                "https://api.moonshot.cn/v1/responses",
                data=json.dumps(req, ensure_ascii=False).encode(),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + args.key_file.read_text().strip(),
                },
                method="POST",
            )
            with build_opener(NoRedirect()).open(target, timeout=125) as res:
                row["http"] = res.status
                self.start_stream()
                for line in res:
                    if line.startswith(b"data: {"):
                        event = json.loads(line[6:])
                        if event["type"] == "response.output_item.done":
                            observe(row, event["item"])
                        elif event["type"] == "response.completed":
                            row["completed"] = (
                                event["response"]["status"] == "completed"
                            )
                            row["responseId"] = event["response"]["id"]
                    self.wfile.write(line)
                    if not line.strip():
                        self.wfile.flush()
            if not row["completed"]:
                raise ValueError("provider outcome not confirmed")

        def do_POST(self):
            try:
                if self.headers.get("Authorization") != "Bearer " + credentials:
                    self.send_error(403)
                    return
                req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                if self.path == "/mcp":
                    self.mcp(req)
                    return
                if self.path != "/v1/responses":
                    self.send_error(404)
                    return
                with grant_lock:
                    if fatal:
                        self.send_error(422)
                        return
                    names = [t.get("name", t["type"]) for t in req.get("tools", [])]
                    row = {
                        "n": len(attempts) + 1,
                        "offered": "web_search" in names,
                        "gapOffered": GAP in names,
                        "searchIDs": [],
                        "commentaryHashes": [],
                        "finalHashes": [],
                        "completed": False,
                    }
                    if not live:
                        outputs = {
                            i["call_id"]: input_text(i)
                            for i in req["input"]
                            if i.get("type") == "function_call_output"
                        }
                        page = outputs.get("known_weather_page", "")
                        row["deliveredDays"] = [
                            r["day"] for r in SOURCE["rows"] if day_line(r) in page
                        ]
                        row["emptyGoalOutputs"] = sum(
                            '"goal":null' in v for v in outputs.values()
                        )
                    attempts.append(row)
                    persist()
                    if live:
                        self.forward(req, row)
                    else:
                        self.serve_recording(req, row)
                    persist()
            except (ValueError, AssertionError, OSError, KeyError, IndexError) as e:
                import traceback

                fatal.append(
                    f"{type(e).__name__} at {traceback.extract_tb(e.__traceback__)[-1].lineno}: "
                    + (str(e.code) if isinstance(e, HTTPError) else str(e)[:160])
                )
                persist()
                self.send_error(422)

    def observe(row, item):
        if item.get("type") == "web_search_call" and item.get("status") == "completed":
            if item["id"] not in row["searchIDs"]:
                row["searchIDs"].append(item["id"])
        if item.get("type") == "message" and item.get("role") == "assistant":
            text = "".join(
                p.get("text", "")
                for p in item.get("content", [])
                if p.get("type") == "output_text"
            )
            declaration = re.match(
                r"^\[\[yijie[.-]public[.-]message[.-]v1:(commentary|final_answer)\]\]\s*\n",
                text,
            )
            phase = declaration[1] if declaration else item.get("phase")
            if declaration:
                text = text[declaration.end() :]
            if phase in ("commentary", "final_answer"):
                row[
                    "commentaryHashes" if phase == "commentary" else "finalHashes"
                ].append(digest(text))

    with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        config = {
            "Endpoint": f"http://127.0.0.1:{server.server_port}",
            "Token": credentials,
            "Prompt": prompt,
            "RecordedMCP": not live,
        }
        if not live:
            config["Prompt"] += "\n\n原始请求当地时间为 2026-11-24 11:54（亚洲/上海）。"
        (directory / "run.json").write_text(json.dumps(config, ensure_ascii=False))
        env = dict(
            os.environ,
            HANGZHOU_HOSTED_RUN=str(directory),
            YIJIE_CODEX_INTEGRATION_BINARY=str(args.artifact.resolve() / "codex"),
            YIJIE_CODEX_INTEGRATION_MANIFEST=str(
                args.artifact.resolve() / "runtime-manifest.json"
            ),
        )
        try:
            with (directory / "host.log").open("w") as log:
                result = subprocess.run(
                    [
                        "go",
                        "test",
                        "-count=1",
                        "-timeout",
                        "9m",
                        "-v",
                        "./internal/codex",
                        "-run",
                        "^TestHangzhouHostedSearchFollowup$",
                    ],
                    env=env,
                    cwd=ROOT / "yijie-agent-host",
                    stdout=log,
                    stderr=subprocess.STDOUT,
                )
        finally:
            server.shutdown()
            thread.join()
    if result.returncode or fatal:
        raise RuntimeError(
            f"native verification failed: {fatal}; see {directory / 'host.log'}"
        )
    native = json.loads((directory / "native.json").read_text())
    sent = [i for r in attempts for i in r["searchIDs"]]
    assert native["searchIDs"] == sent and len(set(sent)) == len(sent)
    assert list(map(digest, native["progress"])) == [
        h for r in attempts for h in r["commentaryHashes"]
    ]
    assert list(map(digest, native["finals"])) == [
        h for r in attempts for h in r["finalHashes"]
    ]
    assert (
        native["status"] == "completed"
        and len(native["finals"]) == 1
        and all(r["completed"] for r in attempts)
    )
    if not live:
        expected = {
            "baseline": (5, 5),
            "ready": (1, 2),
            "gap": (2, 2),
            "stalled": (1, 3),
        }[args.mode]
        assert (len(sent), len(native["progress"])) == expected
        assert native["progress"] == (
            progress
            if args.mode == "baseline"
            else progress[:2] + ([progress[1]] if args.mode == "stalled" else [])
        )
        assert Counter(native["localCalls"]) == replay.calls
        if args.mode in {"ready", "gap"}:
            assert all(day_line(r) in native["finals"][0] for r in SOURCE["rows"])
    result = {
        "mode": args.mode,
        "runtimeSha256": json.loads(
            (args.artifact / "runtime-manifest.json").read_text()
        )["runtime"]["sha256"],
        "modelRequests": len(attempts),
        "hostedSearch": len(sent),
        "progress": len(native["progress"]),
        "duplicateProgress": len(native["progress"]) - len(set(native["progress"])),
        "localTools": native["localCalls"],
        "finalAnswers": len(native["finals"]),
        "completed": True,
    }
    if live:
        text = native["finals"][0]
        days = []
        for r in SOURCE["rows"]:
            day = str(r["day"])
            pattern = re.compile(
                r"(?<![0-9])(?:11\s*[月./-]\s*)?" + day + r"(?:\s*日|(?=\s|[|（(/.-]))"
            )
            for line in text.splitlines():
                match = pattern.search(line)
                if match:
                    values = line[match.end() :]
                    if r["condition"] in line and all(
                        re.search(r"(?<![0-9])" + str(t) + r"(?![0-9])", values)
                        for t in (r["low"], r["high"])
                    ):
                        days.append(r["day"])
                        break
        result["forecastDaysMatched"] = days
        result["citesSource"] = bool(re.search(r"https?://[^\s)]+", text))
    (directory / "metrics.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(result, ensure_ascii=False))
    if live:
        assert 1 <= len(sent) <= 2 and len(attempts) <= 6
        assert result["duplicateProgress"] == 0 and result["citesSource"]
        assert result["forecastDaysMatched"] == [r["day"] for r in SOURCE["rows"]], (
            "compare with the issuing source before accepting the live answer"
        )


def digest(text):
    return hashlib.sha256(text.strip().encode()).hexdigest()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--recording", type=Path, required=True)
    p.add_argument("--artifact", type=Path, required=True)
    p.add_argument("--directory", type=Path, required=True)
    p.add_argument(
        "--mode", choices=("baseline", "ready", "gap", "stalled", "live"), required=True
    )
    p.add_argument("--key-file", type=Path)
    p.add_argument("--allowance", type=Path)
    run(p.parse_args())
