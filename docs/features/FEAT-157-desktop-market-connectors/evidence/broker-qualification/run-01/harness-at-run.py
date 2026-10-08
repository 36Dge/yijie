#!/usr/bin/env python3
"""Fixed real Runtime + canonical-built Rust Gateway; only ordinary local data.

This is a protocol qualification driver, not the product Host grant/approval
adapter. It uses no platform accounts, paid model, process signals or binary
substitution. The worker owns MCP transport; this script only owns a local
synthetic Responses provider and the worker's private control pipe.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import queue
import secrets
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.dont_write_bytecode = True
PREVIOUS = Path(__file__).resolve().parent.parent / "runtime-qualification"
sys.path.insert(0, str(PREVIOUS))
from qualify_runtime import Journal, Native, digest, model_catalog
from qualify_elicitation import NativeWithCallbacks

CAPABILITY_ENV = "YIJIE_MARKET_RUNTIME_CAPABILITY"
REFERENCE = {"installationId": "11111111-1111-4111-8111-111111111111", "revision": 1, "generation": 1}
QUERY = "public-synthetic-record"


def identifier():
    return str(uuid.uuid4())


class SafeJournal(Journal):
    def __init__(self, path, capability):
        super().__init__(path)
        self.capability = capability
        self.leak_observed = False

    def write(self, kind, data):
        encoded = json.dumps(data, ensure_ascii=False)
        if self.capability in encoded:
            self.leak_observed = True
            data = {"omitted": "internal capability unexpectedly present"}
        super().write(kind, data)


class Runtime(NativeWithCallbacks):
    def __init__(self, binary, home, cwd, journal, capability):
        self.journal = journal
        self.incoming = queue.Queue()
        self.received = []
        self.sequence = 0
        self.stderr = []
        environment = {
            "PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "HOME": str(home.parent),
            "CODEX_HOME": str(home), "XDG_CONFIG_HOME": str(home.parent / "xdg"),
            "TMPDIR": str(home.parent), "LANG": "en_US.UTF-8",
            "NO_PROXY": "127.0.0.1,localhost", "RUST_LOG": "warn",
            CAPABILITY_ENV: capability,
        }
        self.process = subprocess.Popen(
            [str(binary), "app-server", "--listen", "stdio://", "--strict-config"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", bufsize=1, cwd=cwd, env=environment,
            close_fds=True,
        )
        journal.write("runtime_started", {"pid": self.process.pid, "binary": str(binary), "environment_keys": sorted(environment)})
        threading.Thread(target=self.read_stdout, daemon=True).start()
        threading.Thread(target=self.read_stderr, daemon=True).start()


class Worker:
    def __init__(self, manifest_path, cwd, journal, capability):
        manifest = json.loads(manifest_path.read_text())
        binary = Path(manifest["binary"])
        if not (manifest.get("candidateOnly") is True and manifest.get("qualificationOnly") is True
                and manifest.get("externalCallsEnabled") is False
                and binary.name == "market-broker-qualification"
                and digest(binary) == manifest["sha256"]
                and binary.stat().st_size == manifest["sizeBytes"]):
            raise RuntimeError("Expected canonical isolated qualification artifact")
        self.manifest = manifest
        self.manifest_digest = digest(manifest_path)
        self.journal = journal
        self.responses = queue.Queue()
        self.stderr = []
        self.process = subprocess.Popen(
            [str(binary), "--broker-control-stdio"], cwd=cwd,
            env={"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "HOME": str(cwd),
                 "TMPDIR": str(cwd), "LANG": "en_US.UTF-8", CAPABILITY_ENV: capability},
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", bufsize=1, close_fds=True,
        )
        self.reader = threading.Thread(target=self.read_stdout, daemon=True)
        self.reader.start()
        threading.Thread(target=self.read_stderr, daemon=True).start()
        journal.write("worker_started", {"pid": self.process.pid, "manifest_sha256": self.manifest_digest})

    def read_stdout(self):
        for line in self.process.stdout:
            if len(line.encode()) > 65536:
                self.responses.put(RuntimeError("Worker response exceeds frame bound"))
                return
            try:
                value = json.loads(line)
            except ValueError:
                self.responses.put(RuntimeError("Worker response is not JSON"))
                return
            self.journal.write("broker_control_response", value)
            self.responses.put(value)

    def read_stderr(self):
        for line in self.process.stderr:
            self.stderr.append(line)
            self.journal.write("worker_stderr", line.rstrip())

    def request(self, method, payload, expect_error=None):
        request_id = identifier()
        request = {"schemaVersion": 1, "requestId": request_id, "method": method, "payload": payload}
        encoded = json.dumps(request, separators=(",", ":")) + "\n"
        if len(encoded.encode()) > 65536:
            raise RuntimeError("Qualification request exceeds control bound")
        self.journal.write("broker_control_request", request)
        self.process.stdin.write(encoded)
        self.process.stdin.flush()
        value = self.responses.get(timeout=5)
        if isinstance(value, Exception):
            raise value
        if value.get("requestId") != request_id or value.get("schemaVersion") != 1:
            raise RuntimeError("Worker response identity mismatch")
        if expect_error is not None:
            if value.get("code") != expect_error:
                raise RuntimeError("Expected closed control state: " + expect_error)
            return value
        if "code" in value:
            raise RuntimeError("Control request was rejected: " + value["code"])
        return value["data"]

    def close_normally(self):
        if self.process.stdin and not self.process.stdin.closed:
            self.process.stdin.close()
        try:
            code = self.process.wait(timeout=10)
            self.reader.join(timeout=1)
            return {"normal_eof": True, "exit_code": code, "pid": self.process.pid}
        except subprocess.TimeoutExpired:
            return {"normal_eof": False, "status": "STOP_PENDING", "pid": self.process.pid}


class Provider(ThreadingHTTPServer):
    daemon_threads = True
    block_on_close = False

    def __init__(self, journal):
        super().__init__(("127.0.0.1", 0), ProviderHandler)
        self.journal = journal
        self.case = "unset"
        self.step = 0
        self.requests = []
        self.thread = threading.Thread(target=self.serve_forever, daemon=True)
        self.thread.start()

    def close_normally(self):
        self.shutdown()
        self.server_close()
        self.thread.join(timeout=5)


class ProviderHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *_):
        pass

    def reply(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        if self.path != "/v1/responses" or length > 2 * 1024 * 1024:
            self.reply(400, b"")
            return
        request = json.loads(self.rfile.read(length))
        self.server.requests.append(request)
        self.server.journal.write("local_responses_request", request)
        self.server.step += 1
        step, case = self.server.step, self.server.case
        if step == 1:
            item = {"type": "function_call", "id": f"item_{case}", "call_id": f"call_{case}",
                    "namespace": "mcp__gateway", "name": "lookup", "arguments": json.dumps({"query": QUERY})}
        elif step == 2:
            item = {"id": f"msg_{case}", "type": "message", "role": "assistant", "phase": "final_answer",
                    "status": "completed", "content": [{"type": "output_text", "text": "Local qualification finished.", "annotations": []}]}
        else:
            self.reply(400, b"")
            return
        response_id = f"response_{case}_{step}"
        events = [
            {"type": "response.created", "response": {"id": response_id, "status": "in_progress", "output": []}},
            {"type": "response.output_item.done", "output_index": 0, "item": item},
            {"type": "response.completed", "response": {"id": response_id, "status": "completed", "output": [item],
                 "usage": {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2}}},
        ]
        self.reply(200, "".join("data: " + json.dumps(value) + "\n\n" for value in events).encode())


def snapshot():
    operation = identifier()
    encoded = f"yijie.market-selection/v1\n{operation}\n1\n{REFERENCE['installationId']} 1 1\n"
    return {"schemaVersion": 1, "turnOperationId": operation, "selection": [REFERENCE],
            "selectionDigest": hashlib.sha256(encoded.encode()).hexdigest()}


def run_case(native, worker, provider, process, scope, cwd, gateway_url, decision, journal):
    provider.case, provider.step = decision, 0
    started = native.result("thread/start", {
        "cwd": str(cwd), "model": "qualification-text", "modelProvider": "qualification",
        "approvalPolicy": "on-request", "approvalsReviewer": "user", "sandbox": "read-only",
        "ephemeral": False, "baseInstructions": "Use the provided local synthetic lookup once.",
    })
    thread_id = started["thread"]["id"]
    prepare = {"operationId": identifier(), "context": {"process": process, "scope": scope,
               "agentSessionId": identifier(), "nativeThreadId": thread_id}, "snapshot": snapshot(), "ttlMs": 120000}
    prepared = worker.request("prepare", prepare)
    binding = prepared["binding"]
    duplicate = worker.request("prepare", prepare)
    if duplicate["binding"] != binding or duplicate["remainingTtlMs"] > prepared["remainingTtlMs"]:
        raise RuntimeError("Prepare replay changed capability or extended lease")
    native.result("thread/unsubscribe", {"threadId": thread_id})
    # Fixed Runtime ignores config on loaded resume; perform a normal cold resume.
    native.result("thread/resume", {
        "threadId": thread_id, "cwd": str(cwd), "model": "qualification-text", "modelProvider": "qualification",
        "approvalPolicy": "on-request", "approvalsReviewer": "user", "sandbox": "read-only",
        "config": {"mcp_servers": {"gateway": {
            "url": gateway_url + "/" + binding["capabilityRef"], "bearer_token_env_var": CAPABILITY_ENV,
            "enabled": True, "enabled_tools": ["lookup"], "default_tools_approval_mode": "auto",
            "startup_timeout_sec": 5, "tool_timeout_sec": 20,
        }}},
    })
    turn = native.result("turn/start", {"threadId": thread_id, "input": [
        {"type": "text", "text": "Use the local synthetic lookup once for the public synthetic record."}]})
    turn_id = turn["turn"]["id"]
    bound = worker.request("bind_turn", {"operationId": identifier(), "binding": binding,
        "expectedRevision": prepared["revision"], "nativeTurnId": turn_id})
    case = {"decision": decision, "threadId": thread_id, "turnId": turn_id,
            "binding": binding, "callbacks": [], "prepareReplayPreserved": True}
    seen = set()
    end = time.monotonic() + 25
    while time.monotonic() < end:
        for message in list(native.received):
            params = message.get("params", {})
            if (message.get("method") == "mcpServer/elicitation/request"
                    and params.get("threadId") == thread_id and message.get("id") not in seen):
                seen.add(message["id"])
                meta = params.get("_meta", {})
                ref = meta.get("yijieMarketCallRef")
                if (params.get("turnId") != turn_id or params.get("serverName") != "gateway"
                        or params.get("mode") != "form"
                        or meta != {"yijieMarketCallRef": ref, "yijieKind": "gateway_call_approval"}):
                    raise RuntimeError("Native elicitation correlation differs")
                query = {"binding": binding, "nativeTurnId": turn_id, "callRef": ref}
                pending = worker.request("pending_call", query)
                identity = pending["identity"]
                if (identity["binding"] != binding or identity["nativeTurnId"] != turn_id
                        or identity["callRef"] != ref or identity["reference"] != REFERENCE
                        or identity["serviceId"] != "market-qualification" or identity["toolName"] != "lookup"
                        or identity["argsEncoding"] != "worker-json-v1" or pending["state"] != "pending"):
                    raise RuntimeError("Trusted call does not match the actual native Turn")
                # This qualification supplies an ordinary synthetic review decision.
                # Product Host approval authority is intentionally not claimed here.
                payload = {"operationId": identifier(), "identity": identity,
                           "expectedRevision": pending["revision"], "approvalRef": identifier(),
                           "decisionId": identifier(), "decision": "approve_once" if decision == "accept" else "reject"}
                decided = worker.request("decide_call", payload)
                replay = worker.request("decide_call", payload)
                if replay != decided:
                    raise RuntimeError("Decision receipt replay differs")
                native.send({"id": message["id"], "result": {"action": decision,
                    "content": {} if decision == "accept" else None, "_meta": None}})
                case["callbacks"].append({"request": message, "pending": pending, "decisionReceipt": decided})
                case["callQuery"] = query
            if (message.get("method") == "turn/completed" and params.get("threadId") == thread_id
                    and params.get("turn", {}).get("id") == turn_id):
                case["terminal"] = message
        if "terminal" in case:
            break
        time.sleep(0.01)
    if "terminal" not in case or len(case["callbacks"]) != 1 or provider.step != 2:
        raise RuntimeError("Expected one actual lookup, one elicitation and ordinary completed Turn")
    case["callFinal"] = worker.request("pending_call", case.pop("callQuery"))
    expected = "consumed" if decision == "accept" else "rejected"
    if case["callFinal"]["state"] != expected:
        raise RuntimeError("Unexpected final call admission state")
    completed_items = [message["params"]["item"] for message in native.received
                       if message.get("method") == "item/completed"
                       and message.get("params", {}).get("threadId") == thread_id
                       and message.get("params", {}).get("turnId") == turn_id
                       and message.get("params", {}).get("item", {}).get("type") == "mcpToolCall"]
    if len(completed_items) != 1:
        raise RuntimeError("Missing unambiguous actual native Tool Item")
    case["nativeTool"] = completed_items[0]
    case["nativeHistory"] = native.result("thread/read", {"threadId": thread_id, "includeTurns": True})
    case["revoked"] = worker.request("revoke", {"operationId": identifier(), "binding": binding,
        "expectedRevision": bound["revision"], "reason": "turn_terminal"})
    case["reprepare"] = worker.request("prepare", prepare, expect_error="lease_revoked")
    if case["revoked"]["state"] != "revoked":
        raise RuntimeError("Terminal revoke not observed")
    journal.write("case_completed", {"decision": decision, "turnId": turn_id, "callState": expected})
    return case


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--worker-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    shutil.copy2(Path(__file__), args.output / "harness-at-run.py")
    capability = secrets.token_hex(32)
    journal = SafeJournal(args.output / "wire.jsonl", capability)
    root = Path(tempfile.mkdtemp(prefix="feat157-rust-gateway-")).resolve()
    home, cwd = root / "codex-home", root / "workspace"
    home.mkdir()
    cwd.mkdir()
    report = {"status": "NOT_RUN", "temp_root": str(root), "external_calls": 0,
              "real_model_calls": 0, "platform_credentials_read_or_written": 0, "cases": [],
              "harness_sha256": digest(Path(__file__)), "reused_harness_sources": {
                  path.name: digest(path) for path in (PREVIOUS / "qualify_runtime.py", PREVIOUS / "qualify_elicitation.py")}}
    native = worker = provider = None
    try:
        lock_path = args.workspace / "yijie-desktop/contracts/runtime-chat-models.candidate.json"
        lock = json.loads(lock_path.read_text())
        artifact = args.workspace / "yijie-codex/.yijie/build/chat-models-stream-args/aarch64-apple-darwin"
        if (digest(artifact / "codex") != lock["runtime_artifact"]["sha256"]
                or digest(artifact / "runtime-manifest.json") != lock["runtime_manifest_sha256"]):
            raise RuntimeError("Fixed Runtime artifact differs")
        report.update({"runtime_artifact": lock["runtime_artifact"], "runtime_manifest_sha256": lock["runtime_manifest_sha256"]})
        worker = Worker(args.worker_manifest, root, journal, capability)
        report["worker_manifest"] = worker.manifest
        report["worker_manifest_sha256"] = worker.manifest_digest
        process = {"hostInstanceId": identifier(), "runtimeGeneration": identifier()}
        initialized = worker.request("initialize", {"operationId": identifier(), "process": process})
        if initialized["process"] != process or initialized["externalCallsEnabled"] is not False:
            raise RuntimeError("Unexpected worker generation or qualification")
        provider = Provider(journal)
        origin = f"http://127.0.0.1:{provider.server_address[1]}"
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
[shell_environment_policy]
inherit = "core"
exclude = ["{CAPABILITY_ENV}"]
set = {{}}
[model_providers.qualification]
name = "Local protocol qualification"
base_url = "{origin}/v1"
wire_api = "responses"
requires_openai_auth = false
supports_websockets = false
request_max_retries = 0
stream_max_retries = 0
'''
        (home / "config.toml").write_text(config)
        (args.output / "synthetic-config.toml").write_text(config)
        native = Runtime(artifact / "codex", home, cwd, journal, capability)
        native.result("initialize", {"clientInfo": {"name": "yijie_feat157_rust_gateway", "version": "0.1.0"}, "capabilities": {"experimentalApi": False}})
        native.send({"method": "initialized", "params": {}})
        scope = {"ownerUserId": identifier(), "tenantId": identifier(), "nativeProcessEpoch": identifier(),
                 "authorizationRevision": 1, "authorizationExpiresAtUnixMs": int(time.time() * 1000) + 240000}
        for decision in ("accept", "decline"):
            report["cases"].append(run_case(native, worker, provider, process, scope, cwd, initialized["gatewayUrl"], decision, journal))
        report["shutdown_receipt"] = worker.request("shutdown", {"operationId": identifier(), "process": process, "reason": "owner_shutdown"})
        report["status"] = "COMPLETED_OBSERVATIONS"
    except Exception as error:
        report["status"] = "INCOMPLETE"
        # Exceptions contain only qualification-generated metadata or fixed error codes.
        report["error"] = str(error).replace(capability, "[omitted]")
    finally:
        native_stop = native.close_normally() if native else {"normal_eof": True, "not_started": True}
        worker_stop = worker.close_normally() if worker else {"normal_eof": True, "not_started": True}
        report["normal_shutdown"] = {"runtime": native_stop, "worker": worker_stop}
        if any(value.get("exit_code", 0) != 0 for value in (native_stop, worker_stop)):
            report["status"] = "CHECK_FAILED"
        if provider:
            report["local_responses_requests"] = len(provider.requests)
            provider.close_normally()
        report["internal_capability_in_observed_wire"] = journal.leak_observed
        marker_files = []
        for path in root.rglob("*"):
            if path.is_file() and capability.encode() in path.read_bytes():
                marker_files.append(str(path.relative_to(root)))
        report["internal_capability_in_temporary_files"] = marker_files
        if marker_files or journal.leak_observed:
            report["status"] = "CHECK_FAILED"
        stopped = native_stop.get("normal_eof") and worker_stop.get("normal_eof")
        report["temporary_data_removed_after_exit"] = bool(stopped)
        if stopped:
            shutil.rmtree(root)
        else:
            report["status"] = "STOP_PENDING"
        (args.output / "result.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        journal.stream.close()
    print(json.dumps({"status": report["status"], "error": report.get("error"),
        "cases": [{"decision": value["decision"], "call_state": value["callFinal"]["state"]} for value in report["cases"]],
        "local_responses_requests": report.get("local_responses_requests", 0), "normal_shutdown": report["normal_shutdown"]}, ensure_ascii=False))
    return 0 if report["status"] == "COMPLETED_OBSERVATIONS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
