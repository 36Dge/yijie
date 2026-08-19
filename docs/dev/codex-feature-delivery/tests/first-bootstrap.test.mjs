import assert from "node:assert/strict";
import { chmodSync, existsSync, mkdirSync, mkdtempSync, readFileSync, realpathSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import test from "node:test";
import YAML from "yaml";
import { canonicalGitPath, decodeGitUtf8 } from "../scripts/verify-first-bootstrap.mjs";

const distributionRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const initProject = join(distributionRoot, "scripts/init-project.mjs");
const verifier = join(distributionRoot, "scripts/verify-first-bootstrap.mjs");

function run(command, args, options = {}) {
  return spawnSync(command, args, { encoding: "utf8", ...options, env: { ...process.env, ...options.env } });
}

function git(root, ...args) {
  const result = run("git", ["-C", root, ...args]);
  assert.equal(result.status, 0, `git ${args.join(" ")} failed:\n${result.stdout}\n${result.stderr}`);
  return result.stdout.trim();
}

function commitAll(root, message) {
  git(root, "add", "-A");
  git(root, "commit", "-qm", message);
  return git(root, "rev-parse", "HEAD");
}

function bootstrapArgs(state, overrides = {}) {
  const now = Date.now();
  return [
    verifier,
    "--repo-root", state.root,
    "--repository", overrides.repository ?? `acme/${state.repositoryId}`,
    "--repo-id", overrides.repoId ?? state.repositoryId,
    "--target-branch", overrides.targetBranch ?? "main",
    "--base", overrides.base ?? state.base,
    "--head", overrides.head ?? state.head,
    "--authorization-id", overrides.authorizationId ?? "BOOTSTRAP-2026-001",
    "--approval-reference", overrides.approvalReference ?? "change-ticket:example-001",
    "--created-at", overrides.createdAt ?? new Date(now - 60_000).toISOString(),
    "--expires-at", overrides.expiresAt ?? new Date(now + 60 * 60_000).toISOString(),
    ...(overrides.digest ? ["--bootstrap-digest", overrides.digest] : []),
    "--json",
  ];
}

function invoke(state, overrides = {}) {
  const result = run(process.execPath, bootstrapArgs(state, overrides));
  let report;
  try { report = JSON.parse(result.stdout); } catch { report = { stdout: result.stdout, stderr: result.stderr }; }
  return { ...result, report };
}

function createCandidate(t, repositoryId = "bootstrap-app") {
  const root = realpathSync(mkdtempSync(join(tmpdir(), "cfd-first-bootstrap-")));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  git(root, "init", "-q", "-b", "main");
  git(root, "config", "user.name", "Example Owner");
  git(root, "config", "user.email", "owner@example.invalid");
  git(root, "remote", "add", "origin", `https://github.com/acme/${repositoryId}.git`);
  writeFileSync(join(root, "README.md"), "# Bootstrap application\n");
  const base = commitAll(root, "initial base");
  git(root, "update-ref", "refs/remotes/origin/main", base);

  const initialized = run(process.execPath, [
    initProject,
    "--project-root", root,
    "--project-id", "example-suite",
    "--project-name", "Example Suite",
    "--repository-id", repositoryId,
    "--actor-id", "36Dge",
    "--framework-root", "platform/cfd/runtime",
    "--feature-root", "delivery/features",
    "--primary-branch", "main",
    "--ci", "github",
  ]);
  assert.equal(initialized.status, 0, `${initialized.stdout}\n${initialized.stderr}`);

  mkdirSync(join(root, ".codex/prompts"), { recursive: true });
  mkdirSync(join(root, ".codex/tasks"), { recursive: true });
  writeFileSync(join(root, "AGENTS.md"), `# Agent rules

## Feature Delivery v2

New work uses schema_version: 2, all required G2C instances, and feature-delivery/trusted-coverage-status.
`);
  writeFileSync(join(root, ".codex/config.toml"), `read_before_work = ["platform/cfd/runtime/README.md", "platform/cfd/runtime/HANDBOOK.md"]\n`);
  writeFileSync(join(root, ".codex/prompts/dev.md"), "Follow Feature Delivery v2 before implementation.\n");
  writeFileSync(join(root, ".codex/tasks/implement.md"), "Require schema_version: 2, G2C, and feature-delivery/trusted-coverage-status.\n");
  writeFileSync(join(root, ".github/pull_request_template.md"), `${readFileSync(join(root, ".github/pull_request_template.md"), "utf8")}\n## Project-specific review\n\n- [ ] Project contract checked.\n`);
  const head = commitAll(root, "install feature delivery v2");
  return { root, repositoryId, base, head, frameworkRoot: "platform/cfd/runtime" };
}

test("first-bootstrap emits a repository/base/head-bound digest and accepts only the exact external pin", (t) => {
  const state = createCandidate(t);
  const diagnostic = invoke(state);
  assert.equal(diagnostic.status, 1, `${diagnostic.stderr}\n${JSON.stringify(diagnostic.report)}`);
  assert.equal(diagnostic.report.verdict, "BOOTSTRAP_DIGEST_REQUIRED");
  assert.match(diagnostic.report.expected_bootstrap_digest, /^sha256:[0-9a-f]{64}$/);
  assert.equal(diagnostic.report.repository, "acme/bootstrap-app");
  assert.equal(diagnostic.report.base_sha, state.base);
  assert.equal(diagnostic.report.head_sha, state.head);
  assert.ok(diagnostic.report.changed_file_count > 20);

  const accepted = invoke(state, {
    createdAt: diagnostic.report.authorization.created_at,
    expiresAt: diagnostic.report.authorization.expires_at,
    digest: diagnostic.report.expected_bootstrap_digest,
  });
  assert.equal(accepted.status, 0, accepted.stderr);
  assert.equal(accepted.report.valid, true);
  assert.equal(accepted.report.verdict, "BOOTSTRAP_DIGEST_APPLIED");

  const wrongPin = invoke(state, {
    createdAt: diagnostic.report.authorization.created_at,
    expiresAt: diagnostic.report.authorization.expires_at,
    digest: "sha256:0000000000000000000000000000000000000000000000000000000000000000",
  });
  assert.equal(wrongPin.status, 1);
  assert.equal(wrongPin.report.verdict, "BOOTSTRAP_DIGEST_REQUIRED");

  const otherRepository = invoke(state, { repository: "acme/another-app", digest: diagnostic.report.expected_bootstrap_digest });
  assert.equal(otherRepository.status, 2);
  assert.match(otherRepository.report.errors.join(" "), /origin=.*--repository/i);
});

test("path, mode, content, head, tree, authorization, and time changes cannot reuse a digest", (t) => {
  const state = createCandidate(t);
  const original = invoke(state).report.expected_bootstrap_digest;
  writeFileSync(join(state.root, "README.md"), "# Changed after authorization\n");
  const contentHead = commitAll(state.root, "change content");
  const content = invoke(state, { head: contentHead });
  assert.equal(content.status, 1, `${content.stderr}\n${JSON.stringify(content.report)}`);
  assert.notEqual(content.report.expected_bootstrap_digest, original);

  chmodSync(join(state.root, "README.md"), 0o755);
  const modeHead = commitAll(state.root, "change mode");
  const mode = invoke(state, { head: modeHead });
  assert.equal(mode.status, 1);
  assert.notEqual(mode.report.expected_bootstrap_digest, content.report.expected_bootstrap_digest);

  const changedAuthorization = invoke(state, { authorizationId: "BOOTSTRAP-2026-002", head: modeHead });
  assert.notEqual(changedAuthorization.report.expected_bootstrap_digest, mode.report.expected_bootstrap_digest);
  const expired = invoke(state, {
    head: modeHead,
    createdAt: new Date(Date.now() - 26 * 60 * 60_000).toISOString(),
    expiresAt: new Date(Date.now() - 25 * 60 * 60_000).toISOString(),
  });
  assert.equal(expired.status, 2);
  assert.equal(expired.report.verdict, "AUTHORIZATION_EXPIRED");
});

test("candidate scripts are never executed and runtime/workflow drift is rejected", (t) => {
  const state = createCandidate(t);
  const marker = join(state.root, "candidate-script-executed");
  const candidateVerifier = join(state.root, state.frameworkRoot, "scripts/verify-first-bootstrap.mjs");
  writeFileSync(candidateVerifier, `import { writeFileSync } from "node:fs"; writeFileSync(${JSON.stringify(marker)}, "unsafe");\n`);
  writeFileSync(join(state.root, ".github/workflows/feature-delivery-coverage.yml"), "on: pull_request\njobs: {unsafe: {runs-on: ubuntu-latest, steps: [{run: node candidate.js}]}}\n");
  const maliciousHead = commitAll(state.root, "malicious candidate runtime");
  const result = invoke(state, { head: maliciousHead });
  assert.equal(result.status, 2);
  assert.match(result.report.errors.join(" "), /workflow|runtime|manifest/i);
  assert.equal(existsSync(marker), false, "candidate script must remain unexecuted");
});

test("an older distribution is reported as stale instead of producing an authorization digest", (t) => {
  const state = createCandidate(t);
  const manifestPath = join(state.root, state.frameworkRoot, "RELEASE-MANIFEST.json");
  const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
  manifest.distribution.version = "2.0.0";
  manifest.distribution_digest = "sha256:62cd19a9a61ac3ab81fd90dbeb5ef060f2f8c80c5ce985e5cf1c17c3cf9a323b";
  writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
  const head = commitAll(state.root, "install stale runtime");
  const result = invoke(state, { head });
  assert.equal(result.status, 2);
  assert.equal(result.report.verdict, "STALE_DISTRIBUTION");
  assert.match(result.report.errors.join(" "), /2\.0\.0.*2\.0\.1/);
});

test("non-empty trust, embedded exemption, symlink, and gitlink are fail-closed", async (t) => {
  await t.test("non-empty trust", (t) => {
    const state = createCandidate(t);
    const trustPath = join(state.root, ".feature-delivery/approval-trust.yaml");
    const trust = YAML.parse(readFileSync(trustPath, "utf8"));
    trust.keys.push({ id: "forged" });
    writeFileSync(trustPath, YAML.stringify(trust));
    const head = commitAll(state.root, "forge trust");
    const result = invoke(state, { head });
    assert.equal(result.status, 2);
    assert.match(result.report.errors.join(" "), /approval trust|keys/i);
  });

  await t.test("embedded exemption", (t) => {
    const state = createCandidate(t);
    const policyPath = join(state.root, ".feature-delivery/change-coverage-policy.yaml");
    const policy = YAML.parse(readFileSync(policyPath, "utf8"));
    policy.exemptions.push({ id: "forged" });
    writeFileSync(policyPath, YAML.stringify(policy));
    const head = commitAll(state.root, "embed exemption");
    const result = invoke(state, { head });
    assert.equal(result.status, 2);
    assert.match(result.report.errors.join(" "), /coverage policy|exemptions/i);
  });

  await t.test("symlink", (t) => {
    const state = createCandidate(t);
    symlinkSync("README.md", join(state.root, "unsafe-link"));
    const head = commitAll(state.root, "add symlink");
    const result = invoke(state, { head });
    assert.equal(result.status, 2);
    assert.match(result.report.errors.join(" "), /symlink|mode=120000/i);
  });

  await t.test("gitlink", (t) => {
    const state = createCandidate(t);
    git(state.root, "update-index", "--add", "--cacheinfo", `160000,${state.base},unsafe-submodule`);
    git(state.root, "commit", "-qm", "add gitlink");
    const head = git(state.root, "rev-parse", "HEAD");
    const result = invoke(state, { head });
    assert.equal(result.status, 2);
    assert.match(result.report.errors.join(" "), /submodule|mode=160000/i);
  });
});

test("base with any v2 project config cannot use first-bootstrap", (t) => {
  const state = createCandidate(t);
  git(state.root, "update-ref", "refs/remotes/origin/main", state.head);
  writeFileSync(join(state.root, "after-bootstrap.txt"), "normal change\n");
  const nextHead = commitAll(state.root, "normal change");
  const result = invoke({ ...state, base: state.head, head: nextHead });
  assert.equal(result.status, 2);
  assert.equal(result.report.verdict, "BASE_ALREADY_INITIALIZED");
});

test("authorization validity is bounded to at most 24 hours", (t) => {
  const state = createCandidate(t);
  const now = Date.now();
  const result = invoke(state, {
    createdAt: new Date(now - 60_000).toISOString(),
    expiresAt: new Date(now + 24 * 60 * 60_000).toISOString(),
  });
  assert.equal(result.status, 2);
  assert.match(result.report.errors.join(" "), /24 小时/);
});

test("Git path decoder and canonicalizer reject byte and normalization aliases", () => {
  assert.throws(() => decodeGitUtf8(Buffer.from([0xff])), /非法 UTF-8/);
  for (const path of ["foo\\bar", "foo//bar", "foo/../bar", "foo/.git/config", "e\u0301.txt", "./foo"]) {
    assert.throws(() => canonicalGitPath(path), /路径|segment|NFC/);
  }
  assert.equal(canonicalGitPath("é.txt"), "é.txt");
});
