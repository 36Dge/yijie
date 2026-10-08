#!/usr/bin/env python3
"""Offline Q-SEL-05 assertions; never calls a process, credential store or URL."""
import json
from pathlib import Path

root = Path(__file__).parent / "qsel05-run-01"
report = json.loads((root / "result.json").read_text())
wire = [json.loads(line) for line in (root / "wire.jsonl").read_text().splitlines()]
assert report["status"] == "COMPLETED_OBSERVATIONS"
assert report["external_calls"] == report["real_model_calls"] == report["credentials_read_or_written"] == 0
assert report["local_responses_requests"] == 4
assert report["mcp_method_counts"]["tools/call"] == 2
assert report["mcp_method_counts"]["elicitation_response"] == 2
assert [case["decision"] for case in report["cases"]] == ["accept", "decline"]
refs = set()
for case in report["cases"]:
    assert len(case["callbacks"]) == 1
    callback = case["callbacks"][0]
    params = callback["nativeRequest"]["params"]
    registered = callback["trustedRecord"]
    assert params["threadId"] == registered["threadId"] == case["threadId"]
    assert params["turnId"] == registered["turnId"] == case["turnId"]
    assert params["serverName"] == registered["server"] == "gateway"
    assert params["mode"] == "form"
    ref = registered["callRef"]
    assert ref not in refs
    refs.add(ref)
    assert params["_meta"] == {"yijieCallRef": ref, "yijieKind": "gateway_call_approval"}
    assert registered["controlDecision"] is None  # lookup precedes the trusted decision.
    assert case["gatewayFinal"]["controlDecision"] == case["decision"]
    assert case["gatewayFinal"]["elicitationResult"]["action"] == case["decision"]
    assert case["terminal"]["params"]["turn"]["status"] == "completed"
    tools = [item for turn in case["nativeHistory"]["thread"]["turns"] for item in turn["items"] if item["type"] == "mcpToolCall"]
    assert len(tools) == 1
    assert tools[0]["tool"] == registered["tool"] == "lookup"
    assert tools[0]["arguments"] == registered["arguments"] == {"key": "public-synthetic-record"}
    assert tools[0]["status"] == ("completed" if case["decision"] == "accept" else "failed")
    events = [(i, row) for i, row in enumerate(wire) if ref in json.dumps(row)]
    positions = {kind: next(i for i, row in events if row["kind"] == kind) for kind in ["gateway_actual_call_registered", "gateway_elicitation_sent", "trusted_control_lookup", "trusted_control_decision", "gateway_tool_result"]}
    assert list(positions.values()) == sorted(positions.values())
    result = next(row["data"] for _, row in events if row["kind"] == "gateway_tool_result")
    assert result["response"]["id"] == registered["rpcCallId"]
    assert result["executed"] == (case["decision"] == "accept")
assert len(report["executions"]) == 1
assert report["executions"][0]["callRef"] == report["cases"][0]["gatewayFinal"]["callRef"]
assert report["normal_shutdown"]["normal_eof"] and report["normal_shutdown"]["exit_code"] == 0
assert report["temporary_data_removed_after_exit"] and not Path(report["temp_root"]).exists()
print("PASS: native form metadata retained, trusted call lookup/decision precedes exact tool result, accept executes once, decline executes zero, Tool/Turn facts preserved, normal EOF")
