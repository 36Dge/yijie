#!/usr/bin/env python3
"""Q-SEL-05: ordinary loopback MCP form elicitation, no external services.

The synthetic Gateway records the actual tools/call before requesting approval.
Host-side code queries a separately authenticated owner-only control path and
registers its decision there; the elicitation _meta is only an opaque reference.
"""
from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import queue
import shutil
import tempfile
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from qualify_runtime import Journal, Native, digest, model_catalog


def canonical_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class Gateway(ThreadingHTTPServer):
    daemon_threads = True
    block_on_close = False

    def __init__(self, journal):
        super().__init__(("127.0.0.1", 0), Handler)
        self.journal = journal
        self.owner_key = uuid.uuid4().hex  # Synthetic private control capability; never sent to Runtime.
        self.calls = {}
        self.pending_elicitations = {}
        self.provider_requests = []
        self.provider_step = 0
        self.active_case = None
        self.active_thread = None
        self.active_turn = None
        self.lock = threading.Lock()
        self.executions = []
        self.http_methods = []
        self.thread = threading.Thread(target=self.serve_forever, daemon=True)
        self.thread.start()

    def close_normally(self):
        self.shutdown()
        self.server_close()
        self.thread.join(timeout=5)


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *_):
        pass

    def reply(self, status, value=None, content_type="application/json"):
        data = b"" if value is None else value if isinstance(value, bytes) else json.dumps(value).encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Connection", "close")
        self.end_headers()
        if data:
            self.wfile.write(data)

    def control_allowed(self):
        return self.headers.get("X-Qualification-Owner") == self.server.owner_key

    def do_GET(self):
        if self.path.startswith("/control/calls/"):
            if not self.control_allowed():
                self.reply(403)
                return
            ref = self.path.rsplit("/", 1)[-1]
            with self.server.lock:
                record = self.server.calls.get(ref)
                public = None if record is None else {key: value for key, value in record.items() if key != "event"}
            self.server.journal.write("trusted_control_lookup", {"callRef": ref, "record": public})
            self.reply(200 if public is not None else 404, public)
            return
        self.reply(405)

    def do_DELETE(self):
        self.reply(204)

    def emit_sse(self, value):
        self.wfile.write(("event: message\ndata: " + json.dumps(value) + "\n\n").encode())
        self.wfile.flush()

    def provider(self, body):
        with self.server.lock:
            self.server.provider_step += 1
            step = self.server.provider_step
            case = self.server.active_case
            self.server.provider_requests.append(body)
        self.server.journal.write("loopback_responses_request", body)
        response_id = f"response_{case}_{step}"
        if step == 1:
            item = {"type": "function_call", "id": f"item_{case}", "call_id": f"model_call_{case}", "namespace": "mcp__gateway", "name": "lookup", "arguments": json.dumps({"key": "public-synthetic-record"})}
        elif step == 2:
            item = {"id": f"msg_{case}", "type": "message", "role": "assistant", "phase": "final_answer", "status": "completed", "content": [{"type": "output_text", "text": "Local approval qualification finished.", "annotations": []}]}
        else:
            self.reply(400, {"error": {"message": "ordinary qualification permits one tool call and one final response"}})
            return
        events = [
            {"type": "response.created", "response": {"id": response_id, "status": "in_progress", "output": []}},
            {"type": "response.output_item.done", "output_index": 0, "item": item},
            {"type": "response.completed", "response": {"id": response_id, "status": "completed", "output": [item], "usage": {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2}}},
        ]
        self.reply(200, "".join("data: " + json.dumps(item) + "\n\n" for item in events).encode(), "text/event-stream")

    def call_tool(self, body):
        params = body["params"]
        metadata = params.get("_meta", {})
        turn_meta = metadata.get("x-codex-turn-metadata", {})
        ref = str(uuid.uuid4())
        request_id = "elicitation_" + ref
        record = {"callRef": ref, "rpcCallId": body["id"], "server": "gateway", "tool": params["name"], "arguments": params.get("arguments"), "argumentsDigest": canonical_digest(params.get("arguments")), "threadId": metadata.get("threadId"), "turnId": turn_meta.get("turn_id"), "state": "awaiting_decision", "controlDecision": None, "elicitationResult": None, "event": threading.Event()}
        with self.server.lock:
            self.server.calls[ref] = record
            self.server.pending_elicitations[request_id] = ref
        self.server.journal.write("gateway_actual_call_registered", {key: value for key, value in record.items() if key != "event"})
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()
        self.close_connection = True
        request = {"jsonrpc": "2.0", "id": request_id, "method": "elicitation/create", "params": {"mode": "form", "message": "Review the registered local lookup through the trusted control channel.", "requestedSchema": {"type": "object", "properties": {}}, "_meta": {"yijieCallRef": ref, "yijieKind": "gateway_call_approval"}}}
        self.server.journal.write("gateway_elicitation_sent", request)
        self.emit_sse(request)
        arrived = record["event"].wait(12)
        with self.server.lock:
            accepted = arrived and record["controlDecision"] == "accept" and record["elicitationResult"].get("action") == "accept" and record["threadId"] == self.server.active_thread and record["turnId"] == self.server.active_turn
            record["state"] = "completed" if accepted else "declined" if arrived else "unconfirmed"
            if accepted:
                self.server.executions.append({"callRef": ref, "tool": record["tool"], "argumentsDigest": record["argumentsDigest"], "result": "public-synthetic-value"})
            result = {"content": [{"type": "text", "text": "public-synthetic-value" if accepted else "Lookup was not approved; no lookup executed."}], "isError": not accepted}
        reply = {"jsonrpc": "2.0", "id": body["id"], "result": result}
        self.server.journal.write("gateway_tool_result", {"callRef": ref, "executed": accepted, "response": reply})
        self.emit_sse(reply)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length > 2 * 1024 * 1024:
            self.reply(413)
            return
        body = json.loads(self.rfile.read(length))
        if self.path == "/v1/responses":
            self.provider(body)
            return
        if self.path == "/control/decision":
            if not self.control_allowed():
                self.reply(403)
                return
            with self.server.lock:
                record = self.server.calls.get(body.get("callRef"))
                valid = record is not None and record["state"] == "awaiting_decision" and record["controlDecision"] is None and body.get("decision") in ("accept", "decline") and body.get("argumentsDigest") == record["argumentsDigest"] and body.get("threadId") == record["threadId"] == self.server.active_thread and body.get("turnId") == record["turnId"] == self.server.active_turn
                if valid:
                    record["controlDecision"] = body["decision"]
            self.server.journal.write("trusted_control_decision", {"request": body, "accepted": valid})
            self.reply(200 if valid else 409, {"recorded": valid})
            return
        if self.path != "/mcp/gateway":
            self.reply(404)
            return
        self.server.journal.write("local_mcp_message", body)
        self.server.http_methods.append(body.get("method", "elicitation_response"))
        if "method" not in body:
            with self.server.lock:
                ref = self.server.pending_elicitations.get(body.get("id"))
                record = self.server.calls.get(ref)
                if record is not None:
                    record["elicitationResult"] = body.get("result", {})
                    record["event"].set()
            self.reply(202)
            return
        if "id" not in body:
            self.reply(202)
            return
        method = body["method"]
        if method == "initialize":
            result = {"protocolVersion": body["params"]["protocolVersion"], "capabilities": {"tools": {"listChanged": False}}, "serverInfo": {"name": "qualification-gateway", "version": "1.0.0"}}
        elif method == "tools/list":
            result = {"tools": [{"name": "lookup", "description": "Read one public synthetic value after the Gateway approval.", "inputSchema": {"type": "object", "properties": {"key": {"type": "string"}}, "required": ["key"], "additionalProperties": False}, "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}}]}
        elif method == "tools/call":
            self.call_tool(body)
            return
        elif method in ("resources/list", "resources/templates/list"):
            result = {"resources" if method == "resources/list" else "resourceTemplates": []}
        elif method == "ping":
            result = {}
        else:
            self.reply(200, {"jsonrpc": "2.0", "id": body["id"], "error": {"code": -32601, "message": "Unsupported qualification method"}})
            return
        self.reply(200, {"jsonrpc": "2.0", "id": body["id"], "result": result})


class NativeWithCallbacks(Native):
    def request(self, method, params, timeout=20):
        self.sequence += 1
        request_id = self.sequence
        self.send({"id": request_id, "method": method, "params": params})
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            try:
                message = self.incoming.get(timeout=max(0.01, end - time.monotonic()))
            except queue.Empty:
                break
            if message.get("id") == request_id and "method" not in message:
                return message
            # All messages are already saved in received by the sole reader;
            # callback processing happens only after the real turn ID is known.
        raise TimeoutError("Runtime request timeout: " + method)


def control(gateway, method, path, value=None):
    connection = http.client.HTTPConnection("127.0.0.1", gateway.server_address[1], timeout=5)
    body = None if value is None else json.dumps(value)
    connection.request(method, path, body=body, headers={"X-Qualification-Owner": gateway.owner_key, "Content-Type": "application/json"})
    response = connection.getresponse()
    data = json.loads(response.read())
    connection.close()
    if response.status != 200:
        raise RuntimeError("Trusted control request was not accepted")
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    journal = Journal(args.output / "wire.jsonl")
    lock = json.loads((args.workspace / "yijie-desktop/contracts/runtime-chat-models.candidate.json").read_text())
    artifact = args.workspace / "yijie-codex/.yijie/build/chat-models-stream-args/aarch64-apple-darwin"
    assert digest(artifact / "codex") == lock["runtime_artifact"]["sha256"]
    assert digest(artifact / "runtime-manifest.json") == lock["runtime_manifest_sha256"]
    root = Path(tempfile.mkdtemp(prefix="feat157-local-elicitation-")).resolve()
    home, cwd = root / "codex-home", root / "workspace"
    home.mkdir()
    cwd.mkdir()
    gateway = Gateway(journal)
    origin = f"http://127.0.0.1:{gateway.server_address[1]}"
    (home / "catalog.json").write_text(json.dumps(model_catalog()))
    config = f'''model = "qualification-text"
model_provider = "qualification"
model_catalog_json = {json.dumps(str(home / "catalog.json"))}
check_for_update_on_startup = false
web_search = "disabled"
mcp_oauth_credentials_store = "file"
approval_policy = "on-request"
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
base_url = "{origin}/v1"
wire_api = "responses"
requires_openai_auth = false
supports_websockets = false
request_max_retries = 0
stream_max_retries = 0
[mcp_servers.gateway]
url = "{origin}/mcp/gateway"
enabled = true
enabled_tools = ["lookup"]
default_tools_approval_mode = "auto"
startup_timeout_sec = 5
tool_timeout_sec = 20
supports_parallel_tool_calls = false
'''
    (home / "config.toml").write_text(config)
    (args.output / "synthetic-config.toml").write_text(config)
    report = {"harness_sha256": digest(Path(__file__)), "runtime_artifact": lock["runtime_artifact"], "runtime_manifest_sha256": lock["runtime_manifest_sha256"], "runtime_source": lock["runtime_source"], "temp_root": str(root), "external_calls": 0, "real_model_calls": 0, "credentials_read_or_written": 0, "cases": [], "status": "NOT_RUN"}
    native = None
    try:
        native = NativeWithCallbacks(artifact / "codex", home, cwd, journal)
        native.result("initialize", {"clientInfo": {"name": "yijie_feat157_elicitation", "version": "0.1.0"}, "capabilities": {"experimentalApi": False}})
        native.send({"method": "initialized", "params": {}})
        handled = set()
        for decision in ("accept", "decline"):
            with gateway.lock:
                gateway.active_case = decision
                gateway.provider_step = 0
                gateway.active_thread = None
                gateway.active_turn = None
            started = native.result("thread/start", {"cwd": str(cwd), "model": "qualification-text", "modelProvider": "qualification", "approvalPolicy": "on-request", "approvalsReviewer": "user", "sandbox": "read-only", "ephemeral": False, "baseInstructions": "Use the provided local synthetic lookup once and return its result.", "developerInstructions": "Only the local Gateway lookup is requested. The Gateway requires approval before reading its synthetic value."})
            thread_id = started["thread"]["id"]
            with gateway.lock:
                gateway.active_thread = thread_id
            response = native.result("turn/start", {"threadId": thread_id, "input": [{"type": "text", "text": "Please use the local Gateway lookup for the public synthetic record."}]})
            turn_id = response["turn"]["id"]
            with gateway.lock:
                gateway.active_turn = turn_id
            case = {"decision": decision, "threadId": thread_id, "turnId": turn_id, "callbacks": []}
            report["cases"].append(case)
            end = time.monotonic() + 20
            terminal = None
            while time.monotonic() < end:
                for message in list(native.received):
                    if message.get("method") == "mcpServer/elicitation/request" and message.get("id") not in handled:
                        handled.add(message["id"])
                        params = message["params"]
                        if params.get("threadId") != thread_id or params.get("turnId") != turn_id or params.get("serverName") != "gateway" or params.get("mode") != "form":
                            raise RuntimeError("Native elicitation binding differs")
                        meta = params.get("_meta", {})
                        ref = meta.get("yijieCallRef")
                        record = control(gateway, "GET", "/control/calls/" + str(ref))
                        if meta != {"yijieCallRef": ref, "yijieKind": "gateway_call_approval"} or record["threadId"] != thread_id or record["turnId"] != turn_id or record["tool"] != "lookup" or record["argumentsDigest"] != canonical_digest({"key": "public-synthetic-record"}):
                            raise RuntimeError("Gateway record does not match the current native execution")
                        control(gateway, "POST", "/control/decision", {"callRef": ref, "threadId": thread_id, "turnId": turn_id, "argumentsDigest": record["argumentsDigest"], "decision": decision})
                        native.send({"id": message["id"], "result": {"action": decision, "content": {} if decision == "accept" else None, "_meta": None}})
                        case["callbacks"].append({"nativeRequest": message, "trustedRecord": record, "decision": decision})
                    if message.get("method") == "turn/completed" and message.get("params", {}).get("threadId") == thread_id and message.get("params", {}).get("turn", {}).get("id") == turn_id:
                        terminal = message
                if terminal is not None:
                    break
                time.sleep(0.01)
            if terminal is None:
                raise TimeoutError("Expected ordinary turn completion unavailable")
            case["terminal"] = terminal
            case["nativeHistory"] = native.result("thread/read", {"threadId": thread_id, "includeTurns": True})
            if len(case["callbacks"]) != 1:
                raise RuntimeError("Expected exactly one Gateway-origin elicitation")
            ref = case["callbacks"][0]["trustedRecord"]["callRef"]
            case["gatewayFinal"] = control(gateway, "GET", "/control/calls/" + ref)
        report["status"] = "COMPLETED_OBSERVATIONS"
    except Exception as error:
        report["status"] = "INCOMPLETE"
        report["error"] = str(error)
    finally:
        stopped = {"normal_eof": True}
        if native is not None:
            stopped = native.close_normally()
            report["normal_shutdown"] = stopped
        gateway.close_normally()
        report["executions"] = gateway.executions
        report["local_responses_requests"] = len(gateway.provider_requests)
        report["mcp_method_counts"] = {key: gateway.http_methods.count(key) for key in sorted(set(gateway.http_methods))}
        if stopped.get("normal_eof"):
            shutil.rmtree(root)
            report["temporary_data_removed_after_exit"] = True
        else:
            report["status"] = "STOP_PENDING"
            report["temporary_data_removed_after_exit"] = False
        (args.output / "result.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        journal.stream.close()
    print(json.dumps({"status": report["status"], "error": report.get("error"), "cases": [{"decision": item["decision"], "callbacks": len(item["callbacks"]), "gatewayState": item.get("gatewayFinal", {}).get("state")} for item in report["cases"]], "executions": len(report["executions"]), "local_responses_requests": report["local_responses_requests"], "normal_shutdown": stopped}, ensure_ascii=False))
    return 0 if report["status"] == "COMPLETED_OBSERVATIONS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
