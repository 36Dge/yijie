import assert from "node:assert/strict";
import { cpSync, mkdirSync, mkdtempSync, readFileSync, realpathSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import test from "node:test";
import YAML from "yaml";

const frameworkDir = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = resolve(frameworkDir, "../../..");
const newFeature = resolve(frameworkDir, "scripts/new-feature.sh");

function run(command, args) {
  return spawnSync(command, args, { encoding: "utf8", env: process.env });
}

function report(result) {
  try {
    return JSON.parse(result.stdout);
  } catch (error) {
    assert.fail(`evaluator did not return JSON (${error.message})\nstdout:\n${result.stdout}\nstderr:\n${result.stderr}`);
  }
}

function copiedEvaluator(t, mutatePolicy) {
  const outer = mkdtempSync(join(tmpdir(), "cfd-gate-policy-schema-"));
  t.after(() => rmSync(outer, { recursive: true, force: true }));
  const copiedRepository = join(outer, "yijie");
  const copiedFramework = join(copiedRepository, "docs/dev/codex-feature-delivery");
  mkdirSync(dirname(copiedFramework), { recursive: true });
  cpSync(frameworkDir, copiedFramework, { recursive: true });
  symlinkSync(join(repositoryRoot, "node_modules"), join(copiedRepository, "node_modules"), "dir");

  const policyPath = join(copiedFramework, "gate-policy.yaml");
  const policy = YAML.parse(readFileSync(policyPath, "utf8"), { uniqueKeys: true });
  mutatePolicy(policy);
  writeFileSync(policyPath, YAML.stringify(policy, { lineWidth: 0 }));
  return realpathSync(join(copiedFramework, "scripts/evaluate-feature-package.mjs"));
}

test("evaluator fails closed when human_actor_required is missing or misspelled", (t) => {
  const packageRoot = mkdtempSync(join(tmpdir(), "cfd-gate-policy-package-"));
  t.after(() => rmSync(packageRoot, { recursive: true, force: true }));
  const generated = run(newFeature, [
    "FEAT-POLICY-SCHEMA",
    "gate-policy-schema",
    "--profile",
    "lite",
    "--target",
    "local_engineering",
    "--title",
    "Gate policy schema regression",
    "--owner",
    "Test Owner",
    "--repository-id",
    "primary",
    "--output-root",
    packageRoot,
  ]);
  assert.equal(generated.status, 0, `${generated.stdout}\n${generated.stderr}`);
  const packageDir = join(packageRoot, "FEAT-POLICY-SCHEMA-gate-policy-schema");

  const missing = copiedEvaluator(t, (policy) => {
    delete policy.gates.G0.human_actor_required;
  });
  const missingResult = run(process.execPath, [missing, "--json", packageDir]);
  assert.notEqual(missingResult.status, 0, `${missingResult.stdout}\n${missingResult.stderr}`);
  assert.match(report(missingResult).errors.join("\n"), /G0\.human_actor_required.*缺少必填字段/);

  const misspelled = copiedEvaluator(t, (policy) => {
    policy.gates.G0.human_actor_require = policy.gates.G0.human_actor_required;
    delete policy.gates.G0.human_actor_required;
  });
  const misspelledResult = run(process.execPath, [misspelled, "--json", packageDir]);
  assert.notEqual(misspelledResult.status, 0, `${misspelledResult.stdout}\n${misspelledResult.stderr}`);
  assert.match(report(misspelledResult).errors.join("\n"), /G0\.human_actor_require.*不允许的字段/);
});
