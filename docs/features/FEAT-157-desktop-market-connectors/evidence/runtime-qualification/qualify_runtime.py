#!/usr/bin/env python3
"""FEAT-157 normal loopback protocol qualification; never kills processes.

Uses the existing pinned executable unchanged. All HTTP endpoints are owned
loopback servers, and no external credentials/environment are inherited.
Loopback Responses emits ordinary synthetic text only; it is not a model test.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import queue
import shutil
import subprocess
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class Journal:
    def __init__(self, path):
        self.stream = path.open("w", encoding="utf-8")
        self.lock = threading.Lock()

    def write(self, kind, data):
        with self.lock:
            self.stream.write(json.dumps({"time": time.time(), "kind": kind, "data": data}, ensure_ascii=False) + "\n")
            self.stream.flush()


class LocalServer(ThreadingHTTPServer):
    daemon_threads = True
    block_on_close = False

    def __init__(self, journal):
        super().__init__(("127.0.0.1", 0), LocalHandler)
        self.journal = journal
        self.calls = []
        self.provider_requests = []
        self.thread = threading.Thread(target=self.serve_forever, daemon=True)
        self.thread.start()

    def close_normally(self):
        self.shutdown()
        self.server_close()
        self.thread.join(timeout=5)


class LocalHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *_):
        pass

    def reply(self, code, data=None, content_type="application/json"):
        raw = b"" if data is None else (data if isinstance(data, bytes) else json.dumps(data).encode())
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Connection", "close")
        self.end_headers()
        if raw:
            self.wfile.write(raw)

    def do_GET(self):
        self.server.journal.write("local_http_get", self.path)
        self.reply(405)

    def do_DELETE(self):
        self.server.journal.write("local_http_delete", self.path)
        self.reply(204)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length > 2 * 1024 * 1024:
            self.reply(413)
            return
        body = json.loads(self.rfile.read(length))
        if self.path == "/v1/responses":
            self.server.provider_requests.append(body)
            self.server.journal.write("loopback_responses_request", body)
            index = len(self.server.provider_requests)
            item = {"id": f"msg_local_{index}", "type": "message", "role": "assistant", "phase": "final_answer", "status": "completed", "content": [{"type": "output_text", "text": "Local protocol qualification completed.", "annotations": []}]}
            response = {"id": f"resp_local_{index}", "status": "completed", "output": [item], "usage": {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2}}
            events = [
                {"type": "response.created", "response": {"id": response["id"], "status": "in_progress", "output": []}},
                {"type": "response.output_item.added", "output_index": 0, "item": item},
                {"type": "response.output_item.done", "output_index": 0, "item": item},
                {"type": "response.completed", "response": response},
            ]
            raw = "".join("data: " + json.dumps(event) + "\n\n" for event in events).encode()
            self.reply(200, raw, "text/event-stream")
            return
        if not self.path.startswith("/mcp/"):
            self.reply(404)
            return
        name = self.path.rsplit("/", 1)[-1]
        self.server.calls.append({"server": name, "request": body})
        self.server.journal.write("local_mcp_request", {"server": name, "request": body})
        if "id" not in body:
            self.reply(202)
            return
        method = body.get("method")
        if method == "initialize":
            result = {"protocolVersion": body.get("params", {}).get("protocolVersion", "2025-03-26"), "capabilities": {"tools": {"listChanged": False}}, "serverInfo": {"name": "qualification_" + name, "version": "1.0.0"}}
        elif method == "tools/list":
            result = {"tools": [{"name": name + "_read", "description": "Read a fixed public synthetic value.", "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}, "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}}]}
        elif method in ("resources/list", "resources/templates/list"):
            result = {"resources" if method == "resources/list" else "resourceTemplates": []}
        elif method == "ping":
            result = {}
        elif method == "tools/call":
            result = {"content": [{"type": "text", "text": "synthetic public value"}], "isError": False}
        else:
            self.reply(200, {"jsonrpc": "2.0", "id": body["id"], "error": {"code": -32601, "message": "Method not supported by local qualification service"}})
            return
        self.reply(200, {"jsonrpc": "2.0", "id": body["id"], "result": result})


class Native:
    def __init__(self, binary, home, cwd, journal):
        self.journal = journal
        self.incoming = queue.Queue()
        self.received = []
        self.sequence = 0
        self.stderr = []
        environment = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "HOME": str(home.parent), "CODEX_HOME": str(home), "XDG_CONFIG_HOME": str(home.parent / "xdg"), "TMPDIR": str(home.parent), "LANG": "en_US.UTF-8", "NO_PROXY": "127.0.0.1,localhost", "RUST_LOG": "warn"}
        self.process = subprocess.Popen([str(binary), "app-server", "--listen", "stdio://", "--strict-config"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", bufsize=1, cwd=cwd, env=environment)
        self.journal.write("runtime_started", {"pid": self.process.pid, "binary": str(binary), "cwd": str(cwd), "environment_keys": sorted(environment)})
        threading.Thread(target=self.read_stdout, daemon=True).start()
        threading.Thread(target=self.read_stderr, daemon=True).start()

    def read_stdout(self):
        for line in self.process.stdout:
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                self.journal.write("non_json_stdout", line)
                continue
            self.journal.write("runtime_response", msg)
            self.received.append(msg)
            self.incoming.put(msg)

    def read_stderr(self):
        for line in self.process.stderr:
            self.stderr.append(line)
            self.journal.write("runtime_stderr", line.rstrip())

    def send(self, msg):
        self.journal.write("runtime_request", msg)
        self.process.stdin.write(json.dumps(msg) + "\n")
        self.process.stdin.flush()

    def request(self, method, params, timeout=20):
        self.sequence += 1
        request_id = self.sequence
        self.send({"id": request_id, "method": method, "params": params})
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            try:
                msg = self.incoming.get(timeout=max(0.01, end - time.monotonic()))
            except queue.Empty:
                break
            if msg.get("id") == request_id:
                return msg
            if "id" in msg and "method" in msg:
                raise RuntimeError("Unexpected server request; no approvals or tool execution authorized by this harness")
        raise TimeoutError("Runtime request timeout: " + method)

    def result(self, method, params, timeout=20):
        msg = self.request(method, params, timeout)
        if "error" in msg:
            raise RuntimeError(f"{method}: {msg['error']}")
        return msg["result"]

    def wait_notification(self, predicate, timeout=20):
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            for msg in self.received:
                if predicate(msg):
                    return msg
            time.sleep(0.05)
        raise TimeoutError("Expected normal lifecycle notification unavailable")

    def close_normally(self):
        if self.process.stdin and not self.process.stdin.closed:
            self.process.stdin.close()
        try:
            code = self.process.wait(timeout=20)
            self.journal.write("runtime_normal_eof_exit", {"pid": self.process.pid, "exit_code": code})
            return {"pid": self.process.pid, "exit_code": code, "normal_eof": True}
        except subprocess.TimeoutExpired:
            # No terminate/kill/signal fallback. The caller preserves all files.
            self.journal.write("runtime_stop_pending", {"pid": self.process.pid})
            return {"pid": self.process.pid, "normal_eof": False, "status": "STOP_PENDING"}


def model_catalog():
    return {"models": [{"slug": "qualification-text", "display_name": "Qualification text", "description": "Synthetic loopback response only", "default_reasoning_level": "none", "supported_reasoning_levels": [{"effort": "none", "description": "No reasoning"}], "shell_type": "shell_command", "visibility": "list", "supported_in_api": True, "priority": 0, "availability_nux": None, "upgrade": None, "base_instructions": "Return the local qualification response without invoking tools.", "model_messages": None, "supports_reasoning_summaries": False, "default_reasoning_summary": "none", "support_verbosity": False, "default_verbosity": None, "apply_patch_tool_type": None, "truncation_policy": {"mode": "bytes", "limit": 10000}, "supports_parallel_tool_calls": False, "supports_image_detail_original": False, "context_window": 128000, "max_context_window": 128000, "auto_compact_token_limit": 100000, "effective_context_window_percent": 95, "experimental_supported_tools": [], "input_modalities": ["text"], "supports_search_tool": False, "use_responses_lite": False}]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    journal = Journal(args.output / "wire.jsonl")
    lock = json.loads((args.workspace / "yijie-desktop/contracts/runtime-chat-models.candidate.json").read_text())
    artifact = args.workspace / "yijie-codex/.yijie/build/chat-models-stream-args/aarch64-apple-darwin"
    binary = artifact / "codex"
    assert digest(binary) == lock["runtime_artifact"]["sha256"]
    assert digest(artifact / "runtime-manifest.json") == lock["runtime_manifest_sha256"]
    root = Path(tempfile.mkdtemp(prefix="feat157-local-mcp-")).resolve()
    home, cwd = root / "codex-home", root / "workspace"
    home.mkdir()
    cwd.mkdir()
    server = LocalServer(journal)
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    (home / "catalog.json").write_text(json.dumps(model_catalog()))
    config = f'''model = "qualification-text"
model_provider = "qualification"
model_catalog_json = {json.dumps(str(home / "catalog.json"))}
check_for_update_on_startup = false
web_search = "disabled"
mcp_oauth_credentials_store = "file"
approval_policy = "never"
sandbox_mode = "read-only"
[analytics]
enabled = false
[features]
hooks = false
plugins = false
apps = false
tool_suggest = false
shell_snapshot = false
multi_agent = false
memories = false
shell_tool = false
unified_exec = false
[model_providers.qualification]
name = "Local protocol qualification"
base_url = "{base_url}/v1"
wire_api = "responses"
requires_openai_auth = false
supports_websockets = false
request_max_retries = 0
stream_max_retries = 0
[mcp_servers.global]
url = "{base_url}/mcp/global"
enabled = true
startup_timeout_sec = 5
tool_timeout_sec = 5
'''
    (home / "config.toml").write_text(config)
    (args.output / "synthetic-config.toml").write_text(config)
    report = {"harness_sha256": digest(Path(__file__)), "runtime_source": lock["runtime_source"], "runtime_artifact": lock["runtime_artifact"], "runtime_manifest_sha256": lock["runtime_manifest_sha256"], "runtime_schema": lock["runtime_schema"], "temp_root": str(root), "credential_mode": "empty isolated synthetic file store; no credentials read or written; production Keyring NOT TESTED", "external_calls": 0, "real_model_calls": 0, "cases": [], "normal_shutdown": []}
    native = None
    try:
        native = Native(binary, home, cwd, journal)
        report["initialize"] = native.result("initialize", {"clientInfo": {"name": "yijie_feat157_qualification", "version": "0.1.0"}, "capabilities": {"experimentalApi": False}})
        native.send({"method": "initialized", "params": {}})

        def start(label, overrides):
            result = native.result("thread/start", {"model": "qualification-text", "modelProvider": "qualification", "cwd": str(cwd), "approvalPolicy": "never", "sandbox": "read-only", "baseInstructions": "Use only synthetic loopback protocol qualification content.", "developerInstructions": "Return text only; do not invoke any tool.", "ephemeral": False, "config": overrides})
            thread_id = result["thread"]["id"]
            report["cases"].append({"label": label + "_start", "thread_id": thread_id, "config": overrides, "response": result})
            return thread_id

        def inventory(label, thread_id):
            pages, cursor = [], None
            while True:
                params = {"threadId": thread_id, "detail": "toolsAndAuthOnly", "limit": 1}
                if cursor is not None:
                    params["cursor"] = cursor
                page = native.result("mcpServerStatus/list", params)
                pages.append(page)
                cursor = page.get("nextCursor")
                if cursor is None:
                    break
                if len(pages) > 5:
                    raise RuntimeError("Unexpected unbounded local MCP pagination")
            rows = [row for page in pages for row in page["data"]]
            simple = {row["name"]: sorted(row["tools"]) for row in rows}
            report["cases"].append({"label": label, "thread_id": thread_id, "inventory": simple, "pages": pages})
            return simple

        def selected(name=None):
            result = {"mcp_servers.global.enabled": False}
            if name:
                result["mcp_servers." + name] = {"url": base_url + "/mcp/" + name, "enabled": True, "startup_timeout_sec": 5, "tool_timeout_sec": 5}
            return result

        empty = start("empty_object", {"mcp_servers": {}})
        report["empty_object_inventory"] = inventory("empty_object_inventory", empty)
        denied = start("explicit_empty", selected())
        report["explicit_empty_inventory"] = inventory("explicit_empty_inventory", denied)
        alpha = start("alpha", selected("alpha"))
        beta = start("beta", selected("beta"))
        report["alpha_inventory"] = inventory("alpha_inventory", alpha)
        report["beta_inventory"] = inventory("beta_inventory", beta)
        report["alpha_recheck_inventory"] = inventory("alpha_recheck_inventory", alpha)

        # Ordinary local text responses materialize history and expose the actual
        # model-facing tool list. No tool is called by the synthetic provider.
        def text_turn(thread_id, label):
            response = native.result("turn/start", {"threadId": thread_id, "input": [{"type": "text", "text": "Record one ordinary local qualification response."}]})
            turn_id = response["turn"]["id"]
            terminal = native.wait_notification(lambda msg: msg.get("method") == "turn/completed" and msg.get("params", {}).get("threadId") == thread_id and msg.get("params", {}).get("turn", {}).get("id") == turn_id)
            value = {"label": label, "thread_id": thread_id, "response": response, "terminal": terminal, "loopback_request_index": len(server.provider_requests) - 1}
            report.setdefault("synthetic_turns", []).append(value)
            return value

        text_turn(denied, "explicit_empty_model_surface")
        text_turn(alpha, "alpha_before_resume")
        report["native_before_resume"] = native.result("thread/read", {"threadId": alpha, "includeTurns": True})
        swap = selected("beta")
        # Cold resume does not inherit the original ephemeral config overrides;
        # a disabled stanza must still have a valid complete transport.
        swap["mcp_servers.alpha"] = {"url": base_url + "/mcp/alpha", "enabled": False, "startup_timeout_sec": 5, "tool_timeout_sec": 5}
        report["loaded_resume"] = native.request("thread/resume", {"threadId": alpha, "config": swap})
        report["loaded_resume_inventory"] = inventory("loaded_resume_inventory", alpha)
        report["unsubscribe"] = native.result("thread/unsubscribe", {"threadId": alpha})
        report["idle_unsubscribed_status"] = native.result("thread/read", {"threadId": alpha, "includeTurns": False})
        report["cold_resume"] = native.request("thread/resume", {"threadId": alpha, "config": swap})
        report["cold_resume_inventory"] = inventory("cold_resume_inventory", alpha)
        report["native_after_resume"] = native.result("thread/read", {"threadId": alpha, "includeTurns": True})
        text_turn(alpha, "beta_after_cold_resume")
        report["native_after_second_turn"] = native.result("thread/read", {"threadId": alpha, "includeTurns": True})
        before = report["native_before_resume"]["thread"]
        after = report["native_after_resume"]["thread"]
        report["same_thread_and_prior_history"] = before["id"] == after["id"] and before["turns"] == after["turns"]
        report["status"] = "COMPLETED_OBSERVATIONS"
    except Exception as error:
        report["status"] = "INCOMPLETE"
        report["error"] = str(error)
    finally:
        if native:
            stopped = native.close_normally()
            report["normal_shutdown"].append(stopped)
            report["runtime_stderr_lines"] = len(native.stderr)
        else:
            stopped = {"normal_eof": True}
        report["loopback_responses_requests"] = len(server.provider_requests)
        report["mcp_method_counts"] = {method: sum(call["request"].get("method") == method for call in server.calls) for method in sorted({call["request"].get("method", "") for call in server.calls})}
        report["loopback_provider_tool_names"] = [[tool.get("name", tool.get("type")) for tool in body.get("tools", [])] for body in server.provider_requests]
        server.close_normally()
        if stopped.get("normal_eof"):
            shutil.rmtree(root)
            report["temporary_data_removed_after_exit"] = True
        else:
            report["temporary_data_removed_after_exit"] = False
            report["status"] = "STOP_PENDING"
        (args.output / "result.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        journal.stream.close()
    print(json.dumps({k: report.get(k) for k in ("status", "error", "empty_object_inventory", "explicit_empty_inventory", "alpha_inventory", "beta_inventory", "loaded_resume_inventory", "cold_resume_inventory", "loopback_responses_requests", "mcp_method_counts", "normal_shutdown")}, ensure_ascii=False))
    return 0 if report["status"] == "COMPLETED_OBSERVATIONS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
