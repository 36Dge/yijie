#!/usr/bin/env node

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import YAML from "yaml";

import {
  claimedGateChecks,
  validateClaimedFeaturePackage,
  validateFeaturePackageEvolution,
} from "./validate-feature-package.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const repositoryRoot = path.resolve(scriptDir, "../../../..");

function parseArgs(argv) {
  let baseRef = "";
  let featureRoot = path.join(repositoryRoot, "docs/features");
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--") {
      continue;
    } else if (argument === "--base-ref") {
      baseRef = argv[index + 1] ?? "";
      index += 1;
      if (!baseRef) throw new Error("--base-ref requires a Git commit or ref");
    } else if (argument.startsWith("-")) {
      throw new Error(`unknown option: ${argument}`);
    } else if (featureRoot !== path.join(repositoryRoot, "docs/features")) {
      throw new Error("only one FEATURE_ROOT may be specified");
    } else {
      featureRoot = path.resolve(argument);
    }
  }
  return { baseRef, featureRoot };
}

function parseFeatureYaml(source, label) {
  const document = YAML.parseDocument(source, { uniqueKeys: true });
  if (document.errors.length > 0) {
    throw new Error(`${label}: ${document.errors.map((error) => error.message).join("; ")}`);
  }
  return document.toJS();
}

function readAtBase(baseRef, relativePath) {
  const listed = execFileSync("git", ["ls-tree", "--name-only", baseRef, "--", relativePath], {
    cwd: repositoryRoot,
    encoding: "utf8",
  }).trim();
  if (!listed) return null;
  return execFileSync("git", ["show", `${baseRef}:${relativePath}`], {
    cwd: repositoryRoot,
    encoding: "utf8",
  });
}

function listFeaturePackagesAtBase(baseRef) {
  const output = execFileSync(
    "git",
    ["ls-tree", "-r", "--name-only", baseRef, "--", "docs/features"],
    { cwd: repositoryRoot, encoding: "utf8" },
  );
  return new Set(
    output
      .split("\n")
      .filter((entry) => /^docs\/features\/FEAT-[^/]+\/feature\.yaml$/.test(entry)),
  );
}

function runAuthoritativePackageChecks(featureDir, data) {
  const checker = path.join(scriptDir, "check-feature-package.sh");
  const checks = [{ label: "package structure", args: [] }, ...claimedGateChecks(data).map((claim) => ({
    label: claim.sliceId ? `${claim.gate}/${claim.sliceId}` : claim.gate,
    args: claim.sliceId
      ? ["--gate", claim.gate, "--slice", claim.sliceId]
      : ["--gate", claim.gate],
  }))];
  const errors = [];
  for (const check of checks) {
    try {
      execFileSync(checker, [...check.args, featureDir], {
        cwd: repositoryRoot,
        stdio: "ignore",
      });
    } catch {
      errors.push(`authoritative shell check failed for ${check.label}`);
    }
  }
  return errors;
}

export function auditFeaturePackages({ baseRef = "", featureRoot }) {
  const errors = [];
  const warnings = [];
  let baseFeaturePaths = new Set();
  if (baseRef) {
    try {
      execFileSync("git", ["cat-file", "-e", `${baseRef}^{commit}`], {
        cwd: repositoryRoot,
        stdio: "ignore",
      });
      baseFeaturePaths = listFeaturePackagesAtBase(baseRef);
    } catch (error) {
      return {
        errors: [`cannot resolve CI base ref: ${error.message}`],
        warnings,
        packageCount: 0,
      };
    }
  }
  const entries = fs
    .readdirSync(featureRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && entry.name.startsWith("FEAT-"))
    .sort((left, right) => left.name.localeCompare(right.name));

  for (const entry of entries) {
    const featureDir = path.join(featureRoot, entry.name);
    const featurePath = path.join(featureDir, "feature.yaml");
    const result = validateClaimedFeaturePackage(featureDir);
    errors.push(...result.errors.map((error) => `${entry.name}: ${error}`));
    warnings.push(...result.warnings.map((warning) => `${entry.name}: ${warning}`));

    let current;
    if (fs.existsSync(featurePath)) {
      try {
        current = parseFeatureYaml(fs.readFileSync(featurePath, "utf8"), `${entry.name} current`);
        if ([2, 3].includes(current?.schema_version)) {
          errors.push(
            ...runAuthoritativePackageChecks(featureDir, current).map(
              (error) => `${entry.name}: ${error}`,
            ),
          );
        }
      } catch (error) {
        errors.push(`${entry.name}: ${error.message}`);
      }
    }

    if (!baseRef || !fs.existsSync(featurePath)) continue;
    try {
      const relativePath = path.relative(repositoryRoot, featurePath);
      if (relativePath.startsWith("..") || path.isAbsolute(relativePath)) {
        errors.push(`${entry.name}: feature package is outside the repository`);
        continue;
      }
      const previousSource = readAtBase(baseRef, relativePath);
      if (previousSource === null) {
        errors.push(
          ...validateFeaturePackageEvolution(null, current).map(
            (error) => `${entry.name}: ${error}`,
          ),
        );
        continue;
      }
      baseFeaturePaths.delete(relativePath);
      const previous = parseFeatureYaml(previousSource, `${entry.name} at base ref`);
      errors.push(
        ...validateFeaturePackageEvolution(previous, current).map(
          (error) => `${entry.name}: ${error}`,
        ),
      );
    } catch (error) {
      errors.push(`${entry.name}: cannot audit base ref: ${error.message}`);
    }
  }

  for (const removedPath of baseFeaturePaths) {
    try {
      const previous = parseFeatureYaml(
        execFileSync("git", ["show", `${baseRef}:${removedPath}`], {
          cwd: repositoryRoot,
          encoding: "utf8",
        }),
        `${removedPath} at base ref`,
      );
      if ([2, 3].includes(previous?.schema_version)) {
        errors.push(`schema v${previous.schema_version} Feature Package was removed or renamed: ${removedPath}`);
      }
    } catch (error) {
      errors.push(`${removedPath}: cannot audit removed package: ${error.message}`);
    }
  }

  return { errors: [...new Set(errors)], warnings: [...new Set(warnings)], packageCount: entries.length };
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
  const result = auditFeaturePackages(options);
  for (const warning of result.warnings) console.warn(`WARNING: ${warning}`);
  if (result.errors.length > 0) {
    for (const error of result.errors) console.error(`ERROR: ${error}`);
    process.exitCode = 1;
    return;
  }
  console.log(`PASS: audited ${result.packageCount} committed Feature Package claim(s).`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) main();
