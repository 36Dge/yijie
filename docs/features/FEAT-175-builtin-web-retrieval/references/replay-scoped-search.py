"""Replay the fixed Hangzhou observations through the gateway, API, Host and desktop."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import subprocess

WORKSPACE = Path(__file__).resolve().parents[5]
CASES = {
    "three": "01a1ee76-cb26-76c3-aa7f-b7e3801b162c",
    "kimi": "01a1f14a-bb1c-7581-a98c-28b9ddd747d5",
    "minimax": "01a1f156-a569-78e2-a1d6-ae50092dbd14",
}


def read_cases(sessions):
    turns = {turn: [] for turn in CASES.values()}
    for file in sessions.rglob("*.jsonl"):
        turn = None
        with file.open() as records:
            for line in records:
                record = json.loads(line)
                event = record.get("payload") or {}
                if record["type"] == "turn_context" or event.get("type") == "task_started":
                    turn = event.get("turn_id", turn)
                if turn not in turns or event.get("type") != "mcp_tool_call_end":
                    continue
                invocation = event["invocation"]
                if invocation.get("server") == "yijie_web" and invocation.get("tool") == "kimi_web_search_pro":
                    turns[turn].append({"logical": event["call_id"], "at": record["timestamp"],
                                        "args": invocation["arguments"], "body": event["result"]["Ok"]["structuredContent"]})
    cases = {name: turns[turn] for name, turn in CASES.items()}
    identities = [json.dumps(row["args"], sort_keys=True) for row in cases["three"]]
    frequencies = Counter(identities)
    cases["three"] = [row for key, row in zip(identities, cases["three"]) if frequencies[key] == 3]
    if [len(cases[name]) for name in CASES] != [9, 20, 24]:
        raise ValueError("The fixed historical inputs are incomplete.")
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sessions", type=Path, default=WORKSPACE / "yijie-desktop/.local/demo-fast/codex-home/sessions")
    parser.add_argument("--output", type=Path, required=True, help="New local directory for private result bodies and native projections")
    args = parser.parse_args()
    if not os.environ.get("FEAT175_TEST_DATABASE_URL"):
        parser.error("Set FEAT175_TEST_DATABASE_URL to the isolated FEAT-175 localhost test database.")
    cases = read_cases(args.sessions)
    directory = args.output.resolve()
    directory.mkdir(mode=0o700, parents=True, exist_ok=False)
    (directory / "recorded.json").write_text(json.dumps(cases, ensure_ascii=False))
    build = subprocess.check_output(["cargo", "test", "--offline", "--locked", "--bin", "yijie-mcp-worker",
                                     "--no-run", "--message-format=json"], cwd=WORKSPACE / "yijie-connectors/worker", text=True)
    binary = next(value["executable"] for value in map(json.loads, build.splitlines())
                  if value.get("executable") and value["target"]["name"] == "yijie-mcp-worker")
    artifacts = WORKSPACE / "yijie-codex/.yijie/build/native-skill-marketplace-v1"
    runtime = artifacts / json.loads((artifacts / "current.json").read_text())["artifact"]
    env = {**os.environ, "SCOPED_REPLAY_RUST_TEST": binary, "SCOPED_REPLAY_DIRECTORY": str(directory),
           "YIJIE_CODEX_INTEGRATION_BINARY": str(runtime / "codex"),
           "YIJIE_CODEX_INTEGRATION_MANIFEST": str(runtime / "runtime-manifest.json")}
    for project, command in [
        ("yijie-api", ["go", "test", "-v", "-count=1", "./internal/modules/webretrieval/interfaces/http", "-run", "^TestRecordedHangzhouScopedReplay$"]),
        ("yijie-agent-host", ["go", "test", "-count=1", "./internal/session", "-run", "^TestProjectRecordedScopedSearch$"]),
        ("yijie-agent-host", ["go", "test", "-v", "-count=1", "./internal/codex", "-run", "^TestRecordedKimiSearchModelReceivesThreeTopics$"]),
        ("yijie-desktop", ["pnpm", "exec", "vitest", "run", "src/components/chat/ChatDeepSearchReceipt.test.ts"]),
    ]:
        subprocess.run(command, cwd=WORKSPACE / project, env=env, check=True)


if __name__ == "__main__":
    main()
