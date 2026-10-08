#!/usr/bin/env python3
"""Normal local carrier qualification. Synthetic marker, no credential IO.

The fixed Runtime performs one ordinary environment-presence check and one MCP
lookup per case. The marker lives only in harness/Runtime memory. Neither the
command nor the journal prints it; no full environment is requested. The local
Responses service is synthetic and is not a paid or external model.
"""
from __future__ import annotations

import argparse
import json
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "runtime-qualification"))
from qualify_runtime import Journal, Native, digest, model_catalog

MARKER_ENV = "YIJIE_MARKET_QUALIFICATION_TOKEN"
COMMAND = ('if [ -z "${' + MARKER_ENV + '+x}" ]; then '
           'printf "MARKER_ABSENT\\n"; else printf "MARKER_PRESENT\\n"; fi')


class SafeJournal(Journal):
    def __init__(self, path, marker):
        super().__init__(path)
        self.marker = marker
        self.marker_observations = 0

    def write(self, kind, data):
        raw = json.dumps(data, ensure_ascii=False)
        if self.marker in raw:
            self.marker_observations += 1
            data = json.loads(raw.replace(self.marker, "[QUALIFICATION_MARKER_REMOVED]"))
        super().write(kind, data)


class OwnedRuntime(Native):
    def __init__(self, binary, home, cwd, journal, marker):
        self.journal, self.incoming, self.received = journal, queue.Queue(), []
        self.sequence, self.stderr = 0, []
        env = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "HOME": str(home.parent),
               "CODEX_HOME": str(home), "XDG_CONFIG_HOME": str(home.parent / "xdg"),
               "TMPDIR": str(home.parent), "LANG": "en_US.UTF-8", "RUST_LOG": "warn",
               "NO_PROXY": "127.0.0.1,localhost", MARKER_ENV: marker}
        self.process = subprocess.Popen(
            [str(binary), "app-server", "--listen", "stdio://", "--strict-config"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", bufsize=1, cwd=cwd, env=env)
        journal.write("runtime_started", {"pid": self.process.pid, "environment_keys": sorted(env)})
        threading.Thread(target=self.read_stdout, daemon=True).start()
        threading.Thread(target=self.read_stderr, daemon=True).start()


class LocalService(ThreadingHTTPServer):
    daemon_threads = True
    block_on_close = False

    def __init__(self, journal, marker, tool):
        super().__init__(("127.0.0.1", 0), Handler)
        self.journal, self.marker, self.tool = journal, marker, tool
        self.provider_requests, self.mcp_observations = [], []
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

    def reply(self, status, data=None, content_type="application/json"):
        raw = b"" if data is None else data if isinstance(data, bytes) else json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Connection", "close")
        self.end_headers()
        if raw:
            self.wfile.write(raw)

    def do_GET(self):
        self.reply(405)

    def do_DELETE(self):
        self.reply(204)

    def provider(self, body):
        self.server.provider_requests.append(body)
        self.server.journal.write("local_responses_request", body)
        step = len(self.server.provider_requests)
        response_id = f"local_{self.server.tool}_{step}"
        if step == 1:
            args = {"command": COMMAND, "login": False, "timeout_ms": 1000} if self.server.tool == "shell_command" else {"cmd": COMMAND, "login": False, "yield_time_ms": 1000, "max_output_tokens": 100}
            item = {"type": "function_call", "id": "local_command", "call_id": "local_command_call",
                    "name": self.server.tool, "arguments": json.dumps(args)}
        elif step == 2:
            item = {"type": "function_call", "id": "local_lookup", "call_id": "local_lookup_call",
                    "namespace": "mcp__gateway", "name": "lookup", "arguments": "{}"}
        elif step == 3:
            item = {"type": "message", "id": "local_final", "role": "assistant", "phase": "final_answer",
                    "status": "completed", "content": [{"type": "output_text", "text": "Local carrier checks finished.", "annotations": []}]}
        else:
            self.reply(400, {"error": {"message": "Local qualification request limit reached"}})
            return
        events = [
            {"type": "response.created", "response": {"id": response_id, "status": "in_progress", "output": []}},
            {"type": "response.output_item.done", "output_index": 0, "item": item},
            {"type": "response.completed", "response": {"id": response_id, "status": "completed", "output": [item], "usage": {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2}}},
        ]
        self.reply(200, "".join("data: " + json.dumps(event) + "\n\n" for event in events).encode(), "text/event-stream")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length > 2 * 1024 * 1024:
            self.reply(413)
            return
        body = json.loads(self.rfile.read(length))
        if self.path == "/v1/responses":
            self.provider(body)
            return
        if self.path != "/mcp/gateway":
            self.reply(404)
            return
        authorized = self.headers.get("Authorization") == "Bearer " + self.server.marker
        observation = {"method": body.get("method"), "bearer_matches_marker": authorized}
        self.server.mcp_observations.append(observation)
        self.server.journal.write("mcp_bearer_check", observation)
        if not authorized:
            self.reply(403)
            return
        if "id" not in body:
            self.reply(202)
            return
        method = body.get("method")
        if method == "initialize":
            result = {"protocolVersion": body["params"]["protocolVersion"], "capabilities": {"tools": {}}, "serverInfo": {"name": "local-carrier", "version": "1.0.0"}}
        elif method == "tools/list":
            result = {"tools": [{"name": "lookup", "description": "Read a fixed public local value.", "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}, "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}}]}
        elif method == "tools/call":
            result = {"content": [{"type": "text", "text": "public-local-carrier-value"}], "isError": False}
        elif method in ("resources/list", "resources/templates/list"):
            result = {"resources" if method == "resources/list" else "resourceTemplates": []}
        elif method == "ping":
            result = {}
        else:
            self.reply(200, {"jsonrpc": "2.0", "id": body["id"], "error": {"code": -32601, "message": "Not used by local qualification"}})
            return
        self.reply(200, {"jsonrpc": "2.0", "id": body["id"], "result": result})


def run_case(workspace, output, tool, binary):
    output.mkdir()
    marker = uuid.uuid4().hex + uuid.uuid4().hex
    journal = SafeJournal(output / "wire.jsonl", marker)
    root = Path(tempfile.mkdtemp(prefix="feat157-carrier-")).resolve()
    home, cwd = root / "codex-home", root / "workspace"
    home.mkdir()
    cwd.mkdir()
    service = LocalService(journal, marker, tool)
    base = f"http://127.0.0.1:{service.server_address[1]}"
    catalog = model_catalog()
    catalog["models"][0]["shell_type"] = "shell_command" if tool == "shell_command" else "unified_exec"
    catalog["models"][0]["base_instructions"] = "Perform only the ordinary local qualification checks."
    (home / "catalog.json").write_text(json.dumps(catalog))
    config = f'''model = "qualification-text"
model_provider = "qualification"
model_catalog_json = {json.dumps(str(home / "catalog.json"))}
check_for_update_on_startup = false
web_search = "disabled"
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
js_repl = false
shell_tool = true
unified_exec = {str(tool == "exec_command").lower()}
[shell_environment_policy]
inherit = "core"
exclude = ["{MARKER_ENV}", "YIJIE_FEAT144_SORFTIME_ACCOUNT_SK", "YIJIE_FEAT144_SORFTIME_ENABLED", "MINIMAX_API_KEY", "KIMI_API_KEY", "MOONSHOT_API_KEY", "YIJIE_KIMI_API_KEY", "YIJIE_KIMI_API_KEY_FILE"]
set = {{}}
[model_providers.qualification]
name = "Local synthetic carrier qualification"
base_url = "{base}/v1"
wire_api = "responses"
requires_openai_auth = false
supports_websockets = false
request_max_retries = 0
stream_max_retries = 0
[mcp_servers.gateway]
url = "{base}/mcp/gateway"
bearer_token_env_var = "{MARKER_ENV}"
enabled = true
enabled_tools = ["lookup"]
default_tools_approval_mode = "auto"
startup_timeout_sec = 5
tool_timeout_sec = 5
'''
    (home / "config.toml").write_text(config)
    (output / "synthetic-config.toml").write_text(config)
    report = {"tool": tool, "temp_root": str(root), "status": "INCOMPLETE"}
    native = None
    stopped = {"normal_eof": True}
    try:
        native = OwnedRuntime(binary, home, cwd, journal, marker)
        native.result("initialize", {"clientInfo": {"name": "yijie_carrier_qualification", "version": "0.1.0"}, "capabilities": {"experimentalApi": False}})
        native.send({"method": "initialized", "params": {}})
        effective = native.result("config/read", {"includeLayers": False})
        report["effective_environment_policy"] = effective["config"]["shell_environment_policy"]
        start = native.result("thread/start", {"model": "qualification-text", "modelProvider": "qualification", "cwd": str(cwd), "approvalPolicy": "never", "sandbox": "read-only", "ephemeral": False})
        tid = start["thread"]["id"]
        turn = native.result("turn/start", {"threadId": tid, "input": [{"type": "text", "text": "Perform the ordinary local carrier qualification checks."}]})
        turn_id = turn["turn"]["id"]
        terminal = native.wait_notification(lambda msg: msg.get("method") == "turn/completed" and msg.get("params", {}).get("threadId") == tid and msg["params"]["turn"]["id"] == turn_id)
        history = native.result("thread/read", {"threadId": tid, "includeTurns": True})
        items = history["thread"]["turns"][0]["items"]
        # The pinned cold-history projection omits these command items. Observe
        # the actual completed notification bound to this thread/turn/item;
        # do not reconstruct a command item from model-visible text.
        commands = [msg["params"]["item"] for msg in native.received
                    if msg.get("method") == "item/completed"
                    and msg.get("params", {}).get("threadId") == tid
                    and msg["params"].get("turnId") == turn_id
                    and msg["params"].get("item", {}).get("type") == "commandExecution"
                    and msg["params"]["item"].get("id") == "local_command_call"]
        lookups = [item for item in items if item.get("type") == "mcpToolCall"]
        report["native_terminal"] = terminal["params"]["turn"]["status"]
        report["cold_history_command_count"] = sum(item.get("type") == "commandExecution" for item in items)
        report["command_observation_source"] = "actual item/completed with exact native thread, turn and call item"
        report["command_observations"] = [{"status": item.get("status"), "exitCode": item.get("exitCode"), "output": item.get("aggregatedOutput")} for item in commands]
        report["lookup_observations"] = [{"status": item.get("status"), "server": item.get("server"), "tool": item.get("tool")} for item in lookups]
        report["environment_marker_absent"] = len(commands) == 1 and commands[0].get("exitCode") == 0 and (commands[0].get("aggregatedOutput") or "").strip() == "MARKER_ABSENT"
        report["mcp_lookup_completed"] = len(lookups) == 1 and lookups[0].get("status") == "completed"
        report["status"] = "OBSERVATIONS_COMPLETE"
        native.result("thread/unsubscribe", {"threadId": tid})
    except Exception as error:
        # Native exception text may include input; remove marker before saving.
        report["error"] = str(error).replace(marker, "[QUALIFICATION_MARKER_REMOVED]")
    finally:
        if native:
            stopped = native.close_normally()
            report["native_output_marker_absent"] = marker not in json.dumps(native.received) and marker not in "".join(native.stderr)
        report["normal_shutdown"] = stopped
        report["mcp_observations"] = service.mcp_observations
        report["mcp_bearer_observed"] = bool(service.mcp_observations) and all(x["bearer_matches_marker"] for x in service.mcp_observations)
        report["synthetic_provider_requests"] = len(service.provider_requests)
        report["provider_input_marker_absent"] = marker not in json.dumps(service.provider_requests)
        service.close_normally()
        scanned, hits = 0, []
        for path in root.rglob("*"):
            if path.is_file():
                scanned += 1
                if marker.encode() in path.read_bytes():
                    hits.append(str(path.relative_to(root)))
        report["temporary_files_scanned"] = scanned
        report["temporary_files_containing_marker"] = hits
        report["journal_marker_observations"] = journal.marker_observations
        if stopped.get("normal_eof"):
            shutil.rmtree(root)
            report["temporary_data_removed_after_exit"] = True
        else:
            report["status"] = "STOP_PENDING"
        if report["status"] == "OBSERVATIONS_COMPLETE":
            report["status"] = "PASS" if all(report.get(key) for key in ["environment_marker_absent", "mcp_lookup_completed", "mcp_bearer_observed", "native_output_marker_absent", "provider_input_marker_absent"]) and not hits and not journal.marker_observations and stopped.get("exit_code") == 0 else "CHECK_FAILED"
        journal.stream.close()
        (output / "result.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(exist_ok=False)
    lock = json.loads((args.workspace / "yijie-desktop/contracts/runtime-chat-models.candidate.json").read_text())
    artifact = args.workspace / "yijie-codex/.yijie/build/chat-models-stream-args/aarch64-apple-darwin"
    binary = artifact / "codex"
    assert digest(binary) == lock["runtime_artifact"]["sha256"]
    assert digest(artifact / "runtime-manifest.json") == lock["runtime_manifest_sha256"]
    report = {"harness_sha256": digest(Path(__file__)), "runtime_artifact": lock["runtime_artifact"], "runtime_manifest_sha256": lock["runtime_manifest_sha256"], "external_calls": 0, "real_model_calls": 0, "real_credentials_read_or_written": 0, "force_kills": 0, "cases": []}
    for tool in ["shell_command", "exec_command"]:
        case = run_case(args.workspace, args.output / tool, tool, binary)
        report["cases"].append(case)
        if not case.get("normal_shutdown", {}).get("normal_eof"):
            break
    report["status"] = "PASS" if len(report["cases"]) == 2 and all(case["status"] == "PASS" for case in report["cases"]) else "INCOMPLETE"
    (args.output / "result.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "cases": [{"tool": case["tool"], "status": case["status"], "error": case.get("error"), "command_observations": case.get("command_observations"), "normal_shutdown": case.get("normal_shutdown")} for case in report["cases"]]}))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
