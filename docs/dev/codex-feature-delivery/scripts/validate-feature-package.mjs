#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { pathToFileURL } from "node:url";
import { isDeepStrictEqual } from "node:util";
import YAML from "yaml";

const GATE_KEYS = {
  G0: "G0_intake",
  G1: "G1_design_ready",
  G2: "G2_implementation_ready",
  G2A: "G2A_contract_ready",
  G2V: "G2V_vertical_feasibility",
  G4: "G4_code_complete",
  G5: "G5_production_ready",
  G6: "G6_delivery_complete",
};
const GATE_PREREQUISITES = new Set(["G0", "G1", "G2", "G2A", "G2V"]);
const DOWNSTREAM_GATES = new Set(["G2V", "G3", "G4", "G5", "G6"]);
const DEMO_GATES = new Set(["D0", "D4", "DP"]);
const DELIVERY_PROFILES = new Set(["demo_fast", "production_hardened"]);
const EXPOSURES = new Set(["local", "public"]);
const PUBLIC_DEMO_CHECKS = [
  "auth_and_data",
  "cost_limits",
  "input_limits",
  "recovery",
  "safe_errors",
  "secrets",
];
const GATE_STATUSES = new Set(["blocked", "fail", "not_applicable", "pass", "pending"]);
const SLICE_STATUSES = new Set(["blocked", "fail", "not_applicable", "pass", "pending"]);
const FAILURE_CLASSES = [
  "gate_failure",
  "harness_failure",
  "platform_failure",
  "product_failure",
];
const FINAL_E2E_KEYS = ["core_vertical", "accessibility_visual", "teardown"];
const TEMPORAL_PHASES = [
  "cleanup",
  "notification",
  "persistence",
  "producer",
  "replay",
  "terminal",
];
const SCOPE_ENUMS = {
  risk_level: ["low", "medium", "high", "critical"],
  data_classification: ["public", "internal", "confidential", "restricted"],
  contract_impact: ["none", "additive", "semantic", "breaking"],
  database_change: ["none", "expand", "migrate", "contract"],
  persistence_change: ["none", "durable", "replay"],
  runtime_change: ["none", "runtime", "platform"],
  auth_permission_change: ["none", "auth", "permission", "both"],
  user_workflow_change: ["none", "internal", "user_visible"],
  ui_change: ["none", "visual", "interactive"],
  ai_behavior_change: ["none", "prompt", "model", "retrieval", "tool", "eval"],
};
const FULL_SHA = /^[0-9a-f]{40}$/;
const SHA256 = /^[0-9a-f]{64}$/;
const EVIDENCE_REF = /^08-verification-report\.md#([A-Z][A-Z0-9._-]{2,127})$/;
const SENTINELS = new Set(["", "tbd", "todo", "not run", "not_run", "n/a"]);

function normalized(value) {
  return typeof value === "string"
    ? value.trim().toLowerCase().replace(/[\s-]+/g, "_")
    : "";
}

function meaningful(value) {
  return typeof value === "string" && !SENTINELS.has(value.trim().toLowerCase());
}

function isPass(value) {
  return normalized(value) === "pass";
}

function isFail(value) {
  return normalized(value) === "fail";
}

function isNotApplicable(value) {
  return ["n/a", "not_applicable"].includes(normalized(value));
}

function isFullSha(value) {
  return typeof value === "string" && FULL_SHA.test(value);
}

function isSha256(value) {
  return typeof value === "string" && SHA256.test(value);
}

function isIsoInstant(value) {
  return (
    meaningful(value) &&
    /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/.test(value) &&
    !Number.isNaN(Date.parse(value))
  );
}

function asObject(value) {
  return value && typeof value === "object" && !Array.isArray(value) ? value : null;
}

function addRequiredObject(errors, value, label) {
  const object = asObject(value);
  if (!object) errors.push(`${label} must be an object`);
  return object;
}

function exactSet(errors, actual, expected, label) {
  if (!Array.isArray(actual)) {
    errors.push(`${label} must be an array`);
    return;
  }
  const normalizedActual = [...new Set(actual)].sort();
  const normalizedExpected = [...new Set(expected)].sort();
  if (normalizedActual.length !== actual.length) errors.push(`${label} must not contain duplicates`);
  if (JSON.stringify(normalizedActual) !== JSON.stringify(normalizedExpected)) {
    errors.push(`${label} must exactly match the current immutable reference set`);
  }
}

function validateEvidenceRef(errors, ref, label) {
  if (typeof ref !== "string" || !EVIDENCE_REF.test(ref)) {
    errors.push(`${label} must use 08-verification-report.md#EVIDENCE-ID`);
  }
}

function validateEvidenceRefs(errors, refs, label, required) {
  if (!Array.isArray(refs)) {
    errors.push(`${label} must be an array`);
    return;
  }
  if (required && refs.length === 0) errors.push(`${label} must not be empty`);
  for (const [index, ref] of refs.entries()) validateEvidenceRef(errors, ref, `${label}[${index}]`);
  if (new Set(refs).size !== refs.length) errors.push(`${label} must not contain duplicates`);
}

function validateException(errors, exception, label) {
  const value = addRequiredObject(errors, exception, label);
  if (!value) return;
  if (!meaningful(value.owner)) errors.push(`${label}.owner is required`);
  if (!isIsoInstant(value.approved_at)) errors.push(`${label}.approved_at must be an ISO-8601 instant`);
  if (!meaningful(value.reason)) errors.push(`${label}.reason is required`);
}

function obviousG2VTrigger(data) {
  const scope = asObject(data.scope) ?? {};
  const repositories = Array.isArray(data.repositories) ? data.repositories : [];
  return (
    ["high", "critical"].includes(normalized(scope.risk_level)) ||
    repositories.length > 1 ||
    !["", "none", "tbd"].includes(normalized(scope.contract_impact)) ||
    !["", "none", "tbd"].includes(normalized(scope.database_change)) ||
    !["", "none", "tbd"].includes(normalized(scope.persistence_change)) ||
    !["", "none", "tbd"].includes(normalized(scope.runtime_change)) ||
    !["", "none", "tbd"].includes(normalized(scope.auth_permission_change)) ||
    normalized(scope.user_workflow_change) === "user_visible"
  );
}

function boundaryEvidenceRequired(data) {
  const scope = asObject(data.scope) ?? {};
  return (
    (Array.isArray(data.repositories) && data.repositories.length > 1) ||
    [
      scope.contract_impact,
      scope.database_change,
      scope.persistence_change,
      scope.runtime_change,
      scope.auth_permission_change,
    ].some((value) => !["", "none", "tbd"].includes(normalized(value)))
  );
}

function gateStatus(data, gate) {
  return asObject(data.gates)?.[GATE_KEYS[gate]];
}

function validateGatePassed(errors, data, gate) {
  if (!isPass(gateStatus(data, gate))) errors.push(`gate ${gate} must be pass`);
}

function validateDesignGateChain(errors, data, throughGate) {
  const chain = ["G0", "G1", "G2"];
  const end = chain.indexOf(throughGate);
  for (const gate of chain.slice(0, end + 1)) validateGatePassed(errors, data, gate);
}

function deliveryProfile(data) {
  if (data?.schema_version === 3) return normalized(data.delivery_profile);
  if (data?.schema_version === 2) return "production_hardened";
  return "legacy";
}

function validateV3Envelope(errors, data) {
  const profile = deliveryProfile(data);
  if (!DELIVERY_PROFILES.has(profile)) {
    errors.push("delivery_profile must be demo_fast or production_hardened");
  }
  if (!EXPOSURES.has(normalized(data.exposure))) {
    errors.push("exposure must be local or public");
  }
  return profile;
}

function validateMeaningfulList(errors, value, label, { minimum = 1 } = {}) {
  if (!Array.isArray(value)) {
    errors.push(`${label} must be an array`);
    return;
  }
  if (value.length < minimum) errors.push(`${label} must contain at least ${minimum} item(s)`);
  for (const [index, item] of value.entries()) {
    if (!meaningful(item)) errors.push(`${label}[${index}] must be meaningful`);
  }
}

function validateDemoAuthorization(errors, value, label) {
  const authorization = addRequiredObject(errors, value, label);
  if (!authorization) return;
  if (typeof authorization.allowed !== "boolean") errors.push(`${label}.allowed must be boolean`);
  if (!Number.isInteger(authorization.max_actions) || authorization.max_actions < 0) {
    errors.push(`${label}.max_actions must be a non-negative integer`);
  }
  if (authorization.allowed) {
    if (authorization.max_actions < 1) errors.push(`${label}.max_actions must be positive when allowed`);
    if (!meaningful(authorization.approved_by)) errors.push(`${label}.approved_by is required when allowed`);
    if (!isIsoInstant(authorization.approved_at)) {
      errors.push(`${label}.approved_at must be an ISO-8601 instant when allowed`);
    }
  } else if (authorization.max_actions !== 0) {
    errors.push(`${label}.max_actions must be 0 when not allowed`);
  }
}

function validateDemoCheckList(errors, checks, label, { minimum = 1 } = {}) {
  if (!Array.isArray(checks)) {
    errors.push(`${label} must be an array`);
    return;
  }
  if (checks.length < minimum) errors.push(`${label} must contain at least ${minimum} check(s)`);
  for (const [index, check] of checks.entries()) {
    const itemLabel = `${label}[${index}]`;
    if (!asObject(check)) {
      errors.push(`${itemLabel} must be an object`);
      continue;
    }
    if (!meaningful(check.repository)) errors.push(`${itemLabel}.repository is required`);
    if (!meaningful(check.command)) errors.push(`${itemLabel}.command is required`);
    if (!isPass(check.status)) errors.push(`${itemLabel}.status must be PASS`);
    if (check.exit_code !== 0) errors.push(`${itemLabel}.exit_code must equal 0`);
  }
}

function validateDemoPlanning(errors, data) {
  validateFeatureIdentity(errors, data);
  validatePlanningScope(errors, data);
  const timebox = addRequiredObject(errors, data.timebox, "timebox");
  if (timebox) {
    for (const [field, minimum, maximum] of [
      ["target_hours", 1, 16],
      ["hard_stop_hours", 1, 24],
      ["no_progress_minutes", 15, 60],
      ["same_blocker_minutes", 30, 120],
      ["non_core_limit_minutes", 30, 180],
      ["core_blocker_minutes", 60, 360],
    ]) {
      const value = timebox[field];
      if (!Number.isInteger(value) || value < minimum || value > maximum) {
        errors.push(`timebox.${field} must be an integer between ${minimum} and ${maximum}`);
      }
    }
    if (
      Number.isInteger(timebox.target_hours) &&
      Number.isInteger(timebox.hard_stop_hours) &&
      timebox.target_hours > timebox.hard_stop_hours
    ) {
      errors.push("timebox.target_hours must not exceed timebox.hard_stop_hours");
    }
  }

  const product = addRequiredObject(errors, data.product_ux, "product_ux");
  if (product) {
    if (!isPass(product.status)) errors.push("product_ux.status must be PASS for D0");
    for (const field of ["primary_user", "problem", "user_outcome", "visual_direction"]) {
      if (!meaningful(product[field])) errors.push(`product_ux.${field} is required`);
    }
    validateMeaningfulList(errors, product.in_scope, "product_ux.in_scope");
    validateMeaningfulList(errors, product.out_of_scope, "product_ux.out_of_scope");
    validateMeaningfulList(errors, product.main_flow, "product_ux.main_flow", { minimum: 2 });
    const states = addRequiredObject(errors, product.ui_states, "product_ux.ui_states");
    if (states) {
      for (const state of ["idle", "loading", "success", "empty", "error", "retry", "cancel"]) {
        if (!meaningful(states[state])) errors.push(`product_ux.ui_states.${state} is required`);
      }
    }
  }

  if (!Array.isArray(data.must_acceptance) || data.must_acceptance.length === 0) {
    errors.push("must_acceptance must contain at least one acceptance criterion");
  } else {
    const ids = new Set();
    for (const [index, acceptance] of data.must_acceptance.entries()) {
      const label = `must_acceptance[${index}]`;
      if (!asObject(acceptance)) {
        errors.push(`${label} must be an object`);
        continue;
      }
      if (!/^AC-[A-Z0-9._-]+$/.test(acceptance.id ?? "")) errors.push(`${label}.id must be AC-*`);
      if (ids.has(acceptance.id)) errors.push(`${label}.id must be unique`);
      ids.add(acceptance.id);
      if (!meaningful(acceptance.statement)) errors.push(`${label}.statement is required`);
      if (!meaningful(acceptance.verification)) errors.push(`${label}.verification is required`);
      if (!["pending", "pass", "fail"].includes(normalized(acceptance.status))) {
        errors.push(`${label}.status must be pending, pass, or fail`);
      }
    }
  }

  const contract = addRequiredObject(errors, data.contract, "contract");
  const impact = normalized(asObject(data.scope)?.contract_impact);
  if (contract) {
    if (normalized(contract.impact) !== impact) errors.push("contract.impact must match scope.contract_impact");
    if (!meaningful(contract.authority)) errors.push("contract.authority is required");
    if (!meaningful(contract.source_first_plan)) errors.push("contract.source_first_plan is required");
    if (!["not_run", "pass", "n/a", "not_applicable"].includes(normalized(contract.status))) {
      errors.push("contract.status must be NOT RUN, PASS, or N/A");
    }
    if (impact === "none" && !isNotApplicable(contract.status)) {
      errors.push("contract.status must be N/A when contract_impact is none");
    }
  }

  const authorizations = addRequiredObject(errors, data.external_authorizations, "external_authorizations");
  if (authorizations) {
    validateDemoAuthorization(errors, authorizations.paid_calls, "external_authorizations.paid_calls");
    validateDemoAuthorization(errors, authorizations.destructive_operations, "external_authorizations.destructive_operations");
    validateDemoAuthorization(errors, authorizations.production_writes, "external_authorizations.production_writes");
  }
}

function validateDemoDone(errors, data) {
  validateDemoPlanning(errors, data);
  if (normalized(data.feature?.status) !== "usable") errors.push("feature.status must be usable for D4");
  const implementation = addRequiredObject(errors, data.implementation, "implementation");
  if (implementation) {
    if (normalized(implementation.status) !== "complete") {
      errors.push("implementation.status must be complete for D4");
    }
    if (!meaningful(implementation.real_entrypoint)) errors.push("implementation.real_entrypoint is required");
    if (implementation.mock_only !== false) errors.push("implementation.mock_only must be false");
  }
  for (const [index, acceptance] of (data.must_acceptance ?? []).entries()) {
    if (!isPass(acceptance?.status)) errors.push(`must_acceptance[${index}].status must be PASS for D4`);
  }
  const contract = asObject(data.contract);
  if (normalized(data.scope?.contract_impact) !== "none") {
    if (!isPass(contract?.status)) errors.push("contract.status must be PASS for a contract-impacting D4");
    validateDemoCheckList(errors, contract?.checks, "contract.checks");
  }
  const verification = addRequiredObject(errors, data.verification, "verification");
  if (!verification) return;
  if (!isPass(verification.status)) errors.push("verification.status must be PASS for D4");
  if (!isIsoInstant(verification.verified_at)) {
    errors.push("verification.verified_at must be an ISO-8601 instant for D4");
  }
  for (const key of ["startup", "real_smoke", "representative_failure"]) {
    const check = addRequiredObject(errors, verification[key], `verification.${key}`);
    if (!check) continue;
    if (!isPass(check.status)) errors.push(`verification.${key}.status must be PASS`);
    if (!meaningful(check.command_or_steps)) {
      errors.push(`verification.${key}.command_or_steps is required`);
    }
    if (!meaningful(check.environment)) errors.push(`verification.${key}.environment is required`);
    if (!meaningful(check.actual_result)) errors.push(`verification.${key}.actual_result is required`);
  }
  validateDemoCheckList(errors, verification.focused_checks, "verification.focused_checks");
  validateMeaningfulList(errors, verification.artifacts, "verification.artifacts");
  if (!isPass(verification.diff_review?.status)) errors.push("verification.diff_review.status must be PASS");
  if (!meaningful(verification.diff_review?.summary)) {
    errors.push("verification.diff_review.summary is required");
  }
  if (!Array.isArray(verification.known_limitations)) {
    errors.push("verification.known_limitations must be an array");
  }
}

function validateDemoPublic(errors, data) {
  validateDemoDone(errors, data);
  if (normalized(data.exposure) !== "public") errors.push("DP requires exposure: public");
  const readiness = addRequiredObject(errors, data.public_readiness, "public_readiness");
  if (!readiness) return;
  if (readiness.required !== true) errors.push("public_readiness.required must be true for public exposure");
  if (!isPass(readiness.status)) errors.push("public_readiness.status must be PASS for DP");
  const checks = Array.isArray(readiness.checks) ? readiness.checks : [];
  const ids = checks.map((check) => check?.id).sort();
  if (JSON.stringify(ids) !== JSON.stringify(PUBLIC_DEMO_CHECKS)) {
    errors.push(`public_readiness.checks must contain exactly: ${PUBLIC_DEMO_CHECKS.join(", ")}`);
  }
  for (const [index, check] of checks.entries()) {
    if (!isPass(check?.status)) errors.push(`public_readiness.checks[${index}].status must be PASS`);
    if (!meaningful(check?.evidence)) errors.push(`public_readiness.checks[${index}].evidence is required`);
  }
  const smoke = addRequiredObject(errors, readiness.external_smoke, "public_readiness.external_smoke");
  if (smoke) {
    if (!isPass(smoke.status)) errors.push("public_readiness.external_smoke.status must be PASS");
    if (!meaningful(smoke.command_or_steps)) {
      errors.push("public_readiness.external_smoke.command_or_steps is required");
    }
    if (!meaningful(smoke.actual_result)) errors.push("public_readiness.external_smoke.actual_result is required");
  }
}

function validateDemoBase(errors, data, gate) {
  for (const key of ["feature", "scope", "timebox", "product_ux", "contract", "external_authorizations", "implementation", "verification", "public_readiness", "documents"]) {
    addRequiredObject(errors, data[key], key);
  }
  if (gate === "D0") validateDemoPlanning(errors, data);
  if (gate === "D4") validateDemoDone(errors, data);
  if (gate === "DP") validateDemoPublic(errors, data);
  const readiness = asObject(data.public_readiness);
  if (normalized(data.exposure) === "local") {
    if (readiness?.required !== false) errors.push("public_readiness.required must be false for local exposure");
    if (!isNotApplicable(readiness?.status)) errors.push("public_readiness.status must be N/A for local exposure");
  } else if (normalized(data.exposure) === "public" && readiness?.required !== true) {
    errors.push("public_readiness.required must be true for public exposure");
  }
}

function validateTermination(errors, data, gate) {
  if (normalized(data.feature?.status) !== "terminated") return;
  const termination = addRequiredObject(errors, data.termination, "termination");
  if (termination) {
    if (termination.owner !== data.feature.requirement_owner) errors.push("termination.owner must be the requirement owner");
    if (!isIsoInstant(termination.confirmed_at)) errors.push("termination.confirmed_at must be an ISO-8601 instant");
    if (!meaningful(termination.reason)) errors.push("termination.reason is required");
    if (termination.permanent !== true) errors.push("termination.permanent must be true");
    if (termination.acceptance_passed !== false) errors.push("termination.acceptance_passed must be false");
    if (termination.implementation_resumes !== false) errors.push("termination.implementation_resumes must be false");
  }
  if (["D4", "DP", "G4", "G5", "G6"].includes(gate)) {
    errors.push("permanently terminated feature cannot claim a completion gate");
  }
  if (normalized(data.implementation?.status) === "complete" || isPass(data.verification?.status)) {
    errors.push("permanent termination without acceptance cannot claim complete/PASS");
  }
}

function validateFeatureIdentity(errors, data) {
  const feature = addRequiredObject(errors, data.feature, "feature");
  if (!feature) return;
  if (!/^FEAT-[0-9]+$/.test(feature.id ?? "")) errors.push("feature.id must match FEAT-<number>");
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(feature.slug ?? "")) {
    errors.push("feature.slug must be a lowercase kebab-case slug");
  }
  for (const field of ["title", "requirement_owner", "technical_owner", "reviewer", "release_owner"]) {
    if (!meaningful(feature[field])) errors.push(`feature.${field} is required`);
  }
  if (!/^\d{4}-\d{2}-\d{2}$/.test(feature.created_at ?? "")) {
    errors.push("feature.created_at must be YYYY-MM-DD");
  }
}

function validatePlanningScope(errors, data) {
  const scope = addRequiredObject(errors, data.scope, "scope");
  if (scope) {
    for (const [field, allowed] of Object.entries(SCOPE_ENUMS)) {
      if (!allowed.includes(normalized(scope[field]))) {
        errors.push(`scope.${field} must be one of: ${allowed.join(", ")}`);
      }
    }
  }
  if (!Array.isArray(data.repositories) || data.repositories.length === 0) {
    errors.push("repositories must contain at least one affected repository");
  } else {
    for (const [index, repository] of data.repositories.entries()) {
      if (!meaningful(repository)) errors.push(`repositories[${index}] must be a repository name`);
    }
    if (new Set(data.repositories).size !== data.repositories.length) {
      errors.push("repositories must not contain duplicates");
    }
  }
}

function repositorySet(data) {
  return new Set(Array.isArray(data.repositories) ? data.repositories : []);
}

function validateCommitList(
  errors,
  commits,
  label,
  data,
  { required = true, allowMultiplePerRepository = false } = {},
) {
  if (!Array.isArray(commits)) {
    errors.push(`${label} must be an array`);
    return [];
  }
  if (required && commits.length === 0) errors.push(`${label} must not be empty`);
  const knownRepositories = repositorySet(data);
  const tokens = [];
  const seenRepositories = new Set();
  for (const [index, commit] of commits.entries()) {
    const itemLabel = `${label}[${index}]`;
    if (!asObject(commit)) {
      errors.push(`${itemLabel} must be an object`);
      continue;
    }
    if (!meaningful(commit.repository)) errors.push(`${itemLabel}.repository is required`);
    else if (knownRepositories.size > 0 && !knownRepositories.has(commit.repository)) {
      errors.push(`${itemLabel}.repository is not listed in repositories`);
    }
    if (!isFullSha(commit.full_sha)) errors.push(`${itemLabel}.full_sha must be a full SHA`);
    if (!allowMultiplePerRepository && seenRepositories.has(commit.repository)) {
      errors.push(`${label} must contain at most one commit per repository`);
    }
    seenRepositories.add(commit.repository);
    tokens.push(`${commit.repository}@${commit.full_sha}`);
  }
  return [...new Set(tokens)].sort();
}

function validateImmutableReferences(errors, data, { requireContracts = false } = {}) {
  const immutable = addRequiredObject(errors, data.immutable_references, "immutable_references");
  const contractTokens = [];
  const fixtureTokens = [];
  if (!immutable) return { contractTokens, fixtureTokens };
  if (!Array.isArray(immutable.contracts)) errors.push("immutable_references.contracts must be an array");
  else {
    if (requireContracts && immutable.contracts.length === 0) {
      errors.push("immutable_references.contracts must not be empty when contract_impact is not none");
    }
    const ids = new Set();
    for (const [index, contract] of immutable.contracts.entries()) {
      const label = `immutable_references.contracts[${index}]`;
      if (!asObject(contract)) {
        errors.push(`${label} must be an object`);
        continue;
      }
      if (!meaningful(contract.id)) errors.push(`${label}.id is required`);
      if (ids.has(contract.id)) errors.push(`${label}.id must be unique`);
      ids.add(contract.id);
      if (!meaningful(contract.version)) errors.push(`${label}.version is required`);
      if (!isFullSha(contract.full_commit)) errors.push(`${label}.full_commit must be a full SHA`);
      if (!isSha256(contract.digest)) errors.push(`${label}.digest must be SHA-256`);
      if (!meaningful(contract.generator)) errors.push(`${label}.generator is required`);
      contractTokens.push(
        `contract:${contract.id}@${contract.version}@${contract.full_commit}#${contract.digest}`,
      );
    }
  }
  if (!Array.isArray(immutable.fixtures)) errors.push("immutable_references.fixtures must be an array");
  else {
    const ids = new Set();
    for (const [index, fixture] of immutable.fixtures.entries()) {
      const label = `immutable_references.fixtures[${index}]`;
      if (!asObject(fixture)) {
        errors.push(`${label} must be an object`);
        continue;
      }
      if (!meaningful(fixture.id)) errors.push(`${label}.id is required`);
      if (ids.has(fixture.id)) errors.push(`${label}.id must be unique`);
      ids.add(fixture.id);
      if (!isSha256(fixture.digest)) errors.push(`${label}.digest must be SHA-256`);
      fixtureTokens.push(`fixture:${fixture.id}#${fixture.digest}`);
    }
  }
  return {
    contractTokens: [...new Set(contractTokens)].sort(),
    fixtureTokens: [...new Set(fixtureTokens)].sort(),
  };
}

function validateEvidenceBlock(errors, block, label) {
  const evidence = addRequiredObject(errors, block, label);
  if (!evidence) return;
  if (typeof evidence.required !== "boolean") {
    errors.push(`${label}.required must be boolean`);
    return;
  }
  if (evidence.required) {
    if (!isPass(evidence.status)) errors.push(`${label}.status must be PASS when required`);
    if (!meaningful(evidence.command)) errors.push(`${label}.command is required when required`);
    if (!meaningful(evidence.environment)) errors.push(`${label}.environment is required when required`);
    if (evidence.exit_code !== 0) errors.push(`${label}.exit_code must equal 0 when required`);
    if (!isIsoInstant(evidence.verified_at)) {
      errors.push(`${label}.verified_at must be an ISO-8601 instant when required`);
    }
    validateEvidenceRefs(errors, evidence.refs, `${label}.refs`, true);
  } else {
    if (!isNotApplicable(evidence.status)) errors.push(`${label}.status must be N/A when not required`);
    validateException(errors, evidence.exception, `${label}.exception`);
    validateEvidenceRefs(errors, evidence.refs ?? [], `${label}.refs`, false);
  }
}

function validateHarnessBase(errors, harnesses) {
  if (!Array.isArray(harnesses)) {
    errors.push("runtime_harnesses must be an array");
    return new Map();
  }
  const byId = new Map();
  for (const [index, harness] of harnesses.entries()) {
    const label = `runtime_harnesses[${index}]`;
    if (!asObject(harness)) {
      errors.push(`${label} must be an object`);
      continue;
    }
    if (!meaningful(harness.id)) {
      errors.push(`${label}.id is required`);
      continue;
    }
    if (byId.has(harness.id)) errors.push(`duplicate harness id: ${harness.id}`);
    byId.set(harness.id, harness);
    const classes = Array.isArray(harness.failure_classes) ? [...harness.failure_classes].sort() : [];
    if (JSON.stringify(classes) !== JSON.stringify(FAILURE_CLASSES)) {
      errors.push(`${label}.failure_classes must contain exactly the four closed classes`);
    }
    if (harness.default_enabled !== false) errors.push(`${label}.default_enabled must be false`);
  }
  return byId;
}

function validateControl(errors, control, label) {
  const value = addRequiredObject(errors, control, label);
  if (!value) return;
  if (!isPass(value.status)) errors.push(`${label}.status must be PASS`);
  validateEvidenceRef(errors, value.evidence_ref, `${label}.evidence_ref`);
}

function validateHarnessQualified(errors, harness, label) {
  if (!harness) {
    errors.push(`${label} references a missing harness`);
    return;
  }
  if (!meaningful(harness.real_platform)) errors.push(`${label}.real_platform is required`);
  if (!isFullSha(harness.commit)) errors.push(`${label}.commit must be a full SHA`);
  if (!isSha256(harness.digest)) errors.push(`${label}.digest must be a SHA-256 digest`);
  if (harness.production_bootstrap !== true) errors.push(`${label}.production_bootstrap must be true`);
  if (!meaningful(harness.representative_data)) errors.push(`${label}.representative_data is required`);
  const qualification = addRequiredObject(errors, harness.qualification, `${label}.qualification`);
  if (!qualification) return;
  if (!isPass(qualification.status)) errors.push(`${label}.qualification.status must be PASS`);
  if (!isIsoInstant(qualification.verified_at)) {
    errors.push(`${label}.qualification.verified_at must be an ISO-8601 instant`);
  }
  if (!meaningful(qualification.command)) errors.push(`${label}.qualification.command is required`);
  if (!meaningful(qualification.environment)) errors.push(`${label}.qualification.environment is required`);
  if (qualification.exit_code !== 0) errors.push(`${label}.qualification.exit_code must equal 0`);
  validateControl(errors, qualification.positive_control, `${label}.qualification.positive_control`);
  const negatives = addRequiredObject(
    errors,
    qualification.negative_controls,
    `${label}.qualification.negative_controls`,
  );
  if (negatives) {
    if (JSON.stringify(Object.keys(negatives).sort()) !== JSON.stringify(FAILURE_CLASSES)) {
      errors.push(`${label}.qualification.negative_controls must contain exactly four controls`);
    }
    for (const failureClass of FAILURE_CLASSES) {
      const control = addRequiredObject(
        errors,
        negatives[failureClass],
        `${label}.qualification.negative_controls.${failureClass}`,
      );
      if (!control) continue;
      if (!isPass(control.status)) {
        errors.push(`${label}.qualification.negative_controls.${failureClass}.status must be PASS`);
      }
      if (normalized(control.observed_class) !== failureClass) {
        errors.push(
          `${label}.qualification.negative_controls.${failureClass}.observed_class must equal ${failureClass}`,
        );
      }
      validateEvidenceRef(
        errors,
        control.evidence_ref,
        `${label}.qualification.negative_controls.${failureClass}.evidence_ref`,
      );
    }
  }
  for (const control of ["timeout_control", "cleanup_control", "content_free_verdict"]) {
    validateControl(errors, qualification[control], `${label}.qualification.${control}`);
  }
}

function validateHarnessBinding(errors, binding, harnesses, label) {
  const value = addRequiredObject(errors, binding, label);
  if (!value) return null;
  if (!meaningful(value.id)) {
    errors.push(`${label}.id is required`);
    return null;
  }
  const harness = harnesses.get(value.id);
  if (!harness) {
    errors.push(`${label}.id references a missing harness`);
    return null;
  }
  if (value.commit !== harness.commit) errors.push(`${label}.commit must match the qualified harness`);
  if (value.digest !== harness.digest) errors.push(`${label}.digest must match the qualified harness`);
  return harness;
}

function validateFreshness(errors, freshness, label, context, expectedCommits, needsVertical) {
  const value = addRequiredObject(errors, freshness, label);
  if (!value) return;
  if (!isIsoInstant(value.verified_at)) errors.push(`${label}.verified_at must be an ISO-8601 instant`);
  const actualCommits = validateCommitList(errors, value.commits, `${label}.commits`, context.data, {
    allowMultiplePerRepository: true,
  });
  exactSet(errors, actualCommits, expectedCommits, `${label}.commits`);
  exactSet(errors, value.contract_refs, context.contractTokens, `${label}.contract_refs`);
  exactSet(errors, value.fixture_refs, context.fixtureTokens, `${label}.fixture_refs`);
  if (needsVertical) {
    const harness = validateHarnessBinding(errors, value.harness, context.harnesses, `${label}.harness`);
    if (harness) {
      validateHarnessQualified(errors, harness, `runtime_harnesses.${harness.id}`);
      if (value.platform !== harness.real_platform) {
        errors.push(`${label}.platform must match the qualified harness real platform`);
      }
    }
    if (value.production_bootstrap !== true) errors.push(`${label}.production_bootstrap must be true`);
  }
  if (!meaningful(value.invalidation_rule)) errors.push(`${label}.invalidation_rule is required`);
}

function validateSliceGraph(errors, slices, planningComplete) {
  if (!Array.isArray(slices) || slices.length === 0) {
    errors.push("slices must contain at least one slice");
    return new Map();
  }
  const byId = new Map();
  for (const [index, slice] of slices.entries()) {
    const label = `slices[${index}]`;
    if (!asObject(slice) || !meaningful(slice.id)) {
      errors.push(`${label}.id is required`);
      continue;
    }
    if (byId.has(slice.id)) errors.push(`duplicate slice id: ${slice.id}`);
    byId.set(slice.id, slice);
    if (!Array.isArray(slice.prerequisites)) errors.push(`${label}.prerequisites must be an array`);
    if (typeof slice.required !== "boolean") errors.push(`${label}.required must be boolean`);
    if (!SLICE_STATUSES.has(normalized(slice.status))) errors.push(`${label}.status is invalid`);
    if (planningComplete) {
      if (!meaningful(slice.intent)) errors.push(`${label}.intent is required by G2`);
      for (const evidenceKey of ["local_evidence", "boundary_evidence", "vertical_evidence"]) {
        const evidence = addRequiredObject(errors, slice[evidenceKey], `${label}.${evidenceKey}`);
        if (evidence && typeof evidence.required !== "boolean") {
          errors.push(`${label}.${evidenceKey}.required must be boolean`);
        }
        if (evidenceKey === "local_evidence" && evidence?.required !== true) {
          errors.push(`${label}.local_evidence.required must be true for every implemented slice`);
        }
        if (evidence?.required === false) {
          validateException(errors, evidence.exception, `${label}.${evidenceKey}.exception`);
        } else if (evidence && !meaningful(evidence.reason)) {
          errors.push(`${label}.${evidenceKey}.reason is required by G2`);
        }
      }
    }
  }
  for (const slice of byId.values()) {
    for (const prerequisite of slice.prerequisites ?? []) {
      if (!byId.has(prerequisite) && !GATE_PREREQUISITES.has(prerequisite)) {
        errors.push(`slice ${slice.id} has unknown prerequisite: ${prerequisite}`);
      }
    }
  }
  const visiting = new Set();
  const visited = new Set();
  function visit(id) {
    if (visiting.has(id)) {
      errors.push(`slice prerequisite cycle includes: ${id}`);
      return;
    }
    if (visited.has(id)) return;
    visiting.add(id);
    for (const prerequisite of byId.get(id)?.prerequisites ?? []) {
      if (byId.has(prerequisite)) visit(prerequisite);
    }
    visiting.delete(id);
    visited.add(id);
  }
  for (const id of byId.keys()) visit(id);
  return byId;
}

function validateTemporalContract(errors, data, complete) {
  const matrix = addRequiredObject(errors, data.temporal_contract_matrix, "temporal_contract_matrix");
  if (!matrix) return;
  if (typeof matrix.required !== "boolean") {
    errors.push("temporal_contract_matrix.required must be boolean");
    return;
  }
  if (!matrix.required) {
    if (obviousG2VTrigger(data)) {
      errors.push("temporal_contract_matrix cannot be N/A for an evident high-risk/cross-boundary trigger");
    }
    if (complete) validateException(errors, matrix.exception, "temporal_contract_matrix.exception");
    return;
  }
  if (complete && !meaningful(matrix.applicability_reason)) {
    errors.push("temporal_contract_matrix.applicability_reason is required by G2");
  }
  const phases = addRequiredObject(errors, matrix.phases, "temporal_contract_matrix.phases");
  const requiredPhases = new Set();
  const naPhases = new Set();
  if (phases) {
    if (JSON.stringify(Object.keys(phases).sort()) !== JSON.stringify(TEMPORAL_PHASES)) {
      errors.push(
        "temporal_contract_matrix.phases must contain exactly producer/persistence/notification/replay/terminal/cleanup",
      );
    }
    for (const phase of TEMPORAL_PHASES) {
      const value = addRequiredObject(errors, phases[phase], `temporal_contract_matrix.phases.${phase}`);
      if (!value) continue;
      const status = normalized(value.status);
      if (status === "required") requiredPhases.add(phase);
      else if (["n/a", "not_applicable"].includes(status)) {
        naPhases.add(phase);
        if (complete) {
          validateException(
            errors,
            asObject(matrix.phase_exceptions)?.[phase],
            `temporal_contract_matrix.phase_exceptions.${phase}`,
          );
        }
      } else errors.push(`temporal_contract_matrix.phases.${phase}.status must be required or N/A`);
    }
  }
  if (!asObject(matrix.phase_exceptions)) {
    errors.push("temporal_contract_matrix.phase_exceptions must be an object");
  }
  if (complete) {
    const scope = asObject(data.scope) ?? {};
    const mandatory = new Set(["producer", "cleanup"]);
    if (!["none", ""].includes(normalized(scope.database_change))) {
      mandatory.add("persistence");
      mandatory.add("terminal");
    }
    if (!["none", ""].includes(normalized(scope.persistence_change))) {
      mandatory.add("persistence");
      mandatory.add("terminal");
    }
    if (normalized(scope.persistence_change) === "replay") mandatory.add("replay");
    if (
      (Array.isArray(data.repositories) && data.repositories.length > 1) ||
      !["none", ""].includes(normalized(scope.contract_impact)) ||
      !["none", ""].includes(normalized(scope.runtime_change)) ||
      normalized(scope.user_workflow_change) === "user_visible"
    ) {
      mandatory.add("notification");
      mandatory.add("terminal");
    }
    for (const phase of mandatory) {
      if (!requiredPhases.has(phase)) {
        errors.push(`temporal phase ${phase} must be required for the declared scope`);
      }
    }
  }
  const scenarioIds = new Set();
  const covered = new Set();
  const edges = new Map(TEMPORAL_PHASES.map((phase) => [phase, new Set()]));
  if (!Array.isArray(matrix.scenarios) || matrix.scenarios.length === 0) {
    errors.push("temporal_contract_matrix.scenarios must not be empty");
  } else {
    for (const [index, scenario] of matrix.scenarios.entries()) {
      const label = `temporal_contract_matrix.scenarios[${index}]`;
      if (!asObject(scenario) || !meaningful(scenario.id)) {
        errors.push(`${label}.id is required`);
        continue;
      }
      if (scenarioIds.has(scenario.id)) errors.push(`${label}.id must be unique`);
      scenarioIds.add(scenario.id);
      if (!Array.isArray(scenario.ordered_phases) || scenario.ordered_phases.length < 2) {
        errors.push(`${label}.ordered_phases must contain at least two phases`);
        continue;
      }
      if (new Set(scenario.ordered_phases).size !== scenario.ordered_phases.length) {
        errors.push(`${label}.ordered_phases must not repeat a phase`);
      }
      for (const [phaseIndex, phase] of scenario.ordered_phases.entries()) {
        if (!TEMPORAL_PHASES.includes(phase)) errors.push(`${label} references unknown phase: ${phase}`);
        else {
          covered.add(phase);
          if (naPhases.has(phase)) errors.push(`${label} references N/A phase: ${phase}`);
          const next = scenario.ordered_phases[phaseIndex + 1];
          if (TEMPORAL_PHASES.includes(next)) edges.get(phase).add(next);
        }
      }
    }
  }
  for (const phase of requiredPhases) {
    if (!covered.has(phase)) errors.push(`required temporal phase is absent from all scenarios: ${phase}`);
  }
  const visiting = new Set();
  const visited = new Set();
  function visit(phase) {
    if (visiting.has(phase)) {
      errors.push(`temporal scenario order contains a cycle at: ${phase}`);
      return;
    }
    if (visited.has(phase)) return;
    visiting.add(phase);
    for (const next of edges.get(phase) ?? []) visit(next);
    visiting.delete(phase);
    visited.add(phase);
  }
  for (const phase of TEMPORAL_PHASES) visit(phase);
  const sliceIds = new Set((data.slices ?? []).map((slice) => slice.id));
  const referencedTestIds = new Set();
  const invariantTestRefs = new Map();
  const invariantSliceRefs = new Map();
  if (!Array.isArray(matrix.invariants) || matrix.invariants.length === 0) {
    errors.push("temporal_contract_matrix.invariants must not be empty");
  } else {
    const invariantIds = new Set();
    for (const [index, invariant] of matrix.invariants.entries()) {
      const label = `temporal_contract_matrix.invariants[${index}]`;
      if (!asObject(invariant) || !meaningful(invariant.id)) {
        errors.push(`${label}.id is required`);
        continue;
      }
      if (invariantIds.has(invariant.id)) errors.push(`${label}.id must be unique`);
      invariantIds.add(invariant.id);
      if (complete && !meaningful(invariant.statement)) errors.push(`${label}.statement is required`);
      if (!Array.isArray(invariant.scenario_ids) || invariant.scenario_ids.length === 0) {
        errors.push(`${label}.scenario_ids must not be empty`);
      } else {
        for (const id of invariant.scenario_ids) {
          if (!scenarioIds.has(id)) errors.push(`${label}.scenario_ids references unknown scenario: ${id}`);
        }
      }
      if (!Array.isArray(invariant.slice_ids) || invariant.slice_ids.length === 0) {
        errors.push(`${label}.slice_ids must not be empty`);
      } else {
        invariantSliceRefs.set(invariant.id, [...invariant.slice_ids]);
        if (new Set(invariant.slice_ids).size !== invariant.slice_ids.length) {
          errors.push(`${label}.slice_ids must not contain duplicates`);
        }
        for (const sliceId of invariant.slice_ids) {
          if (!sliceIds.has(sliceId)) errors.push(`${label}.slice_ids references unknown slice: ${sliceId}`);
          else if ((data.slices ?? []).find((slice) => slice.id === sliceId)?.required !== true) {
            errors.push(`${label}.slice_ids must reference required slices: ${sliceId}`);
          }
        }
      }
      if (!Array.isArray(invariant.executable_tests) || invariant.executable_tests.length === 0) {
        errors.push(`${label}.executable_tests must not be empty`);
      } else {
        invariantTestRefs.set(invariant.id, [...invariant.executable_tests]);
        for (const testId of invariant.executable_tests) {
          referencedTestIds.add(testId);
          if (!/^TCONF-[A-Z0-9._-]+$/.test(testId)) {
            errors.push(`${label}.executable_tests contains invalid test id: ${testId}`);
          }
        }
      }
    }
  }
  const testIds = new Set();
  const requiredTestIds = new Set();
  const executableById = new Map();
  if (!Array.isArray(matrix.executable_tests) || matrix.executable_tests.length === 0) {
    errors.push("temporal_contract_matrix.executable_tests must not be empty");
  } else {
    for (const [index, executable] of matrix.executable_tests.entries()) {
      const label = `temporal_contract_matrix.executable_tests[${index}]`;
      if (!asObject(executable) || !/^TCONF-[A-Z0-9._-]+$/.test(executable.id ?? "")) {
        errors.push(`${label}.id must be a TCONF-* id`);
        continue;
      }
      if (testIds.has(executable.id)) errors.push(`${label}.id must be unique`);
      testIds.add(executable.id);
      executableById.set(executable.id, executable);
      if (typeof executable.required !== "boolean") errors.push(`${label}.required must be boolean`);
      if (executable.required === true) requiredTestIds.add(executable.id);
      if (complete) {
        if (!repositorySet(data).has(executable.repository)) {
          errors.push(`${label}.repository must be listed in repositories`);
        }
        if (!meaningful(executable.command)) errors.push(`${label}.command is required by G2`);
        if (!sliceIds.has(executable.slice_id)) errors.push(`${label}.slice_id references an unknown slice`);
        else if (
          executable.required === true &&
          (data.slices ?? []).find((slice) => slice.id === executable.slice_id)?.required !== true
        ) {
          errors.push(`${label}.required test must belong to a required slice`);
        }
        if (executable.required === false) validateException(errors, executable.exception, `${label}.exception`);
      }
    }
  }
  for (const id of referencedTestIds) {
    if (!testIds.has(id)) errors.push(`temporal invariant references missing executable test: ${id}`);
  }
  for (const id of testIds) {
    if (!referencedTestIds.has(id)) errors.push(`temporal executable test is not referenced by an invariant: ${id}`);
  }
  for (const [invariantId, testRefs] of invariantTestRefs) {
    if (!testRefs.some((testId) => requiredTestIds.has(testId))) {
      errors.push(`temporal invariant ${invariantId} must reference at least one required executable test`);
    }
    for (const sliceId of invariantSliceRefs.get(invariantId) ?? []) {
      const hasSliceTest = testRefs.some((testId) => {
        const executable = executableById.get(testId);
        return executable?.required === true && executable.slice_id === sliceId;
      });
      if (!hasSliceTest) {
        errors.push(
          `temporal invariant ${invariantId} must reference a required executable test for slice ${sliceId}`,
        );
      }
    }
  }
}

function validateAttempt(errors, attempt, label, incident) {
  if (!asObject(attempt)) {
    errors.push(`${label} must be an object`);
    return;
  }
  if (!meaningful(attempt.run_id)) errors.push(`${label}.run_id is required`);
  if (!isIsoInstant(attempt.occurred_at)) errors.push(`${label}.occurred_at must be an ISO-8601 instant`);
  if (!isFail(attempt.result)) errors.push(`${label}.result must be FAIL`);
  if (normalized(attempt.failure_class) !== normalized(incident.failure_class)) {
    errors.push(`${label}.failure_class must match the incident fingerprint`);
  }
  if (attempt.failure_code !== incident.failure_code) {
    errors.push(`${label}.failure_code must match the incident fingerprint`);
  }
  if (attempt.checkpoint !== incident.checkpoint) {
    errors.push(`${label}.checkpoint must match the incident fingerprint`);
  }
  validateEvidenceRef(errors, attempt.evidence_ref, `${label}.evidence_ref`);
}

function validateRcaCycle(errors, cycle, label, incident) {
  if (!asObject(cycle)) {
    errors.push(`${label} must be an object`);
    return;
  }
  if (!meaningful(cycle.id)) errors.push(`${label}.id is required`);
  const audit = addRequiredObject(errors, cycle.audit, `${label}.audit`);
  if (audit) {
    if (normalized(audit.status) !== "complete") errors.push(`${label}.audit.status must be complete`);
    for (const field of ["expanded_scope", "candidates", "discriminating_evidence_refs"]) {
      if (!Array.isArray(audit[field]) || audit[field].length === 0) {
        errors.push(`${label}.audit.${field} must not be empty`);
      }
    }
    for (const [index, ref] of (audit.discriminating_evidence_refs ?? []).entries()) {
      validateEvidenceRef(errors, ref, `${label}.audit.discriminating_evidence_refs[${index}]`);
    }
    if (!meaningful(audit.approved_next_action)) {
      errors.push(`${label}.audit.approved_next_action is required`);
    }
    if (!meaningful(audit.approved_by)) errors.push(`${label}.audit.approved_by is required`);
    if (!isIsoInstant(audit.approved_at)) {
      errors.push(`${label}.audit.approved_at must be an ISO-8601 instant`);
    }
  }
  const authorization = addRequiredObject(errors, cycle.authorization, `${label}.authorization`);
  if (authorization) {
    if (authorization.max_attempts !== 1) errors.push(`${label}.authorization.max_attempts must equal 1`);
    if (!meaningful(authorization.action)) errors.push(`${label}.authorization.action is required`);
    if (!meaningful(authorization.approved_by)) errors.push(`${label}.authorization.approved_by is required`);
    if (!isIsoInstant(authorization.approved_at)) {
      errors.push(`${label}.authorization.approved_at must be an ISO-8601 instant`);
    }
    if (audit && authorization.action !== audit.approved_next_action) {
      errors.push(`${label}.authorization.action must equal the RCA approved next action`);
    }
  }
  if (cycle.attempt !== null && cycle.attempt !== undefined) {
    const attempt = cycle.attempt;
    if (!asObject(attempt)) errors.push(`${label}.attempt must be an object or null`);
    else {
      if (!meaningful(attempt.run_id)) errors.push(`${label}.attempt.run_id is required`);
      if (!isIsoInstant(attempt.occurred_at)) {
        errors.push(`${label}.attempt.occurred_at must be an ISO-8601 instant`);
      }
      if (!["pass", "fail"].includes(normalized(attempt.result))) {
        errors.push(`${label}.attempt.result must be PASS or FAIL`);
      }
      if (isFail(attempt.result)) {
        if (attempt.failure_code !== incident.failure_code) {
          errors.push(`${label}.attempt.failure_code must match the incident after a repeated failure`);
        }
        if (attempt.checkpoint !== incident.checkpoint) {
          errors.push(`${label}.attempt.checkpoint must match the incident after a repeated failure`);
        }
      }
      validateEvidenceRef(errors, attempt.evidence_ref, `${label}.attempt.evidence_ref`);
    }
  }
}

function validateFailureFuse(errors, breaker) {
  const value = addRequiredObject(errors, breaker, "failure_circuit_breaker");
  if (!value) return;
  if (value.same_failure_threshold !== 3) {
    errors.push("failure_circuit_breaker.same_failure_threshold must equal 3");
  }
  if (!Array.isArray(value.incidents)) {
    errors.push("failure_circuit_breaker.incidents must be an array");
    return;
  }
  const ids = new Set();
  const fingerprints = new Set();
  const equivalenceKeys = new Set();
  for (const [index, incident] of value.incidents.entries()) {
    const label = `failure_circuit_breaker.incidents[${index}]`;
    if (!asObject(incident)) {
      errors.push(`${label} must be an object`);
      continue;
    }
    if (!meaningful(incident.id)) errors.push(`${label}.id is required`);
    if (ids.has(incident.id)) errors.push(`${label}.id must be unique`);
    ids.add(incident.id);
    for (const field of ["slice_id", "gate_id", "evidence_id", "failure_code", "checkpoint"]) {
      if (!meaningful(incident[field])) errors.push(`${label}.${field} is required`);
    }
    if (!FAILURE_CLASSES.includes(normalized(incident.failure_class))) {
      errors.push(`${label}.failure_class must use the closed harness taxonomy`);
    }
    const expectedFingerprint = [
      incident.slice_id,
      incident.gate_id,
      incident.evidence_id,
      normalized(incident.failure_class),
      incident.failure_code,
      incident.checkpoint,
    ].join("|");
    if (incident.fingerprint !== expectedFingerprint) {
      errors.push(`${label}.fingerprint must exactly derive from slice/gate/evidence/class/code/checkpoint`);
    }
    if (fingerprints.has(incident.fingerprint)) errors.push(`${label}.fingerprint must be unique`);
    fingerprints.add(incident.fingerprint);
    const equivalenceKey = [
      incident.slice_id,
      incident.gate_id,
      normalized(incident.failure_class),
      incident.failure_code,
      incident.checkpoint,
    ].join("|");
    if (equivalenceKeys.has(equivalenceKey)) {
      errors.push(
        `${label} splits one equivalent failure across incidents; evidence_id changes do not reset the fuse`,
      );
    }
    equivalenceKeys.add(equivalenceKey);
    if (!Array.isArray(incident.attempts) || incident.attempts.length === 0) {
      errors.push(`${label}.attempts must not be empty`);
      continue;
    }
    if (incident.attempts.length > 3) errors.push(`${label}.attempts cannot exceed the threshold of 3`);
    const runIds = new Set();
    for (const [attemptIndex, attempt] of incident.attempts.entries()) {
      validateAttempt(errors, attempt, `${label}.attempts[${attemptIndex}]`, incident);
      if (runIds.has(attempt?.run_id)) errors.push(`${label}.attempts run_id must be unique`);
      runIds.add(attempt?.run_id);
    }
    const cycles = Array.isArray(incident.rca_cycles) ? incident.rca_cycles : [];
    if (!Array.isArray(incident.rca_cycles)) errors.push(`${label}.rca_cycles must be an array`);
    const cycleIds = new Set();
    for (const [cycleIndex, cycle] of cycles.entries()) {
      validateRcaCycle(errors, cycle, `${label}.rca_cycles[${cycleIndex}]`, incident);
      if (cycleIds.has(cycle?.id)) errors.push(`${label}.rca_cycles id must be unique`);
      cycleIds.add(cycle?.id);
      if (cycle?.attempt?.run_id && runIds.has(cycle.attempt.run_id)) {
        errors.push(`${label} run_id must be unique across all attempts`);
      }
      if (cycle?.attempt?.run_id) runIds.add(cycle.attempt.run_id);
      if (cycleIndex < cycles.length - 1 && !isFail(cycle?.attempt?.result)) {
        errors.push(`${label}.rca_cycles may continue only after the prior authorized attempt failed`);
      }
    }
    const state = normalized(incident.state);
    if (incident.attempts.length < 3) {
      if (state !== "armed") errors.push(`${label}.state must be armed before the third failure`);
      if (cycles.length > 0) errors.push(`${label}.rca_cycles cannot start before the third failure`);
      continue;
    }
    const lastCycle = cycles.at(-1);
    const expectedState =
      cycles.length === 0 || isFail(lastCycle?.attempt?.result)
        ? "rca_required"
        : lastCycle?.attempt == null
          ? "authorized_once"
          : isPass(lastCycle.attempt.result)
            ? "resolved"
            : "rca_required";
    if (state !== expectedState) errors.push(`${label}.state must be ${expectedState}`);
  }
}

function validateNoOpenBreaker(errors, breaker, gateLabel) {
  for (const incident of breaker?.incidents ?? []) {
    if (["rca_required", "authorized_once"].includes(normalized(incident.state))) {
      errors.push(`open ${incident.state} incident blocks ${gateLabel}: ${incident.id ?? "unknown"}`);
    }
  }
}

function validateV2Base(data, errors, gate) {
  const gates = addRequiredObject(errors, data.gates, "gates");
  if (gates) {
    for (const key of Object.values(GATE_KEYS)) {
      if (!(key in gates)) errors.push(`gates.${key} is required`);
      else if (!GATE_STATUSES.has(normalized(gates[key]))) errors.push(`gates.${key} is invalid`);
    }
    if ("G3_slice_complete" in gates) {
      errors.push("schema v2 forbids aggregate gates.G3_slice_complete; use slices[]");
    }
  }
  if (asObject(data.documents)?.temporal_contract !== "04A-temporal-contract-matrix.md") {
    errors.push("documents.temporal_contract must reference 04A-temporal-contract-matrix.md");
  }
  if (asObject(data.documents)?.verification !== "08-verification-report.md") {
    errors.push("documents.verification must reference 08-verification-report.md");
  }
  const planningComplete = ["G2", "G2A", "G2V", "G3", "G4", "G5", "G6"].includes(gate);
  if (["G0", "G1", "G2", "G2A", "G2V", "G3", "G4", "G5", "G6"].includes(gate)) {
    validateFeatureIdentity(errors, data);
  }
  if (["G1", "G2", "G2A", "G2V", "G3", "G4", "G5", "G6"].includes(gate)) {
    validatePlanningScope(errors, data);
  }
  const impact = normalized(asObject(data.scope)?.contract_impact);
  const immutable = validateImmutableReferences(errors, data, {
    requireContracts: ["G2A", "G2V", "G3", "G4", "G5", "G6"].includes(gate) && impact !== "none",
  });
  const feasibility = addRequiredObject(errors, data.vertical_feasibility, "vertical_feasibility");
  if (feasibility && typeof feasibility.required !== "boolean") {
    errors.push("vertical_feasibility.required must be boolean");
  }
  if (feasibility?.required === false && obviousG2VTrigger(data)) {
    errors.push("vertical_feasibility cannot be N/A for an evident high-risk/cross-boundary trigger");
  }
  if (planningComplete && feasibility && !meaningful(feasibility.applicability_reason)) {
    errors.push("vertical_feasibility.applicability_reason is required by G2");
  }
  if (planningComplete && feasibility?.required === false) {
    validateException(errors, feasibility.exception, "vertical_feasibility.exception");
  }
  const harnesses = validateHarnessBase(errors, data.runtime_harnesses);
  const slices = validateSliceGraph(errors, data.slices, planningComplete);
  if (planningComplete) {
    for (const slice of slices.values()) {
      if (boundaryEvidenceRequired(data) && slice.boundary_evidence?.required !== true) {
        errors.push(`slice ${slice.id}.boundary_evidence.required must be true for the declared boundary scope`);
      }
      if (feasibility?.required === true && slice.vertical_evidence?.required !== true) {
        errors.push(`slice ${slice.id}.vertical_evidence.required must be true when G2V is required`);
      }
    }
  }
  validateTemporalContract(errors, data, planningComplete);
  validateFailureFuse(errors, data.failure_circuit_breaker);
  const finalE2E = addRequiredObject(errors, data.final_e2e, "final_e2e");
  if (finalE2E) {
    for (const key of FINAL_E2E_KEYS) {
      const verdict = addRequiredObject(errors, finalE2E[key], `final_e2e.${key}`);
      if (verdict && typeof verdict.required !== "boolean") {
        errors.push(`final_e2e.${key}.required must be boolean`);
      }
    }
    const scope = asObject(data.scope) ?? {};
    if (obviousG2VTrigger(data) && finalE2E.core_vertical?.required !== true) {
      errors.push("final_e2e.core_vertical is required for a high-risk/cross-boundary feature");
    }
    if (!["none", "tbd", ""].includes(normalized(scope.ui_change))) {
      if (finalE2E.accessibility_visual?.required !== true) {
        errors.push("final_e2e.accessibility_visual is required when scope.ui_change is visual/interactive");
      }
    }
    const teardownTrigger = [scope.database_change, scope.persistence_change, scope.runtime_change].some(
      (value) => !["", "none", "tbd"].includes(normalized(value)),
    );
    if (teardownTrigger && finalE2E.teardown?.required !== true) {
      errors.push("final_e2e.teardown is required for persistence/runtime changes");
    }
  }
  return { data, feasibility, harnesses, slices, finalE2E, ...immutable };
}

function validateG2A(errors, data) {
  validateDesignGateChain(errors, data, "G2");
  const impact = normalized(asObject(data.scope)?.contract_impact);
  if (impact === "none") {
    if (!isNotApplicable(gateStatus(data, "G2A"))) {
      errors.push("gate G2A must be not_applicable when contract_impact is none");
    }
    if (!meaningful(asObject(data.gate_reasons)?.G2A)) errors.push("gate_reasons.G2A is required");
  } else if (!isPass(gateStatus(data, "G2A"))) {
    errors.push("gate G2A must be pass when contract_impact is not none");
  }
}

function validateG2V(errors, data, context) {
  validateNoOpenBreaker(errors, data.failure_circuit_breaker, "G2V");
  validateG2A(errors, data);
  const feasibility = context.feasibility;
  if (!feasibility) return;
  if (!feasibility.required) {
    if (!isNotApplicable(gateStatus(data, "G2V"))) errors.push("gate G2V must be not_applicable");
    validateException(errors, feasibility.exception, "vertical_feasibility.exception");
    return;
  }
  validateGatePassed(errors, data, "G2V");
  if (!meaningful(feasibility.platform)) errors.push("vertical_feasibility.platform is required");
  if (feasibility.production_bootstrap !== true) {
    errors.push("vertical_feasibility.production_bootstrap must be true");
  }
  if (!meaningful(feasibility.representative_data)) {
    errors.push("vertical_feasibility.representative_data is required");
  }
  if (!meaningful(feasibility.critical_path)) errors.push("vertical_feasibility.critical_path is required");
  if (!Array.isArray(feasibility.participating_repositories) || feasibility.participating_repositories.length === 0) {
    errors.push("vertical_feasibility.participating_repositories must not be empty");
  } else {
    const known = repositorySet(data);
    for (const repository of feasibility.participating_repositories) {
      if (!known.has(repository)) {
        errors.push(`vertical_feasibility participating repository is not declared: ${repository}`);
      }
    }
  }
  const evidence = addRequiredObject(errors, feasibility.evidence, "vertical_feasibility.evidence");
  if (evidence) {
    if (!isPass(evidence.status)) errors.push("vertical_feasibility.evidence.status must be PASS");
    const commits = validateCommitList(
      errors,
      evidence.commits,
      "vertical_feasibility.evidence.commits",
      data,
    );
    const expectedRepos = [...new Set(feasibility.participating_repositories ?? [])].sort();
    exactSet(
      errors,
      commits.map((token) => token.slice(0, token.indexOf("@"))),
      expectedRepos,
      "vertical_feasibility.evidence commit repositories",
    );
    if (!meaningful(evidence.command)) errors.push("vertical_feasibility.evidence.command is required");
    if (!meaningful(evidence.environment)) errors.push("vertical_feasibility.evidence.environment is required");
    if (evidence.exit_code !== 0) errors.push("vertical_feasibility.evidence.exit_code must equal 0");
    if (!isIsoInstant(evidence.verified_at)) {
      errors.push("vertical_feasibility.evidence.verified_at must be an ISO-8601 instant");
    }
    if (evidence.platform !== feasibility.platform) {
      errors.push("vertical_feasibility.evidence.platform must match vertical_feasibility.platform");
    }
    if (evidence.production_bootstrap !== true) {
      errors.push("vertical_feasibility.evidence.production_bootstrap must be true");
    }
    exactSet(errors, evidence.contract_refs, context.contractTokens, "vertical_feasibility.evidence.contract_refs");
    exactSet(errors, evidence.fixture_refs, context.fixtureTokens, "vertical_feasibility.evidence.fixture_refs");
    validateEvidenceRefs(errors, evidence.refs, "vertical_feasibility.evidence.refs", true);
    const harness = validateHarnessBinding(
      errors,
      evidence.harness,
      context.harnesses,
      "vertical_feasibility.evidence.harness",
    );
    if (harness && harness.id !== feasibility.harness_id) {
      errors.push("vertical_feasibility.evidence.harness.id must equal vertical_feasibility.harness_id");
    }
  }
  const qualifiedHarness = context.harnesses.get(feasibility.harness_id);
  validateHarnessQualified(
    errors,
    qualifiedHarness,
    `runtime_harnesses.${feasibility.harness_id}`,
  );
  if (qualifiedHarness) {
    if (feasibility.platform !== qualifiedHarness.real_platform) {
      errors.push("vertical_feasibility.platform must match the qualified harness real platform");
    }
    if (feasibility.representative_data !== qualifiedHarness.representative_data) {
      errors.push("vertical_feasibility.representative_data must match the qualified harness fixture profile");
    }
  }
}

function validatePrerequisite(errors, data, slices, prerequisite, sliceId) {
  if (GATE_PREREQUISITES.has(prerequisite)) {
    const status = gateStatus(data, prerequisite);
    if (!isPass(status) && !isNotApplicable(status)) {
      errors.push(`slice ${sliceId} prerequisite ${prerequisite} is not satisfied`);
    }
    return;
  }
  const dependency = slices.get(prerequisite);
  if (!dependency || normalized(dependency.status) !== "pass") {
    errors.push(`slice ${sliceId} prerequisite ${prerequisite} is not pass`);
  }
}

function transitiveSliceCommits(errors, data, slices, slice) {
  const tokens = new Set();
  const visited = new Set();
  function collect(current) {
    if (!current || visited.has(current.id)) return;
    visited.add(current.id);
    for (const token of validateCommitList(errors, current.commits, `slice ${current.id}.commits`, data)) {
      tokens.add(token);
    }
    for (const prerequisite of current.prerequisites ?? []) collect(slices.get(prerequisite));
  }
  collect(slice);
  return [...tokens].sort();
}

function validateTemporalConformanceForSlice(errors, data, slices, slice) {
  const tests = data.temporal_contract_matrix?.executable_tests ?? [];
  for (const [index, executable] of tests.entries()) {
    if (executable?.slice_id !== slice.id) continue;
    const label = `temporal_contract_matrix.executable_tests[${index}]`;
    if (executable.required === false) {
      validateException(errors, executable.exception, `${label}.exception`);
      continue;
    }
    if (!isPass(executable.status)) errors.push(`${label}.status must be PASS for G3/${slice.id}`);
    if (executable.exit_code !== 0) errors.push(`${label}.exit_code must equal 0 for G3/${slice.id}`);
    if (!isIsoInstant(executable.verified_at)) {
      errors.push(`${label}.verified_at must be an ISO-8601 instant for G3/${slice.id}`);
    }
    validateEvidenceRef(errors, executable.evidence_ref, `${label}.evidence_ref`);
    const actualCommits = validateCommitList(errors, executable.commits, `${label}.commits`, data, {
      allowMultiplePerRepository: true,
    });
    const expectedCommits = transitiveSliceCommits(errors, data, slices, slice);
    exactSet(errors, actualCommits, expectedCommits, `${label}.commits`);
  }
}

function validatePassedSlice(errors, data, slices, slice, context) {
  const label = `slice ${slice.id}`;
  if (slice.required !== true && slice.required !== false) errors.push(`${label}.required must be boolean`);
  if (normalized(slice.status) !== "pass") errors.push(`${label}.status must be pass`);
  if (!meaningful(slice.status_reason)) errors.push(`${label}.status_reason is required`);
  if (boundaryEvidenceRequired(data) && slice.boundary_evidence?.required !== true) {
    errors.push(`${label}.boundary_evidence.required must be true for the declared boundary scope`);
  }
  if (context.feasibility?.required === true && slice.vertical_evidence?.required !== true) {
    errors.push(`${label}.vertical_evidence.required must be true when G2V is required`);
  }
  for (const prerequisite of slice.prerequisites ?? []) {
    validatePrerequisite(errors, data, slices, prerequisite, slice.id);
  }
  validateEvidenceBlock(errors, slice.local_evidence, `${label}.local_evidence`);
  validateEvidenceBlock(errors, slice.boundary_evidence, `${label}.boundary_evidence`);
  validateEvidenceBlock(errors, slice.vertical_evidence, `${label}.vertical_evidence`);
  const expectedCommits = transitiveSliceCommits(errors, data, slices, slice);
  const needsVertical = slice.vertical_evidence?.required === true && context.feasibility?.required === true;
  validateFreshness(errors, slice.freshness, `${label}.freshness`, context, expectedCommits, needsVertical);
  validateTemporalConformanceForSlice(errors, data, slices, slice);
}

function validateG3(errors, data, context, sliceId) {
  if (!sliceId) {
    errors.push("schema v2 G3 requires --slice <slice-id>");
    return;
  }
  validateNoOpenBreaker(errors, data.failure_circuit_breaker, `G3/${sliceId}`);
  validateG2V(errors, data, context);
  const slice = context.slices.get(sliceId);
  if (!slice) {
    errors.push(`unknown slice: ${sliceId}`);
    return;
  }
  if (slice.required === false && isNotApplicable(slice.status)) {
    errors.push(`optional slice ${sliceId} is N/A and has no G3 implementation verdict`);
    return;
  }
  const validated = new Set();
  function validateTree(current) {
    for (const prerequisite of current.prerequisites ?? []) {
      const dependency = context.slices.get(prerequisite);
      if (!dependency || validated.has(prerequisite)) continue;
      validateTree(dependency);
      validated.add(prerequisite);
      validatePassedSlice(errors, data, context.slices, dependency, context);
    }
  }
  validateTree(slice);
  validatePassedSlice(errors, data, context.slices, slice, context);
}

function allImplementedCommitTokens(errors, data, context) {
  const tokens = new Set();
  for (const slice of context.slices.values()) {
    if (normalized(slice.status) !== "pass") continue;
    for (const token of validateCommitList(errors, slice.commits, `slice ${slice.id}.commits`, data)) {
      tokens.add(token);
    }
  }
  return [...tokens].sort();
}

function validateFinalVerdicts(errors, data, context) {
  if (!context.finalE2E) return;
  const expectedCommits = allImplementedCommitTokens(errors, data, context);
  for (const key of FINAL_E2E_KEYS) {
    const label = `final_e2e.${key}`;
    const verdict = context.finalE2E[key];
    if (!asObject(verdict)) continue;
    if (verdict.required) {
      if (!isPass(verdict.status)) errors.push(`${label}.status must be PASS`);
      if (!meaningful(verdict.reason)) errors.push(`${label}.reason is required`);
      if (!meaningful(verdict.command)) errors.push(`${label}.command is required`);
      if (!meaningful(verdict.environment)) errors.push(`${label}.environment is required`);
      if (verdict.exit_code !== 0) errors.push(`${label}.exit_code must equal 0`);
      if (!isIsoInstant(verdict.verified_at)) {
        errors.push(`${label}.verified_at must be an ISO-8601 instant`);
      }
      const commits = validateCommitList(errors, verdict.commits, `${label}.commits`, data, {
        allowMultiplePerRepository: true,
      });
      exactSet(errors, commits, expectedCommits, `${label}.commits`);
      exactSet(errors, verdict.contract_refs, context.contractTokens, `${label}.contract_refs`);
      exactSet(errors, verdict.fixture_refs, context.fixtureTokens, `${label}.fixture_refs`);
      const harness = validateHarnessBinding(errors, verdict.harness, context.harnesses, `${label}.harness`);
      if (harness) {
        validateHarnessQualified(errors, harness, `runtime_harnesses.${harness.id}`);
        if (verdict.platform !== harness.real_platform) {
          errors.push(`${label}.platform must match the qualified harness real platform`);
        }
      }
      if (verdict.production_bootstrap !== true) errors.push(`${label}.production_bootstrap must be true`);
      validateEvidenceRefs(errors, verdict.evidence_refs, `${label}.evidence_refs`, true);
    } else {
      if (!isNotApplicable(verdict.status)) errors.push(`${label}.status must be N/A`);
      validateException(errors, verdict.exception, `${label}.exception`);
    }
  }
}

function validateG4(errors, data, context) {
  validateNoOpenBreaker(errors, data.failure_circuit_breaker, "G4");
  validateG2V(errors, data, context);
  validateGatePassed(errors, data, "G4");
  for (const slice of context.slices.values()) {
    if (isNotApplicable(slice.status)) {
      if (slice.required !== false) errors.push(`required slice ${slice.id} cannot be N/A`);
      else validateException(errors, slice.exception, `slice ${slice.id}.exception`);
      continue;
    }
    validatePassedSlice(errors, data, context.slices, slice, context);
  }
  validateFinalVerdicts(errors, data, context);
}

function validateProductionData(data, { gate = "", sliceId = "" }, errors) {
  if (DEMO_GATES.has(gate)) {
    errors.push(`${gate} is only valid for delivery_profile: demo_fast`);
    return;
  }
  const context = validateV2Base(data, errors, gate);
  if (["G0", "G1", "G2"].includes(gate)) validateDesignGateChain(errors, data, gate);
  if (gate === "G2A") validateG2A(errors, data);
  if (gate === "G2V") validateG2V(errors, data, context);
  if (gate === "G3") validateG3(errors, data, context, sliceId);
  if (gate === "G4") validateG4(errors, data, context);
  if (gate === "G5") {
    validateNoOpenBreaker(errors, data.failure_circuit_breaker, "G5");
    validateG4(errors, data, context);
    validateGatePassed(errors, data, "G5");
  }
  if (gate === "G6") {
    validateNoOpenBreaker(errors, data.failure_circuit_breaker, "G6");
    validateG4(errors, data, context);
    validateGatePassed(errors, data, "G5");
    validateGatePassed(errors, data, "G6");
  }
}

export function validateFeatureData(data, { gate = "", sliceId = "" } = {}) {
  const errors = [];
  const warnings = [];
  const schemaVersion = data?.schema_version;
  if (schemaVersion === 1) {
    warnings.push(
      "LEGACY_SCHEMA_V1: historical read only; result does not prove G2V, per-slice G3, temporal contracts, harness qualification, split E2E, or the three-failure fuse",
    );
    if (DOWNSTREAM_GATES.has(gate)) {
      errors.push(`schema v1 must migrate to schema v2 before claiming ${gate}`);
    }
    return { schemaVersion, errors, warnings };
  }
  if (schemaVersion !== 2 && schemaVersion !== 3) {
    errors.push(`unsupported schema_version: ${String(schemaVersion)}`);
    return { schemaVersion, errors, warnings };
  }
  if (schemaVersion === 2) {
    validateProductionData(data, { gate, sliceId }, errors);
    return { schemaVersion, errors, warnings };
  }
  const profile = validateV3Envelope(errors, data);
  validateTermination(errors, data, gate);
  if (profile === "demo_fast") {
    if (gate.startsWith("G")) {
      errors.push(`${gate} is only valid for delivery_profile: production_hardened`);
    } else {
      validateDemoBase(errors, data, gate);
    }
  } else if (profile === "production_hardened") {
    const productionData = { ...data, schema_version: 2 };
    validateProductionData(productionData, { gate, sliceId }, errors);
    if (["G5", "G6"].includes(gate) && normalized(data.exposure) !== "public") {
      errors.push(`${gate} requires exposure: public`);
    }
  }
  return { schemaVersion, errors, warnings };
}

function collectEvidenceRefs(value, key = "", refs = new Set()) {
  if (Array.isArray(value)) {
    if (["refs", "evidence_refs", "discriminating_evidence_refs"].includes(key)) {
      for (const ref of value) if (typeof ref === "string" && EVIDENCE_REF.test(ref)) refs.add(ref);
    } else for (const entry of value) collectEvidenceRefs(entry, "", refs);
    return refs;
  }
  if (!asObject(value)) return refs;
  for (const [childKey, child] of Object.entries(value)) {
    if (childKey === "evidence_ref") {
      if (typeof child === "string" && EVIDENCE_REF.test(child)) refs.add(child);
    } else collectEvidenceRefs(child, childKey, refs);
  }
  return refs;
}

function safeDocumentPath(featureDir, relativePath, expected, errors, label) {
  if (relativePath !== expected) {
    errors.push(`${label} must equal ${expected}`);
    return null;
  }
  const root = path.resolve(featureDir);
  const resolved = path.resolve(root, relativePath);
  if (!resolved.startsWith(`${root}${path.sep}`)) {
    errors.push(`${label} escapes the feature package`);
    return null;
  }
  try {
    const source = fs.readFileSync(resolved, "utf8");
    if (source.trim().length === 0) errors.push(`${label} points to an empty document`);
    return source;
  } catch (error) {
    errors.push(`${label} cannot be read: ${error.code ?? "error"}`);
    return null;
  }
}

function validateLinkedDocuments(featureDir, data, options, errors) {
  const documents = asObject(data.documents) ?? {};
  const temporalSource = safeDocumentPath(
    featureDir,
    documents.temporal_contract,
    "04A-temporal-contract-matrix.md",
    errors,
    "documents.temporal_contract",
  );
  const reportSource = safeDocumentPath(
    featureDir,
    documents.verification,
    "08-verification-report.md",
    errors,
    "documents.verification",
  );
  if (temporalSource && ["G2", "G2A", "G2V", "G3", "G4", "G5", "G6"].includes(options.gate)) {
    const matrix = data.temporal_contract_matrix ?? {};
    const ids = [
      ...(matrix.scenarios ?? []).map((scenario) => scenario.id),
      ...(matrix.invariants ?? []).flatMap((invariant) => [
        invariant.id,
        ...(invariant.executable_tests ?? []),
      ]),
    ].filter(meaningful);
    for (const id of ids) {
      if (!temporalSource.includes(id)) {
        errors.push(`temporal contract document does not contain structured id: ${id}`);
      }
    }
  }
  if (reportSource) {
    for (const ref of collectEvidenceRefs(data)) {
      const id = EVIDENCE_REF.exec(ref)?.[1];
      if (!id) continue;
      const marker = `<!-- evidence: ${id} -->`;
      const occurrences = reportSource.split(marker).length - 1;
      if (occurrences !== 1) {
        errors.push(`${ref} must resolve to exactly one '${marker}' marker`);
      }
    }
  }
}

function validateDemoLinkedDocuments(featureDir, data, errors) {
  const documents = asObject(data.documents) ?? {};
  safeDocumentPath(
    featureDir,
    documents.brief,
    "00-feature-brief.md",
    errors,
    "documents.brief",
  );
  safeDocumentPath(
    featureDir,
    documents.delivery_log,
    "01-delivery-log.md",
    errors,
    "documents.delivery_log",
  );
  safeDocumentPath(
    featureDir,
    documents.verification,
    "02-verification.md",
    errors,
    "documents.verification",
  );
}

export function loadAndValidateFeaturePackage(featureDir, options = {}) {
  const featurePath = path.join(featureDir, "feature.yaml");
  let source;
  try {
    source = fs.readFileSync(featurePath, "utf8");
  } catch (error) {
    return {
      schemaVersion: null,
      errors: [`cannot read ${featurePath}: ${error.code ?? "error"}`],
      warnings: [],
    };
  }
  const document = YAML.parseDocument(source, { uniqueKeys: true });
  if (document.errors.length > 0) {
    return {
      schemaVersion: null,
      errors: document.errors.map((error) => `invalid feature.yaml: ${error.message}`),
      warnings: [],
    };
  }
  const data = document.toJS();
  const result = validateFeatureData(data, options);
  if (result.schemaVersion === 2 || deliveryProfile(data) === "production_hardened") {
    validateLinkedDocuments(featureDir, data, options, result.errors);
  } else if (result.schemaVersion === 3 && deliveryProfile(data) === "demo_fast") {
    validateDemoLinkedDocuments(featureDir, data, result.errors);
  }
  return result;
}

export function claimedGateChecks(data) {
  if (data?.schema_version === 3 && deliveryProfile(data) === "demo_fast") {
    const claims = [];
    if (isPass(data.product_ux?.status)) claims.push({ gate: "D0" });
    if (isPass(data.verification?.status)) claims.push({ gate: "D4" });
    if (normalized(data.exposure) === "public" && isPass(data.public_readiness?.status)) {
      claims.push({ gate: "DP" });
    }
    return claims;
  }
  const claims = [];
  for (const gate of ["G0", "G1", "G2"]) {
    if (isPass(gateStatus(data, gate))) claims.push({ gate });
  }
  for (const gate of ["G2A", "G2V"]) {
    if (isPass(gateStatus(data, gate)) || isNotApplicable(gateStatus(data, gate))) claims.push({ gate });
  }
  for (const slice of data.slices ?? []) {
    if (normalized(slice.status) === "pass") claims.push({ gate: "G3", sliceId: slice.id });
  }
  for (const gate of ["G4", "G5", "G6"]) {
    if (isPass(gateStatus(data, gate))) claims.push({ gate });
  }
  return claims;
}

export function validateClaimedFeaturePackage(featureDir) {
  const base = loadAndValidateFeaturePackage(featureDir);
  if (base.errors.length > 0 || ![2, 3].includes(base.schemaVersion)) return base;
  const featurePath = path.join(featureDir, "feature.yaml");
  const document = YAML.parseDocument(fs.readFileSync(featurePath, "utf8"), { uniqueKeys: true });
  const data = document.toJS();
  const claims = claimedGateChecks(data);
  const errors = [...base.errors];
  const warnings = [...base.warnings];
  for (const claim of claims) {
    const result = loadAndValidateFeaturePackage(featureDir, claim);
    const label = claim.sliceId ? `${claim.gate}/${claim.sliceId}` : claim.gate;
    errors.push(...result.errors.map((error) => `${label}: ${error}`));
    warnings.push(...result.warnings);
  }
  return {
    schemaVersion: base.schemaVersion,
    errors: [...new Set(errors)],
    warnings: [...new Set(warnings)],
  };
}

export function validateFailureLedgerEvolution(previousData, currentData) {
  const errors = [];
  const previousProduction =
    previousData?.schema_version === 2 ||
    (previousData?.schema_version === 3 && deliveryProfile(previousData) === "production_hardened");
  const currentProduction =
    currentData?.schema_version === 2 ||
    (currentData?.schema_version === 3 && deliveryProfile(currentData) === "production_hardened");
  if (!previousProduction) return errors;
  if (!currentProduction) {
    errors.push("production_hardened Feature Package cannot be downgraded or bypass its failure ledger");
    return errors;
  }
  const previousIncidents = new Map(
    (previousData.failure_circuit_breaker?.incidents ?? []).map((incident) => [incident.id, incident]),
  );
  const currentIncidents = new Map(
    (currentData.failure_circuit_breaker?.incidents ?? []).map((incident) => [incident.id, incident]),
  );
  const identityFields = [
    "id",
    "slice_id",
    "gate_id",
    "evidence_id",
    "failure_class",
    "failure_code",
    "checkpoint",
    "fingerprint",
  ];
  for (const [id, previous] of previousIncidents) {
    const current = currentIncidents.get(id);
    if (!current) {
      errors.push(`failure ledger incident was removed: ${id}`);
      continue;
    }
    for (const field of identityFields) {
      if (current[field] !== previous[field]) {
        errors.push(`failure ledger incident ${id}.${field} is immutable`);
      }
    }
    const previousAttempts = previous.attempts ?? [];
    const currentAttempts = current.attempts ?? [];
    if (currentAttempts.length < previousAttempts.length) {
      errors.push(`failure ledger incident ${id}.attempts cannot shrink`);
    }
    for (const [index, attempt] of previousAttempts.entries()) {
      if (JSON.stringify(currentAttempts[index]) !== JSON.stringify(attempt)) {
        errors.push(`failure ledger incident ${id}.attempts[${index}] is immutable`);
      }
    }
    const previousCycles = previous.rca_cycles ?? [];
    const currentCycles = current.rca_cycles ?? [];
    if (currentCycles.length < previousCycles.length) {
      errors.push(`failure ledger incident ${id}.rca_cycles cannot shrink`);
    }
    for (const [index, cycle] of previousCycles.entries()) {
      const next = currentCycles[index];
      if (!next || next.id !== cycle.id) {
        errors.push(`failure ledger incident ${id}.rca_cycles[${index}] is immutable`);
        continue;
      }
      for (const field of ["audit", "authorization"]) {
        if (JSON.stringify(next[field]) !== JSON.stringify(cycle[field])) {
          errors.push(`failure ledger incident ${id}.rca_cycles[${index}].${field} is immutable`);
        }
      }
      if (cycle.attempt != null && JSON.stringify(next.attempt) !== JSON.stringify(cycle.attempt)) {
        errors.push(`failure ledger incident ${id}.rca_cycles[${index}].attempt is immutable once recorded`);
      }
    }
  }
  return errors;
}

export function validateFeaturePackageEvolution(previousData, currentData) {
  if (previousData == null) {
    if (currentData?.schema_version !== 3) return ["new Feature Package must use schema_version: 3"];
    if (!DELIVERY_PROFILES.has(deliveryProfile(currentData))) {
      return ["new Feature Package must declare delivery_profile"];
    }
    if (!EXPOSURES.has(normalized(currentData.exposure))) {
      return ["new Feature Package must declare exposure: local or public"];
    }
    return [];
  }
  if (previousData?.schema_version === 1 && currentData?.schema_version === 1) {
    return isDeepStrictEqual(previousData, currentData)
      ? []
      : ["legacy schema v1 feature.yaml is historical-only; migrate to schema v2 before changing claims"];
  }
  if (previousData?.schema_version === 2 && currentData?.schema_version !== 2) {
    return ["historical schema v2 package keeps its production_hardened semantics and cannot change schema"];
  }
  if (previousData?.schema_version === 3) {
    if (currentData?.schema_version !== 3) return ["schema v3 Feature Package cannot be downgraded"];
    if (deliveryProfile(previousData) !== deliveryProfile(currentData)) {
      return ["delivery_profile is immutable; create an explicit production_hardened package when upgrading"];
    }
    if (normalized(previousData.exposure) === "public" && normalized(currentData.exposure) === "local") {
      return ["exposure cannot be downgraded from public to local to bypass public readiness"];
    }
    if (normalized(previousData.feature?.status) === "terminated" && previousData.termination?.permanent === true) {
      if (normalized(currentData.feature?.status) !== "terminated" ||
          !isDeepStrictEqual(previousData.termination, currentData.termination)) {
        return ["permanent termination decision cannot be removed or reopened"];
      }
    }
  }
  return validateFailureLedgerEvolution(previousData, currentData);
}

function parseArgs(argv) {
  let gate = "";
  let sliceId = "";
  let auditClaims = false;
  let featureDir = "";
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--gate") {
      gate = argv[index + 1] ?? "";
      index += 1;
    } else if (arg === "--slice") {
      sliceId = argv[index + 1] ?? "";
      index += 1;
    } else if (arg === "--audit-claims") {
      auditClaims = true;
    } else if (arg.startsWith("-")) throw new Error(`unknown option: ${arg}`);
    else if (!featureDir) featureDir = arg;
    else throw new Error("only one FEATURE_DIR may be specified");
  }
  if (!featureDir) throw new Error("FEATURE_DIR is required");
  if (auditClaims && (gate || sliceId)) {
    throw new Error("--audit-claims cannot be combined with --gate or --slice");
  }
  return { featureDir, gate, sliceId, auditClaims };
}

function main() {
  let options;
  try {
    options = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    process.exitCode = 2;
    return;
  }
  const result = options.auditClaims
    ? validateClaimedFeaturePackage(options.featureDir)
    : loadAndValidateFeaturePackage(options.featureDir, options);
  for (const warning of result.warnings) console.warn(`WARNING: ${warning}`);
  if (result.errors.length > 0) {
    for (const error of result.errors) console.error(`ERROR: ${error}`);
    process.exitCode = 1;
    return;
  }
  console.log(`PASS: feature.yaml schema v${result.schemaVersion} semantics are valid.`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main();
