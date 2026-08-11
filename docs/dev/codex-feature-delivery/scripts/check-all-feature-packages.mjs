#!/usr/bin/env node

import { existsSync, lstatSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import process from "node:process";
import YAML from "yaml";
import { validateApprovalTrustRoot } from "./approval-attestation.mjs";
import { loadLegacyPins } from "./legacy-v1.mjs";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const frameworkDir = resolve(scriptDir, "..");
const evaluator = resolve(scriptDir, "evaluate-feature-package.mjs");
const featureRoot = resolve(process.argv[2] ?? resolve(frameworkDir, "../../features"));
const allowlistPath = resolve(frameworkDir, "legacy-v1-allowlist.txt");
const trustRootPath = resolve(frameworkDir, "approval-trust.yaml");

if (!existsSync(featureRoot) || !statSync(featureRoot).isDirectory()) {
  process.stderr.write(`ERROR: Feature root 不存在：${featureRoot}\n`);
  process.exit(2);
}

let legacyPins;
try {
  legacyPins = loadLegacyPins(allowlistPath);
} catch (error) {
  process.stderr.write(`ERROR: ${error.message}\n`);
  process.exit(2);
}
const errors = [];
let v2Count = 0;
let legacyCount = 0;
const featureIds = new Map();

try {
  const trustMetadata = lstatSync(trustRootPath);
  if (!trustMetadata.isFile() || trustMetadata.isSymbolicLink() || trustMetadata.nlink !== 1) throw new Error("approval-trust.yaml 必须是非 symlink/hardlink 的普通文件");
  const trustDocument = YAML.parseDocument(readFileSync(trustRootPath, "utf8"), { uniqueKeys: true, prettyErrors: true });
  if (trustDocument.errors.length > 0) throw new Error(trustDocument.errors.map((item) => item.message).join("; "));
  const trustErrors = validateApprovalTrustRoot(trustDocument.toJS());
  if (trustErrors.length > 0) throw new Error(trustErrors.join("; "));
} catch (error) {
  errors.push(`approval trust root 无效：${error.message}`);
}

for (const name of readdirSync(featureRoot).sort()) {
  const packageDir = resolve(featureRoot, name);
  if (!statSync(packageDir).isDirectory() || !existsSync(resolve(packageDir, "feature.yaml"))) continue;
  const evaluation = spawnSync(process.execPath, [evaluator, "--allow-legacy", "--json", packageDir], { encoding: "utf8" });
  let report;
  try {
    report = JSON.parse(evaluation.stdout);
  } catch {
    errors.push(`${name}: evaluator 未返回 JSON：${evaluation.stderr || evaluation.stdout}`);
    continue;
  }
  if (report.legacy) {
    legacyCount += 1;
    const expected = legacyPins.get(name) ?? null;
    const exactRecognition = evaluation.status !== 0
      && report.valid === false
      && report.recognized === true
      && report.verdict === "LEGACY_RECOGNIZED"
      && report.package_basename === name
      && report.expected_tree_digest === expected
      && report.tree_digest === expected;
    if (!exactRecognition) errors.push(`${name}: legacy v1 未通过 basename + normalized tree digest 精确识别：${report.errors?.join("; ") || report.verdict || "rejected"}`);
    continue;
  }
  v2Count += 1;
  const featureId = report.feature?.id;
  if (featureId) {
    const previous = featureIds.get(featureId);
    if (previous) errors.push(`重复 feature.id=${featureId}：${previous} 与 ${name}`);
    else featureIds.set(featureId, name);
  }
  if (evaluation.status !== 0 || !report.valid) errors.push(`${name}: ${report.errors?.join("; ") || "v2 校验失败"}`);
}

for (const legacyName of legacyPins.keys()) {
  if (!existsSync(resolve(featureRoot, legacyName, "feature.yaml"))) errors.push(`legacy allowlist 指向不存在的包：${legacyName}`);
}

if (errors.length > 0) {
  for (const error of errors) process.stderr.write(`ERROR: ${error}\n`);
  process.exit(1);
}
process.stdout.write(`Feature Packages valid: v2=${v2Count}, legacy_recognized=${legacyCount} (legacy is not Gate PASS)\n`);
