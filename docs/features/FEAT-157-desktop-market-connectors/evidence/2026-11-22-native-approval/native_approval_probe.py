"""Exercise the canonical Runtime with an isolated Home and ordinary loopback peers.

Usage: python3 native_approval_probe.py ARTIFACT_DIRECTORY NEW_SCRATCH_DIRECTORY
Python 3.11+. Each JSON line counts accepted calls at the local MCP endpoint.
"""

import hashlib
import http.server
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import threading
import tomllib
import uuid


def encode(value):
    return json.dumps(value, ensure_ascii=False).encode()


def message(text):
    return {"type": "message", "role": "assistant", "status": "completed",
            "content": [{"type": "output_text", "text": text, "annotations": []}]}


class Sample:
    def __init__(self):
        self.calls = {}
        self.accepted = 0
        self.sampling_step = 0
        self.reviews = 0
        self.deny_review = False
        self.scope = hashlib.sha256(b"isolated sample installation and method").hexdigest()
        self.phases = []
        self.choice = None

    def model_item(self, body, call_id):
        if ('risk_level' in body.get("instructions", "")
                or '"outcome"' in json.dumps(body.get("text", {}))):
            self.reviews += 1
            return message(json.dumps({
                "outcome": "deny" if self.deny_review else "allow", "user_authorization": "high",
                "risk_level": "low", "rationale": "Ordinary local sample.",
            }))
        step = self.sampling_step % 3
        self.sampling_step += 1
        if step == 0:
            return {"call_id": call_id, "type": "tool_search_call", "execution": "client",
                    "arguments": {"query": "ordinary public sample lookup", "limit": 1}, "status": "completed"}
        if step == 1:
            discovery = next(v for v in reversed(body["input"]) if v["type"] == "tool_search_output")
            group = next(v for v in discovery["tools"] if v["name"] == "mcp__yijie_market")
            return {"call_id": call_id, "type": "function_call", "namespace": group["name"],
                    "name": group["tools"][0]["name"], "arguments": '{"key":"blue"}', "status": "completed"}
        return message("Ordinary sample finished.")

    def respond_to_runtime(self, params):
        meta = params["_meta"]
        assert params["serverName"] == "yijie_market" and meta["yijieMarketCallRef"] in self.calls
        phase = meta["yijieNativePhase"]
        self.phases.append(phase)
        response = {"action": "accept", "content": {}, "_meta": None}
        if phase == "inspect":
            response["content"] = {"tool": "lookup", "title": "Local sample", "arguments": {"key": "blue"},
                                   "scope": self.scope, "remainingMs": 15000}
        elif phase == "user":
            assert meta["persist"] == ["session", "always"]
            if self.choice in ("session", "always"):
                response["_meta"] = {"persist": self.choice}
            elif self.choice in ("decline", "cancel"):
                response.update(action=self.choice, content=None)
            else:
                assert self.choice == "once"
        else:
            assert phase.startswith(("native_", "stored_")) and meta["yijieScope"] == self.scope
        return response


class Loopback(http.server.BaseHTTPRequestHandler):
    def log_message(self, *unused):
        pass

    def reply(self, status, data=b"", content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self.reply(405)

    def do_DELETE(self):
        self.reply(200)

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        sample = self.server.sample
        if self.path == "/v1/responses":
            rid = uuid.uuid4().hex
            item = sample.model_item(body, "call_" + rid)
            item["id"] = "item_" + rid
            events = [
                {"type": "response.created", "response": {"id": rid, "status": "in_progress", "output": []}},
                {"type": "response.output_item.added", "output_index": 0, "item": item},
                {"type": "response.output_item.done", "output_index": 0, "item": item},
                {"type": "response.completed", "response": {"id": rid, "status": "completed", "output": [item],
                 "usage": {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2}}},
            ]
            self.reply(200, b"".join(b"data: " + encode(event) + b"\n\n" for event in events), "text/event-stream")
            return
        if self.path != "/mcp":
            self.reply(404)
            return
        ident = body.get("id")
        method = body.get("method")
        if ident is None:
            self.reply(202)
            return
        if method is None:
            sample.calls[ident.removeprefix("sample-")].put(body["result"])
            self.reply(202)
            return
        if method == "tools/call":
            assert body["params"]["name"] == "lookup" and body["params"]["arguments"] == {"key": "blue"}
            self.market_call(sample, ident)
            return
        if method == "initialize":
            data = {"protocolVersion": "2025-11-25", "capabilities": {"tools": {}},
                    "serverInfo": {"name": "ordinary-sample", "version": "1"}}
        elif method == "tools/list":
            data = {"tools": [{"name": "lookup", "description": "Read an ordinary public sample.",
                     "inputSchema": {"type": "object", "properties": {"key": {"type": "string"}},
                                     "required": ["key"], "additionalProperties": False}}]}
        elif method == "ping":
            data = {}
        else:
            self.reply(405)
            return
        self.reply(200, encode({"jsonrpc": "2.0", "id": ident, "result": data}))

    def market_call(self, sample, ident):
        ref = str(uuid.uuid4())
        pending = queue.Queue()
        sample.calls[ref] = pending
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.end_headers()

        def event(data):
            self.wfile.write(b"event: message\ndata: " + encode({"jsonrpc": "2.0", **data}) + b"\n\n")
            self.wfile.flush()

        try:
            event({"id": "sample-" + ref, "method": "elicitation/create", "params": {"mode": "form",
                   "message": "Read the ordinary sample?", "requestedSchema": {"type": "object", "properties": {}},
                   "_meta": {"yijieKind": "gateway_native_approval_v1", "yijieMarketCallRef": ref}}})
            allowed = pending.get(timeout=20)["action"] == "accept"
            if allowed:
                sample.accepted += 1
            event({"id": ident, "result": {"isError": not allowed,
                   "content": [{"type": "text", "text": "42" if allowed else "cancelled"}]}})
        finally:
            del sample.calls[ref]


class Runtime:
    def __init__(self, binary, home, cwd, endpoint, sample):
        self.cwd, self.endpoint, self.sample = cwd, endpoint, sample
        self.incoming = queue.Queue()
        self.request_id = 0
        environment = {k: os.environ[k] for k in ("PATH", "USER", "LANG", "TMPDIR", "HOME") if k in os.environ}
        environment["CODEX_HOME"] = str(home)
        with (home.parent / "runtime.stderr").open("a") as log:
            self.process = subprocess.Popen([binary, "app-server", "--listen", "stdio://"], cwd=cwd, env=environment,
                                            text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=log)
        threading.Thread(target=self.read_output, daemon=True).start()

    def read_output(self):
        for line in self.process.stdout:
            self.incoming.put(json.loads(line))
        self.incoming.put(None)

    def send(self, value):
        self.process.stdin.write(json.dumps(value) + "\n")
        self.process.stdin.flush()

    def receive(self):
        value = self.incoming.get(timeout=30)
        if value is None:
            raise RuntimeError("Runtime exited before completing the request")
        if "method" in value and "id" in value:
            assert value["method"] == "mcpServer/elicitation/request"
            self.send({"id": value["id"], "result": self.sample.respond_to_runtime(value["params"])})
        return value

    def call(self, method, params):
        self.request_id += 1
        self.send({"id": self.request_id, "method": method, "params": params})
        while True:
            value = self.receive()
            if value.get("id") == self.request_id and "method" not in value:
                assert "error" not in value, value.get("error")
                return value["result"]

    def __enter__(self):
        self.call("initialize", {"clientInfo": {"name": "local-market-validation", "version": "1"},
                                 "capabilities": {"experimentalApi": False}})
        self.send({"method": "initialized", "params": {}})
        return self

    def __exit__(self, *unused):
        self.process.stdin.close()
        if self.process.wait(timeout=30) != 0:
            raise RuntimeError("Runtime did not exit normally")

    def thread(self, mode, existing=None):
        params = {"model": "gpt-5.4", "modelProvider": "sample", "cwd": str(self.cwd),
                  "approvalPolicy": "never" if mode == "full" else "on-request",
                  "approvalsReviewer": "auto_review" if mode == "auto" else "user",
                  "sandbox": "danger-full-access" if mode == "full" else "workspace-write",
                  "config": {"mcp_servers": {"yijie_market": {"enabled": True, "url": self.endpoint + "/mcp",
                             "default_tools_approval_mode": "approve", "supports_parallel_tool_calls": False}}}}
        if existing:
            self.call("thread/unsubscribe", {"threadId": existing})
            assert self.call("thread/resume", {**params, "threadId": existing})["thread"]["id"] == existing
            return existing
        return self.call("thread/start", {**params, "ephemeral": False})["thread"]["id"]

    def check(self, scenario, thread, choice, phases, count):
        sample = self.sample
        sample.choice, sample.phases = choice, []
        before = sample.accepted
        turn = self.call("turn/start", {"threadId": thread, "input": [{"type": "text",
                              "text": "Read the ordinary local sample."}]})["turn"]["id"]
        while True:
            event = self.receive()
            if event.get("method") == "turn/completed" and event["params"]["turn"]["id"] == turn:
                assert event["params"]["turn"]["status"] == "completed"
                break
        result = {"scenario": scenario, "phases": sample.phases, "acceptedLocalCalls": sample.accepted - before}
        print(json.dumps(result), flush=True)
        assert sample.phases == ["inspect", *phases] and sample.accepted - before == count, result


def main(artifact, scratch):
    scratch.mkdir(mode=0o700)
    home, cwd = scratch / "home", scratch / "workspace"
    home.mkdir(mode=0o700)
    cwd.mkdir(mode=0o700)
    binary = artifact / "codex"
    manifest = json.loads((artifact / "runtime-manifest.json").read_text())
    with binary.open("rb") as file:
        assert hashlib.file_digest(file, "sha256").hexdigest() == manifest["runtime"]["sha256"]
    sample = Sample()
    peer = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Loopback)
    peer.sample = sample
    threading.Thread(target=peer.serve_forever, daemon=True).start()
    endpoint = f"http://127.0.0.1:{peer.server_port}"
    (home / "config.toml").write_text(f'''model = "gpt-5.4"
model_provider = "sample"
[features]
tool_call_mcp_elicitation = true
hooks = false
[model_providers.sample]
name = "ordinary loopback"
base_url = "{endpoint}/v1"
wire_api = "responses"
requires_openai_auth = false
supports_websockets = false
request_max_retries = 0
stream_max_retries = 0
''')

    def saved_apps():
        return tomllib.loads((home / "config.toml").read_text()).get("apps", {})

    app = "yijie-market-" + sample.scope
    try:
        with Runtime(binary, home, cwd, endpoint, sample) as runtime:
            thread = runtime.thread("ask")
            runtime.check("once", thread, "once", ["user"], 1)
            runtime.check("cancel", thread, "cancel", ["user"], 0)
            runtime.check("decline", thread, "decline", ["user"], 0)
            runtime.check("session", thread, "session", ["user", "stored_session"], 1)
            runtime.check("session-after-resume", runtime.thread("ask", thread), None, ["native_session"], 1)
            runtime.check("always-in-new-thread", runtime.thread("ask"), "always", ["user", "stored_always"], 1)
            assert saved_apps()[app]["tools"]["lookup"]["approval_mode"] == "approve"

        with Runtime(binary, home, cwd, endpoint, sample) as runtime:
            thread = runtime.thread("ask")
            runtime.check("always-after-process-restart", thread, None, ["native_always"], 1)
            layer = next(v for v in runtime.call("config/read", {"includeLayers": True})["layers"]
                         if v["name"]["type"] == "user")
            assert layer["config"]["apps"][app]["tools"]["lookup"]["approval_mode"] == "approve"
            result = runtime.call("config/batchWrite", {"expectedVersion": layer["version"], "reloadUserConfig": True,
                                  "edits": [{"keyPath": "apps." + json.dumps(app), "mergeStrategy": "replace", "value": None}]})
            assert result["status"] == "ok" and app not in saved_apps()
            runtime.check("after-native-revocation", thread, "once", ["user"], 1)
            runtime.check("full", runtime.thread("full"), None, ["native_full"], 1)
            thread = runtime.thread("auto")
            runtime.check("guardian-allow", thread, None, ["native_auto"], 1)
            sample.deny_review = True
            runtime.check("guardian-deny", thread, None, ["native_auto_reject"], 0)
            assert sample.reviews >= 2
    finally:
        peer.shutdown()
        peer.server_close()


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
