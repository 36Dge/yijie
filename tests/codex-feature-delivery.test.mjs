import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import {
  loadAndValidateFeaturePackage,
  validateClaimedFeaturePackage,
  validateFailureLedgerEvolution,
  validateFeaturePackageEvolution,
  validateFeatureData,
} from "../docs/dev/codex-feature-delivery/scripts/validate-feature-package.mjs";
import { auditFeaturePackages } from "../docs/dev/codex-feature-delivery/scripts/audit-feature-packages.mjs";

const SHA_A = "a".repeat(40);
const SHA_B = "b".repeat(40);
const DIGEST_B = "b".repeat(64);
const PACKAGE_ROOT = path.resolve("docs/dev/codex-feature-delivery");
const VALID_EVIDENCE_IDS = [
  "EV-SLICE-001",
  "EV-G2V-001",
  "EV-HQ-POSITIVE",
  "EV-HQ-PRODUCT",
  "EV-HQ-HARNESS",
  "EV-HQ-PLATFORM",
  "EV-HQ-GATE",
  "EV-HQ-TIMEOUT",
  "EV-HQ-CLEANUP",
  "EV-HQ-CONTENT-FREE",
  "EV-E2E-CORE",
  "EV-E2E-A11Y",
  "EV-E2E-TEARDOWN",
  "EV-TCONF-001",
];

function ref(id) {
  return `08-verification-report.md#${id}`;
}

function commit(repository, fullSha = SHA_A) {
  return { repository, full_sha: fullSha };
}

function verificationReport() {
  return VALID_EVIDENCE_IDS.map((id) => `<!-- evidence: ${id} -->\n### Evidence ${id}\nPASS`).join(
    "\n\n",
  );
}

const temporalReport = "FLOW-LIVE-001 FLOW-REPLAY-001 TINV-001 TCONF-001\n";

function evidence(required = true) {
  return required
    ? {
        required: true,
        status: "PASS",
        command: "pnpm test -- slice",
        environment: "local locked toolchain",
        exit_code: 0,
        verified_at: "2026-08-23T10:30:00+08:00",
        refs: [ref("EV-SLICE-001")],
        reason: "required",
        exception: { owner: "N/A", approved_at: "N/A", reason: "N/A" },
      }
    : {
        required: false,
        status: "N/A",
        refs: [],
        reason: "not applicable by owner decision",
        exception: {
          owner: "Technical Owner",
          approved_at: "2026-08-23T10:00:00+08:00",
          reason: "not applicable by owner decision",
        },
      };
}

function failureAttempt(index) {
  return {
    run_id: `RUN-${index}`,
    occurred_at: `2026-08-23T10:0${index}:00+08:00`,
    result: "FAIL",
    failure_class: "harness_failure",
    failure_code: "runtime_failed",
    checkpoint: "post_lifecycle",
    evidence_ref: ref(`EV-FAIL-${index}`),
  };
}

function trippedIncident(state = "rca_required") {
  return {
    id: "INC-001",
    slice_id: "S1",
    gate_id: "G3",
    evidence_id: "EV-SLICE-001",
    failure_class: "harness_failure",
    failure_code: "runtime_failed",
    checkpoint: "post_lifecycle",
    fingerprint: "S1|G3|EV-SLICE-001|harness_failure|runtime_failed|post_lifecycle",
    attempts: [failureAttempt(1), failureAttempt(2), failureAttempt(3)],
    rca_cycles: [],
    state,
  };
}

function validV2() {
  return {
    schema_version: 2,
    feature: {
      id: "FEAT-999",
      slug: "governance-v2-test",
      title: "Governance v2 test",
      status: "active",
      created_at: "2026-08-23",
      requirement_owner: "Product Owner",
      technical_owner: "Technical Owner",
      reviewer: "Reviewer",
      release_owner: "Release Owner",
    },
    scope: {
      risk_level: "high",
      data_classification: "internal",
      contract_impact: "none",
      database_change: "none",
      persistence_change: "none",
      runtime_change: "runtime",
      auth_permission_change: "none",
      user_workflow_change: "user_visible",
      ui_change: "interactive",
      ai_behavior_change: "none",
    },
    repositories: ["desktop"],
    immutable_references: {
      baseline_commits: [],
      contracts: [],
      fixtures: [],
      release_artifacts: [],
    },
    gates: {
      G0_intake: "pass",
      G1_design_ready: "pass",
      G2_implementation_ready: "pass",
      G2A_contract_ready: "not_applicable",
      G2V_vertical_feasibility: "pass",
      G4_code_complete: "pass",
      G5_production_ready: "pending",
      G6_delivery_complete: "pending",
    },
    gate_reasons: {
      G2A: "contract impact is none",
      G2V: "required by runtime and user-visible workflow",
    },
    temporal_contract_matrix: {
      required: true,
      applicability_reason: "cross-boundary runtime flow",
      exception: { owner: "N/A", approved_at: "N/A", reason: "N/A" },
      phases: Object.fromEntries(
        ["producer", "persistence", "notification", "replay", "terminal", "cleanup"].map(
          (phase) => [phase, { status: "required", reason: `${phase} is part of the flow` }],
        ),
      ),
      phase_exceptions: {},
      scenarios: [
        {
          id: "FLOW-LIVE-001",
          ordered_phases: ["producer", "persistence", "notification", "terminal", "cleanup"],
        },
        { id: "FLOW-REPLAY-001", ordered_phases: ["persistence", "replay", "cleanup"] },
      ],
      invariants: [
        {
          id: "TINV-001",
          statement: "terminal follows durable publication",
          scenario_ids: ["FLOW-LIVE-001", "FLOW-REPLAY-001"],
          slice_ids: ["S1"],
          executable_tests: ["TCONF-001"],
        },
      ],
      executable_tests: [
        {
          id: "TCONF-001",
          required: true,
          repository: "desktop",
          command: "pnpm test -- temporal-conformance",
          slice_id: "S1",
          status: "PASS",
          exit_code: 0,
          verified_at: "2026-08-23T10:45:00+08:00",
          commits: [commit("desktop")],
          evidence_ref: ref("EV-TCONF-001"),
          exception: { owner: "N/A", approved_at: "N/A", reason: "N/A" },
        },
      ],
    },
    vertical_feasibility: {
      required: true,
      applicability_reason: "runtime and user-visible workflow",
      exception: { owner: "N/A", approved_at: "N/A", reason: "N/A" },
      harness_id: "H-VERTICAL-001",
      participating_repositories: ["desktop"],
      platform: "macOS Tauri release",
      production_bootstrap: true,
      representative_data: "bounded synthetic fixture",
      critical_path: "production app to durable result",
      evidence: {
        commits: [commit("desktop")],
        command: "./scripts/run-vertical.sh",
        environment: "macOS 15 Tauri release",
        exit_code: 0,
        status: "PASS",
        verified_at: "2026-08-23T10:00:00+08:00",
        harness: { id: "H-VERTICAL-001", commit: SHA_A, digest: DIGEST_B },
        platform: "macOS Tauri release",
        production_bootstrap: true,
        contract_refs: [],
        fixture_refs: [],
        refs: [ref("EV-G2V-001")],
      },
    },
    runtime_harnesses: [
      {
        id: "H-VERTICAL-001",
        purpose: "production vertical",
        commit: SHA_A,
        digest: DIGEST_B,
        default_enabled: false,
        real_platform: "macOS Tauri release",
        production_bootstrap: true,
        representative_data: "bounded synthetic fixture",
        failure_classes: [
          "product_failure",
          "harness_failure",
          "platform_failure",
          "gate_failure",
        ],
        qualification: {
          status: "PASS",
          verified_at: "2026-08-23T09:00:00+08:00",
          command: "./scripts/qualify-harness.sh",
          environment: "macOS 15 Tauri release",
          exit_code: 0,
          positive_control: { status: "PASS", evidence_ref: ref("EV-HQ-POSITIVE") },
          negative_controls: {
            product_failure: {
              status: "PASS",
              observed_class: "product_failure",
              evidence_ref: ref("EV-HQ-PRODUCT"),
            },
            harness_failure: {
              status: "PASS",
              observed_class: "harness_failure",
              evidence_ref: ref("EV-HQ-HARNESS"),
            },
            platform_failure: {
              status: "PASS",
              observed_class: "platform_failure",
              evidence_ref: ref("EV-HQ-PLATFORM"),
            },
            gate_failure: {
              status: "PASS",
              observed_class: "gate_failure",
              evidence_ref: ref("EV-HQ-GATE"),
            },
          },
          timeout_control: { status: "PASS", evidence_ref: ref("EV-HQ-TIMEOUT") },
          cleanup_control: { status: "PASS", evidence_ref: ref("EV-HQ-CLEANUP") },
          content_free_verdict: { status: "PASS", evidence_ref: ref("EV-HQ-CONTENT-FREE") },
        },
      },
    ],
    slices: [
      {
        id: "S1",
        intent: "one vertical result",
        required: true,
        prerequisites: ["G2V"],
        commits: [commit("desktop")],
        exception: { owner: "N/A", approved_at: "N/A", reason: "N/A" },
        local_evidence: evidence(),
        boundary_evidence: evidence(),
        vertical_evidence: evidence(),
        freshness: {
          verified_at: "2026-08-23T11:00:00+08:00",
          commits: [commit("desktop")],
          contract_refs: [],
          fixture_refs: [],
          harness: { id: "H-VERTICAL-001", commit: SHA_A, digest: DIGEST_B },
          platform: "macOS Tauri release",
          production_bootstrap: true,
          invalidation_rule: "rerun after any covered reference changes",
        },
        status: "pass",
        status_reason: "all required evidence passed",
      },
    ],
    final_e2e: {
      core_vertical: {
        required: true,
        reason: "user workflow",
        status: "PASS",
        command: "./scripts/run-core.sh",
        environment: "macOS 15 Tauri release",
        exit_code: 0,
        verified_at: "2026-08-23T12:00:00+08:00",
        commits: [commit("desktop")],
        contract_refs: [],
        fixture_refs: [],
        harness: { id: "H-VERTICAL-001", commit: SHA_A, digest: DIGEST_B },
        platform: "macOS Tauri release",
        production_bootstrap: true,
        evidence_refs: [ref("EV-E2E-CORE")],
        exception: { owner: "N/A", approved_at: "N/A", reason: "N/A" },
      },
      accessibility_visual: {
        required: true,
        reason: "user interface",
        status: "PASS",
        command: "./scripts/run-a11y-visual.sh",
        environment: "macOS 15 Tauri release",
        exit_code: 0,
        verified_at: "2026-08-23T12:00:00+08:00",
        commits: [commit("desktop")],
        contract_refs: [],
        fixture_refs: [],
        harness: { id: "H-VERTICAL-001", commit: SHA_A, digest: DIGEST_B },
        platform: "macOS Tauri release",
        production_bootstrap: true,
        evidence_refs: [ref("EV-E2E-A11Y")],
        exception: { owner: "N/A", approved_at: "N/A", reason: "N/A" },
      },
      teardown: {
        required: true,
        reason: "runtime resources",
        status: "PASS",
        command: "./scripts/run-teardown.sh",
        environment: "macOS 15 Tauri release",
        exit_code: 0,
        verified_at: "2026-08-23T12:00:00+08:00",
        commits: [commit("desktop")],
        contract_refs: [],
        fixture_refs: [],
        harness: { id: "H-VERTICAL-001", commit: SHA_A, digest: DIGEST_B },
        platform: "macOS Tauri release",
        production_bootstrap: true,
        evidence_refs: [ref("EV-E2E-TEARDOWN")],
        exception: { owner: "N/A", approved_at: "N/A", reason: "N/A" },
      },
    },
    failure_circuit_breaker: {
      same_failure_threshold: 3,
      policy: "trip at the third equivalent failure",
      incidents: [],
    },
    documents: {
      temporal_contract: "04A-temporal-contract-matrix.md",
      verification: "08-verification-report.md",
    },
  };
}

function validProductionV3() {
  return {
    ...validV2(),
    schema_version: 3,
    delivery_profile: "production_hardened",
    exposure: "public",
  };
}

function validDemoV3(exposure = "local") {
  const publicRequired = exposure === "public";
  return {
    schema_version: 3,
    delivery_profile: "demo_fast",
    exposure,
    feature: {
      id: "FEAT-999",
      slug: "demo-fast-test",
      title: "Demo fast test",
      status: "usable",
      created_at: "2026-08-23",
      requirement_owner: "Product Owner",
      technical_owner: "Technical Owner",
      reviewer: "Reviewer",
      release_owner: "Release Owner",
    },
    scope: {
      risk_level: "medium",
      data_classification: "internal",
      contract_impact: "none",
      database_change: "none",
      persistence_change: "none",
      runtime_change: "runtime",
      auth_permission_change: "none",
      user_workflow_change: "user_visible",
      ui_change: "interactive",
      ai_behavior_change: "tool",
    },
    repositories: ["desktop", "host"],
    timebox: {
      target_hours: 12,
      hard_stop_hours: 16,
      no_progress_minutes: 30,
      same_blocker_minutes: 90,
      non_core_limit_minutes: 120,
      core_blocker_minutes: 240,
    },
    product_ux: {
      status: "PASS",
      primary_user: "local demo user",
      problem: "the user needs one real outcome",
      user_outcome: "the real result is visible and saveable",
      in_scope: ["real happy path", "one representative failure"],
      out_of_scope: ["production SLO and rollout"],
      main_flow: ["start the real service", "perform the action", "inspect the result"],
      visual_direction: "clear primary action and result preview",
      ui_states: {
        idle: "ready to submit",
        loading: "show progress and prevent duplicate submit",
        success: "show and save the result",
        empty: "explain that no result exists",
        error: "show an actionable error",
        retry: "retry the failed action",
        cancel: "cancel returns to an actionable state",
      },
    },
    must_acceptance: [
      {
        id: "AC-001",
        statement: "one real end-to-end result is visible",
        verification: "run the real local service and inspect the result",
        status: "PASS",
      },
    ],
    contract: {
      impact: "none",
      authority: "N/A — no cross-boundary observable contract change",
      source_first_plan: "N/A — existing contract remains unchanged",
      status: "N/A",
      checks: [],
    },
    external_authorizations: {
      paid_calls: { allowed: false, max_actions: 0, approved_by: "N/A", approved_at: "N/A" },
      destructive_operations: {
        allowed: false,
        max_actions: 0,
        approved_by: "N/A",
        approved_at: "N/A",
      },
      production_writes: {
        allowed: false,
        max_actions: 0,
        approved_by: "N/A",
        approved_at: "N/A",
      },
    },
    implementation: {
      status: "complete",
      real_entrypoint: "pnpm dev",
      mock_only: false,
    },
    verification: {
      status: "PASS",
      verified_at: "2026-08-23T12:00:00+08:00",
      startup: {
        status: "PASS",
        command_or_steps: "pnpm dev and wait for readiness",
        environment: "local desktop runtime",
        actual_result: "service became ready",
      },
      real_smoke: {
        status: "PASS",
        command_or_steps: "perform AC-001 in the real app",
        environment: "local desktop runtime",
        actual_result: "real result was displayed",
      },
      representative_failure: {
        status: "PASS",
        command_or_steps: "trigger one bounded provider error and retry",
        environment: "local desktop runtime",
        actual_result: "error was actionable and retry recovered",
      },
      focused_checks: [
        { repository: "desktop", command: "pnpm test -- focused", status: "PASS", exit_code: 0 },
      ],
      artifacts: ["local screenshot and redacted request id"],
      diff_review: { status: "PASS", summary: "only intended files changed" },
      known_limitations: ["production hardening is deferred"],
    },
    public_readiness: publicRequired
      ? {
          required: true,
          status: "PASS",
          checks: [
            "auth_and_data",
            "cost_limits",
            "input_limits",
            "recovery",
            "safe_errors",
            "secrets",
          ].map((id) => ({ id, status: "PASS", evidence: `${id} checked` })),
          external_smoke: {
            status: "PASS",
            command_or_steps: "open the public URL and perform AC-001",
            actual_result: "public smoke passed",
          },
        }
      : {
          required: false,
          status: "N/A",
          checks: [],
          external_smoke: { status: "NOT RUN", command_or_steps: "N/A", actual_result: "N/A" },
        },
    documents: {
      brief: "00-feature-brief.md",
      delivery_log: "01-delivery-log.md",
      verification: "02-verification.md",
    },
  };
}

test("schema v2 accepts qualified G2V, per-slice G3, and split G4 evidence", () => {
  const data = validV2();
  assert.deepEqual(validateFeatureData(data, { gate: "G2V" }).errors, []);
  assert.deepEqual(validateFeatureData(data, { gate: "G3", sliceId: "S1" }).errors, []);
  assert.deepEqual(validateFeatureData(data, { gate: "G4" }).errors, []);
});

test("schema v2 G3 is per-slice and rejects required NOT RUN evidence", () => {
  const withoutSlice = validateFeatureData(validV2(), { gate: "G3" });
  assert.ok(withoutSlice.errors.some((error) => error.includes("requires --slice")));

  const data = validV2();
  data.slices[0].vertical_evidence.status = "NOT RUN";
  data.slices[0].vertical_evidence.refs = [];
  const result = validateFeatureData(data, { gate: "G3", sliceId: "S1" });
  assert.ok(result.errors.some((error) => error.includes("vertical_evidence.status must be PASS")));
});

test("slice evidence N/A requires an explicit Owner exception and local evidence is never optional", () => {
  const data = validV2();
  data.slices[0].boundary_evidence = {
    required: false,
    status: "N/A",
    refs: [],
    reason: "not needed",
  };
  data.slices[0].local_evidence = evidence(false);
  const result = validateFeatureData(data, { gate: "G3", sliceId: "S1" });
  assert.ok(result.errors.some((error) => error.includes("boundary_evidence.exception")));
  assert.ok(result.errors.some((error) => error.includes("local_evidence.required must be true")));
});

test("per-slice freshness must bind the current implementation and harness", () => {
  const data = validV2();
  data.slices[0].freshness.commits = [commit("desktop", "c".repeat(40))];
  data.slices[0].freshness.harness.digest = "c".repeat(64);
  const result = validateFeatureData(data, { gate: "G3", sliceId: "S1" });
  assert.ok(result.errors.some((error) => error.includes("immutable reference set")));
  assert.ok(result.errors.some((error) => error.includes("match the qualified harness")));
});

test("a passing slice cannot depend on a falsely passing prerequisite", () => {
  const data = validV2();
  const second = structuredClone(data.slices[0]);
  second.id = "S2";
  second.prerequisites = ["S1"];
  data.slices.push(second);
  data.slices[0].boundary_evidence.status = "NOT RUN";
  const result = validateFeatureData(data, { gate: "G3", sliceId: "S2" });
  assert.ok(result.errors.some((error) => error.includes("slice S1.boundary_evidence.status")));
});

test("cross-repository slice freshness includes every transitive prerequisite commit", () => {
  const data = validV2();
  data.repositories.push("host");
  const second = structuredClone(data.slices[0]);
  second.id = "S2";
  second.prerequisites = ["S1"];
  second.commits = [commit("host", SHA_B)];
  second.freshness.commits = [commit("desktop"), commit("host", SHA_B)];
  data.slices.push(second);
  assert.deepEqual(validateFeatureData(data, { gate: "G3", sliceId: "S2" }).errors, []);

  second.freshness.commits = [commit("host", SHA_B)];
  const stale = validateFeatureData(data, { gate: "G3", sliceId: "S2" });
  assert.ok(stale.errors.some((error) => error.includes("immutable reference set")));
});

test("serial slices in one repository can bind both immutable slice commits", () => {
  const data = validV2();
  const second = structuredClone(data.slices[0]);
  second.id = "S2";
  second.prerequisites = ["S1"];
  second.commits = [commit("desktop", SHA_B)];
  second.freshness.commits = [commit("desktop"), commit("desktop", SHA_B)];
  data.slices.push(second);
  assert.deepEqual(validateFeatureData(data, { gate: "G3", sliceId: "S2" }).errors, []);
});

test("G2V rejects an unqualified harness", () => {
  const data = validV2();
  data.runtime_harnesses[0].qualification.status = "NOT RUN";
  const result = validateFeatureData(data, { gate: "G2V" });
  assert.ok(result.errors.some((error) => error.includes("qualification.status must be PASS")));
});

test("temporal contract invariants require executable conformance tests", () => {
  const data = validV2();
  data.temporal_contract_matrix.invariants[0].executable_tests = [];
  const result = validateFeatureData(data, { gate: "G2" });
  assert.ok(result.errors.some((error) => error.includes("executable_tests")));
});

test("a required temporal invariant cannot be backed only by an N/A conformance test", () => {
  const data = validV2();
  const executable = data.temporal_contract_matrix.executable_tests[0];
  executable.required = false;
  executable.status = "N/A";
  executable.exit_code = null;
  executable.verified_at = "N/A";
  executable.commits = [];
  executable.evidence_ref = "N/A";
  executable.exception = {
    owner: "Technical Owner",
    approved_at: "2026-08-23T09:00:00+08:00",
    reason: "claimed not applicable",
  };
  const result = validateFeatureData(data, { gate: "G3", sliceId: "S1" });
  assert.ok(
    result.errors.some((error) =>
      error.includes("TINV-001 must reference at least one required executable test"),
    ),
  );
});

test("a slice cannot borrow temporal conformance assigned to another slice", () => {
  const data = validV2();
  const second = structuredClone(data.slices[0]);
  second.id = "S2";
  second.status = "pending";
  second.status_reason = "not implemented";
  data.slices.push(second);
  data.temporal_contract_matrix.executable_tests[0].slice_id = "S2";
  const result = validateFeatureData(data, { gate: "G3", sliceId: "S1" });
  assert.ok(
    result.errors.some((error) =>
      error.includes("TINV-001 must reference a required executable test for slice S1"),
    ),
  );
});

test("temporal scenarios form one acyclic ordered contract", () => {
  const data = validV2();
  data.temporal_contract_matrix.scenarios.push({
    id: "FLOW-CYCLE-001",
    ordered_phases: ["cleanup", "producer"],
  });
  const result = validateFeatureData(data, { gate: "G2" });
  assert.ok(result.errors.some((error) => error.includes("contains a cycle")));
});

test("declared persistence/runtime scope cannot erase mandatory temporal phases", () => {
  const data = validV2();
  data.scope.persistence_change = "durable";
  for (const phase of ["persistence", "notification", "terminal"]) {
    data.temporal_contract_matrix.phases[phase] = { status: "N/A", reason: "not needed" };
    data.temporal_contract_matrix.phase_exceptions[phase] = {
      owner: "Technical Owner",
      approved_at: "2026-08-23T09:00:00+08:00",
      reason: "claimed not applicable",
    };
  }
  data.temporal_contract_matrix.scenarios = [
    { id: "FLOW-LIVE-001", ordered_phases: ["producer", "cleanup"] },
    { id: "FLOW-REPLAY-001", ordered_phases: ["producer", "cleanup"] },
  ];
  const result = validateFeatureData(data, { gate: "G2" });
  assert.ok(result.errors.some((error) => error.includes("phase persistence must be required")));
  assert.ok(result.errors.some((error) => error.includes("phase notification must be required")));
  assert.ok(result.errors.some((error) => error.includes("phase terminal must be required")));
});

test("G2V evidence binds every declared participating repository", () => {
  const data = validV2();
  data.repositories.push("host");
  data.vertical_feasibility.participating_repositories.push("host");
  const result = validateFeatureData(data, { gate: "G2V" });
  assert.ok(result.errors.some((error) => error.includes("commit repositories")));
});

test("G2V cannot substitute a browser mock for the qualified real platform", () => {
  const data = validV2();
  data.vertical_feasibility.platform = "browser mock";
  data.vertical_feasibility.evidence.platform = "browser mock";
  const result = validateFeatureData(data, { gate: "G2V" });
  assert.ok(result.errors.some((error) => error.includes("qualified harness real platform")));
});

test("G2V requires positive, negative, timeout, cleanup, and content-free harness controls", () => {
  const data = validV2();
  data.runtime_harnesses[0].qualification.negative_controls.gate_failure.status = "NOT RUN";
  const result = validateFeatureData(data, { gate: "G2V" });
  assert.ok(result.errors.some((error) => error.includes("negative_controls.gate_failure")));
});

test("G4 keeps core, accessibility/visual, and teardown verdicts independent", () => {
  const data = validV2();
  data.final_e2e.teardown.status = "NOT RUN";
  data.final_e2e.teardown.evidence_refs = [];
  const result = validateFeatureData(data, { gate: "G4" });
  assert.ok(result.errors.some((error) => error.includes("final_e2e.teardown.status must be PASS")));
});

test("the third equivalent failure trips the circuit breaker", () => {
  const data = validV2();
  data.failure_circuit_breaker.incidents.push(trippedIncident("armed"));
  const result = validateFeatureData(data);
  assert.ok(result.errors.some((error) => error.includes("state must be rca_required")));
});

test("the third failure cannot be marked resolved without an approved RCA cycle", () => {
  const data = validV2();
  data.failure_circuit_breaker.incidents.push(trippedIncident("resolved"));
  const result = validateFeatureData(data);
  assert.ok(result.errors.some((error) => error.includes("state must be rca_required")));
});

test("an open three-failure breaker blocks G2V and per-slice G3", () => {
  const data = validV2();
  data.failure_circuit_breaker.incidents.push(trippedIncident());
  assert.ok(
    validateFeatureData(data, { gate: "G2V" }).errors.some((error) =>
      error.includes("blocks G2V"),
    ),
  );
  assert.ok(
    validateFeatureData(data, { gate: "G3", sliceId: "S1" }).errors.some((error) =>
      error.includes("blocks G3/S1"),
    ),
  );
});

test("renaming evidence IDs cannot split one equivalent failure to reset the fuse", () => {
  const data = validV2();
  for (let index = 1; index <= 3; index += 1) {
    const incident = trippedIncident("armed");
    incident.id = `INC-00${index}`;
    incident.evidence_id = `EV-RENAMED-${index}`;
    incident.fingerprint = `S1|G3|EV-RENAMED-${index}|harness_failure|runtime_failed|post_lifecycle`;
    incident.attempts = [failureAttempt(index)];
    data.failure_circuit_breaker.incidents.push(incident);
  }
  const result = validateFeatureData(data, { gate: "G3", sliceId: "S1" });
  assert.ok(result.errors.some((error) => error.includes("do not reset the fuse")));
});

test("one Owner-authorized post-RCA success can resolve a tripped incident", () => {
  const data = validV2();
  const incident = trippedIncident("resolved");
  incident.rca_cycles.push({
    id: "RCA-CYCLE-001",
    audit: {
      status: "complete",
      expanded_scope: ["router", "platform", "harness"],
      candidates: ["candidate A", "candidate B"],
      discriminating_evidence_refs: [ref("EV-RCA-001")],
      approved_next_action: "apply the single evidence-backed repair",
      approved_by: "Technical Owner",
      approved_at: "2026-08-23T12:00:00+08:00",
    },
    authorization: {
      max_attempts: 1,
      action: "apply the single evidence-backed repair",
      approved_by: "Technical Owner",
      approved_at: "2026-08-23T12:01:00+08:00",
    },
    attempt: {
      run_id: "RUN-RCA-001",
      occurred_at: "2026-08-23T12:02:00+08:00",
      result: "PASS",
      evidence_ref: ref("EV-RCA-RESULT-001"),
    },
  });
  data.failure_circuit_breaker.incidents.push(incident);
  assert.deepEqual(validateFeatureData(data).errors, []);
});

test("failure ledger evolution is append-only across the CI base ref", () => {
  const previous = validV2();
  previous.failure_circuit_breaker.incidents.push(trippedIncident());

  const removed = validV2();
  assert.ok(
    validateFailureLedgerEvolution(previous, removed).some((error) =>
      error.includes("incident was removed"),
    ),
  );

  const rewritten = structuredClone(previous);
  rewritten.failure_circuit_breaker.incidents[0].attempts[0].run_id = "RUN-REWRITTEN";
  assert.ok(
    validateFailureLedgerEvolution(previous, rewritten).some((error) =>
      error.includes("attempts[0] is immutable"),
    ),
  );

  const appended = structuredClone(previous);
  appended.failure_circuit_breaker.incidents[0].rca_cycles.push({
    id: "RCA-CYCLE-001",
    audit: { status: "pending" },
    authorization: null,
    attempt: null,
  });
  assert.deepEqual(validateFailureLedgerEvolution(previous, appended), []);

  const downgraded = structuredClone(previous);
  downgraded.schema_version = 1;
  assert.ok(
    validateFailureLedgerEvolution(previous, downgraded).some((error) =>
      error.includes("cannot be downgraded"),
    ),
  );
});

test("a package absent from the CI base must start at schema v3 with an explicit profile", () => {
  assert.ok(
    validateFeaturePackageEvolution(null, { schema_version: 1 }).some((error) =>
      error.includes("must use schema_version: 3"),
    ),
  );
  assert.ok(
    validateFeaturePackageEvolution(null, validV2()).some((error) =>
      error.includes("must use schema_version: 3"),
    ),
  );
  assert.deepEqual(validateFeaturePackageEvolution(null, validDemoV3()), []);
  assert.deepEqual(validateFeaturePackageEvolution(null, validProductionV3()), []);
});

test("a legacy v1 manifest is immutable until it is migrated to schema v2", () => {
  const previous = { schema_version: 1, gates: { G4_code_complete: "pending" } };
  const changed = structuredClone(previous);
  changed.gates.G4_code_complete = "pass";
  assert.ok(
    validateFeaturePackageEvolution(previous, changed).some((error) =>
      error.includes("historical-only"),
    ),
  );
  assert.deepEqual(validateFeaturePackageEvolution(previous, structuredClone(previous)), []);
});

test("harness taxonomy is closed to four failure owners", () => {
  const data = validV2();
  data.runtime_harnesses[0].failure_classes.pop();
  const result = validateFeatureData(data);
  assert.ok(result.errors.some((error) => error.includes("exactly the four closed classes")));
});

test("an evident cross-boundary trigger cannot mark G2V not applicable", () => {
  const data = validV2();
  data.vertical_feasibility.required = false;
  data.gates.G2V_vertical_feasibility = "not_applicable";
  const result = validateFeatureData(data);
  assert.ok(result.errors.some((error) => error.includes("cannot be N/A")));
});

test("closed scope enums and required slice applicability fail closed", () => {
  const invalidScope = validV2();
  invalidScope.scope.runtime_change = "runtim";
  assert.ok(
    validateFeatureData(invalidScope, { gate: "G1" }).errors.some((error) =>
      error.includes("scope.runtime_change"),
    ),
  );

  const requiredNa = validV2();
  requiredNa.slices[0].status = "not_applicable";
  const result = validateFeatureData(requiredNa, { gate: "G4" });
  assert.ok(result.errors.some((error) => error.includes("required slice S1 cannot be N/A")));
});

test("final E2E evidence binds a qualified harness digest and canonical report reference", () => {
  const data = validV2();
  data.final_e2e.core_vertical.harness.digest = "c".repeat(64);
  data.final_e2e.core_vertical.evidence_refs = ["anything"];
  const result = validateFeatureData(data, { gate: "G4" });
  assert.ok(result.errors.some((error) => error.includes("match the qualified harness")));
  assert.ok(result.errors.some((error) => error.includes("08-verification-report.md#EVIDENCE-ID")));
});

test("schema v3 demo_fast accepts one product/UX checkpoint and one real-service done checkpoint", () => {
  const data = validDemoV3();
  assert.deepEqual(validateFeatureData(data, { gate: "D0" }).errors, []);
  assert.deepEqual(validateFeatureData(data, { gate: "D4" }).errors, []);
  assert.ok(
    validateFeatureData(data, { gate: "G4" }).errors.some((error) =>
      error.includes("production_hardened"),
    ),
  );
});

function permanentlyTerminatedDemo() {
  const data = validDemoV3();
  data.feature.status = "terminated";
  data.implementation.status = "terminated";
  data.verification.status = "BLOCKED";
  data.termination = {
    owner: data.feature.requirement_owner,
    confirmed_at: "2026-09-05T11:05:49+08:00",
    reason: "Owner permanently ended implementation because the time cost was too high",
    permanent: true,
    acceptance_passed: false,
    implementation_resumes: false,
  };
  return data;
}

test("permanent termination preserves historical D0 but cannot claim acceptance", () => {
  const data = permanentlyTerminatedDemo();
  assert.deepEqual(validateFeatureData(data, { gate: "D0" }).errors, []);
  assert.ok(validateFeatureData(data, { gate: "D4" }).errors.some((e) => e.includes("cannot claim a completion gate")));
  data.verification.status = "PASS";
  assert.ok(validateFeatureData(data, { gate: "D0" }).errors.some((e) => e.includes("cannot claim complete/PASS")));
});

test("permanent termination requires explicit Owner authority and cannot be reopened", () => {
  const original = permanentlyTerminatedDemo();
  assert.deepEqual(validateFeaturePackageEvolution(original, structuredClone(original)), []);
  for (const field of Object.keys(original.termination)) {
    const data = structuredClone(original);
    delete data.termination[field];
    assert.ok(validateFeatureData(data, { gate: "D0" }).errors.some((e) => e.includes("termination.")));
    assert.ok(validateFeaturePackageEvolution(original, data).some((e) => e.includes("cannot be removed or reopened")));
  }
  const reopened = structuredClone(original);
  reopened.feature.status = "active";
  assert.ok(validateFeaturePackageEvolution(original, reopened).some((e) => e.includes("cannot be removed or reopened")));
});

test("demo_fast D4 rejects mock-only, missing real smoke, and failed Must acceptance", () => {
  const data = validDemoV3();
  data.implementation.mock_only = true;
  data.verification.real_smoke.status = "NOT RUN";
  data.verification.focused_checks = [];
  data.must_acceptance[0].status = "FAIL";
  const result = validateFeatureData(data, { gate: "D4" });
  assert.ok(result.errors.some((error) => error.includes("mock_only must be false")));
  assert.ok(result.errors.some((error) => error.includes("real_smoke.status must be PASS")));
  assert.ok(result.errors.some((error) => error.includes("must_acceptance[0].status must be PASS")));
  assert.ok(result.errors.some((error) => error.includes("focused_checks must contain")));
});

test("demo_fast DP is public-only and enforces the minimum public safety floor", () => {
  assert.ok(
    validateFeatureData(validDemoV3(), { gate: "DP" }).errors.some((error) =>
      error.includes("DP requires exposure: public"),
    ),
  );
  const publicDemo = validDemoV3("public");
  assert.deepEqual(validateFeatureData(publicDemo, { gate: "DP" }).errors, []);
  publicDemo.public_readiness.checks.pop();
  assert.ok(
    validateFeatureData(publicDemo, { gate: "DP" }).errors.some((error) =>
      error.includes("must contain exactly"),
    ),
  );
});

test("schema v3 production_hardened preserves the full schema v2 gate semantics", () => {
  const data = validProductionV3();
  assert.deepEqual(validateFeatureData(data, { gate: "G4" }).errors, []);
  assert.ok(
    validateFeatureData(data, { gate: "D4" }).errors.some((error) =>
      error.includes("demo_fast"),
    ),
  );
});

test("schema v1 remains readable but cannot claim any downstream gate", () => {
  const legacy = validateFeatureData({ schema_version: 1 });
  assert.deepEqual(legacy.errors, []);
  assert.equal(legacy.warnings.length, 1);
  assert.ok(validateFeatureData({ schema_version: 1 }, { gate: "G2V" }).errors.length > 0);
  assert.ok(
    validateFeatureData({ schema_version: 1 }, { gate: "G3", sliceId: "S1" }).errors.length > 0,
  );
  assert.ok(validateFeatureData({ schema_version: 1 }, { gate: "G4" }).errors.length > 0);
});

test("shell checker treats legacy packages as historical-only at G3", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "yijie-feature-v1-g3-"));
  const requiredDocs = [
    "00-feature-brief.md",
    "01-requirements.md",
    "02-impact-assessment.md",
    "03-decisions-and-risks.md",
    "04-contract-change-plan.md",
    "05-technical-design.md",
    "06-test-plan.md",
    "07-implementation-plan.md",
    "08-verification-report.md",
    "09-release-and-rollback.md",
    "10-delivery-summary.md",
  ];
  try {
    fs.writeFileSync(path.join(root, "feature.yaml"), "schema_version: 1\n");
    for (const file of requiredDocs) fs.writeFileSync(path.join(root, file), "complete\n");
    assert.throws(
      () =>
        execFileSync(
          path.join(PACKAGE_ROOT, "scripts/check-feature-package.sh"),
          ["--gate", "G3", root],
          { stdio: "pipe" },
        ),
      (error) => error.stderr.toString().includes("must migrate to schema v2"),
    );
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("feature.yaml duplicate keys fail closed", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "yijie-feature-v2-"));
  try {
    fs.writeFileSync(path.join(root, "feature.yaml"), "schema_version: 2\nschema_version: 1\n");
    const result = loadAndValidateFeaturePackage(root);
    assert.ok(result.errors.some((error) => error.includes("Map keys must be unique")));
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("schema version comments cannot bypass the required temporal matrix file", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "yijie-feature-comment-"));
  const docs = [
    "00-feature-brief.md",
    "01-requirements.md",
    "02-impact-assessment.md",
    "03-decisions-and-risks.md",
    "04-contract-change-plan.md",
    "05-technical-design.md",
    "06-test-plan.md",
    "07-implementation-plan.md",
    "08-verification-report.md",
    "09-release-and-rollback.md",
    "10-delivery-summary.md",
  ];
  try {
    fs.writeFileSync(path.join(root, "feature.yaml"), "schema_version: 2 # current\n");
    for (const file of docs) fs.writeFileSync(path.join(root, file), "complete\n");
    assert.throws(
      () =>
        execFileSync(path.join(PACKAGE_ROOT, "scripts/check-feature-package.sh"), [root], {
          encoding: "utf8",
          stdio: "pipe",
        }),
      (error) => error.stderr.includes("MISSING: 04A-temporal-contract-matrix.md"),
    );
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("verification evidence references must resolve to one report marker", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "yijie-feature-evidence-"));
  try {
    fs.writeFileSync(path.join(root, "feature.yaml"), JSON.stringify(validV2(), null, 2));
    fs.writeFileSync(path.join(root, "04A-temporal-contract-matrix.md"), temporalReport);
    fs.writeFileSync(path.join(root, "08-verification-report.md"), "no evidence markers\n");
    const missing = loadAndValidateFeaturePackage(root, { gate: "G2V" });
    assert.ok(missing.errors.some((error) => error.includes("must resolve to exactly one")));

    fs.writeFileSync(path.join(root, "08-verification-report.md"), verificationReport());
    assert.deepEqual(loadAndValidateFeaturePackage(root, { gate: "G2V" }).errors, []);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("CI claim audit rejects a v2 slice that claims PASS with missing evidence", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "yijie-feature-claims-"));
  try {
    const data = validV2();
    data.slices[0].boundary_evidence.status = "NOT RUN";
    fs.writeFileSync(path.join(root, "feature.yaml"), JSON.stringify(data, null, 2));
    fs.writeFileSync(path.join(root, "04A-temporal-contract-matrix.md"), temporalReport);
    fs.writeFileSync(path.join(root, "08-verification-report.md"), verificationReport());
    const result = validateClaimedFeaturePackage(root);
    assert.ok(result.errors.some((error) => error.includes("G3/S1")));
    assert.ok(result.errors.some((error) => error.includes("boundary_evidence.status")));
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("repository audit applies the authoritative full-document shell check", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "yijie-feature-shell-audit-"));
  try {
    const featureDir = path.join(root, "FEAT-999-incomplete-doc-set");
    fs.mkdirSync(featureDir);
    fs.writeFileSync(path.join(featureDir, "feature.yaml"), JSON.stringify(validV2(), null, 2));
    fs.writeFileSync(path.join(featureDir, "04A-temporal-contract-matrix.md"), temporalReport);
    fs.writeFileSync(path.join(featureDir, "08-verification-report.md"), verificationReport());
    const result = auditFeaturePackages({ featureRoot: root });
    assert.ok(
      result.errors.some((error) => error.includes("authoritative shell check failed")),
    );
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("repository CI audits every committed historical and profile-aware claim", () => {
  const featureRoot = path.resolve("docs/features");
  for (const entry of fs.readdirSync(featureRoot, { withFileTypes: true })) {
    if (!entry.isDirectory() || !entry.name.startsWith("FEAT-")) continue;
    const result = validateClaimedFeaturePackage(path.join(featureRoot, entry.name));
    assert.deepEqual(result.errors, [], `${entry.name}: ${result.errors.join("; ")}`);
  }
});

test("the repository Feature Package audit entrypoint scans committed packages", () => {
  execFileSync(
    "node",
    [
      path.join(PACKAGE_ROOT, "scripts/audit-feature-packages.mjs"),
      "--base-ref",
      "HEAD",
      "docs/features",
    ],
    { stdio: "pipe" },
  );
});

test("delivery shell entrypoints remain syntactically valid", () => {
  execFileSync("bash", [
    "-n",
    path.join(PACKAGE_ROOT, "scripts/check-feature-package.sh"),
    path.join(PACKAGE_ROOT, "scripts/new-feature.sh"),
  ]);
});

test("new-feature defaults to compact schema v3 demo_fast local", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "yijie-new-feature-"));
  try {
    execFileSync(
      path.join(PACKAGE_ROOT, "scripts/new-feature.sh"),
      ["FEAT-999", "demo-fast-test", root],
      { stdio: "pipe" },
    );
    const featureDir = path.join(root, "FEAT-999-demo-fast-test");
    assert.equal(fs.existsSync(path.join(featureDir, "01-delivery-log.md")), true);
    assert.equal(fs.existsSync(path.join(featureDir, "02-verification.md")), true);
    assert.equal(fs.existsSync(path.join(featureDir, "04A-temporal-contract-matrix.md")), false);
    const source = fs.readFileSync(path.join(featureDir, "feature.yaml"), "utf8");
    assert.match(source, /^schema_version: 3$/m);
    assert.match(source, /^delivery_profile: "demo_fast"$/m);
    assert.match(source, /^exposure: "local"$/m);
    execFileSync(path.join(PACKAGE_ROOT, "scripts/check-feature-package.sh"), [featureDir], {
      stdio: "pipe",
    });
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("new-feature creates production_hardened only when explicitly selected", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "yijie-new-production-feature-"));
  try {
    execFileSync(
      path.join(PACKAGE_ROOT, "scripts/new-feature.sh"),
      [
        "--profile",
        "production_hardened",
        "--exposure",
        "public",
        "FEAT-999",
        "production-test",
        root,
      ],
      { stdio: "pipe" },
    );
    const featureDir = path.join(root, "FEAT-999-production-test");
    assert.equal(fs.existsSync(path.join(featureDir, "04A-temporal-contract-matrix.md")), true);
    const source = fs.readFileSync(path.join(featureDir, "feature.yaml"), "utf8");
    assert.match(source, /^schema_version: 3$/m);
    assert.match(source, /^delivery_profile: "production_hardened"$/m);
    assert.match(source, /^exposure: "public"$/m);
    execFileSync(path.join(PACKAGE_ROOT, "scripts/check-feature-package.sh"), [featureDir], {
      stdio: "pipe",
    });
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("shell checker enforces demo_fast D0, D4, and profile separation", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "yijie-check-demo-v3-"));
  try {
    fs.writeFileSync(path.join(root, "feature.yaml"), JSON.stringify(validDemoV3(), null, 2));
    for (const file of ["00-feature-brief.md", "01-delivery-log.md", "02-verification.md"]) {
      fs.writeFileSync(path.join(root, file), "complete\n");
    }
    const checker = path.join(PACKAGE_ROOT, "scripts/check-feature-package.sh");
    execFileSync(checker, ["--gate", "D0", root], { stdio: "pipe" });
    execFileSync(checker, ["--gate", "D4", root], { stdio: "pipe" });
    assert.throws(
      () => execFileSync(checker, ["--gate", "G4", root], { stdio: "pipe" }),
      (error) => error.stderr.toString().includes("demo_fast"),
    );
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("shell checker enforces schema v2 G2V and per-slice G3 semantics", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "yijie-check-feature-v2-"));
  const requiredDocs = [
    "00-feature-brief.md",
    "01-requirements.md",
    "02-impact-assessment.md",
    "03-decisions-and-risks.md",
    "04-contract-change-plan.md",
    "04A-temporal-contract-matrix.md",
    "05-technical-design.md",
    "06-test-plan.md",
    "07-implementation-plan.md",
    "08-verification-report.md",
    "09-release-and-rollback.md",
    "10-delivery-summary.md",
  ];
  try {
    fs.writeFileSync(path.join(root, "feature.yaml"), JSON.stringify(validV2(), null, 2));
    for (const file of requiredDocs) {
      const content =
        file === "04A-temporal-contract-matrix.md"
          ? temporalReport
          : file === "08-verification-report.md"
            ? verificationReport()
            : "complete\n";
      fs.writeFileSync(path.join(root, file), content);
    }
    const checker = path.join(PACKAGE_ROOT, "scripts/check-feature-package.sh");
    execFileSync(checker, ["--gate", "G2V", root], { stdio: "pipe" });
    execFileSync(checker, ["--gate", "G3", "--slice", "S1", root], { stdio: "pipe" });
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
