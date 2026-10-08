#!/usr/bin/env python3
"""Offline assertions over saved native receipts; makes no process/network calls."""
import json
from pathlib import Path

root = Path(__file__).parent
report = json.loads((root / "run-03/result.json").read_text())
wire = [json.loads(line) for line in (root / "run-03/wire.jsonl").read_text().splitlines()]
assert report["status"] == "COMPLETED_OBSERVATIONS"
assert report["empty_object_inventory"] == {"global": ["global_read"]}
assert report["explicit_empty_inventory"] == {"global": []}
assert report["alpha_inventory"] == report["alpha_recheck_inventory"] == {"alpha": ["alpha_read"], "global": []}
assert report["beta_inventory"] == {"beta": ["beta_read"], "global": []}
assert report["loaded_resume_inventory"] == report["alpha_inventory"]
assert report["unsubscribe"] == {"status": "unsubscribed"}
assert report["idle_unsubscribed_status"]["thread"]["status"]["type"] == "idle"
assert report["cold_resume_inventory"] == {"alpha": [], "beta": ["beta_read"], "global": []}
assert report["same_thread_and_prior_history"] is True
assert len(report["native_after_second_turn"]["thread"]["turns"]) == 2
requests = [row["data"] for row in wire if row["kind"] == "loopback_responses_request"]
assert len(requests) == 3
namespace_sets = [{tool["name"] for tool in request["tools"] if tool["type"] == "namespace"} for request in requests]
assert namespace_sets == [set(), {"mcp__alpha"}, {"mcp__beta"}]
assert all(turn["terminal"]["params"]["turn"]["status"] == "completed" for turn in report["synthetic_turns"])
assert report["mcp_method_counts"].get("tools/call", 0) == 0
assert all(item["normal_eof"] and item["exit_code"] == 0 for item in report["normal_shutdown"])
assert report["temporary_data_removed_after_exit"] is True
assert not Path(report["temp_root"]).exists()
assert not any("failed to read OAuth tokens from keyring" in str(row) for row in wire)
print("PASS: explicit filtering, thread isolation, loaded-resume limitation, normal cold resume, exact history preservation, actual provider tool surfaces, no tool calls, normal EOF cleanup")
