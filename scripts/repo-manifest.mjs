import { readFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import YAML from "yaml";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const manifestPath = path.join(root, "repos.yaml");

export async function loadManifest() {
  const manifest = YAML.parse(await readFile(manifestPath, "utf8"));
  const defaultBranch = manifest?.defaults?.branch;

  if (manifest?.version !== 1 || !Array.isArray(manifest?.repos) || !defaultBranch) {
    throw new Error("repos.yaml must define version 1, defaults.branch, and repos");
  }

  const names = new Set();
  const paths = new Set();
  for (const repo of manifest.repos) {
    for (const field of ["name", "path", "url", "type", "owner"]) {
      if (typeof repo[field] !== "string" || repo[field].length === 0) {
        throw new Error(`repository entry is missing ${field}`);
      }
    }
    if (names.has(repo.name) || paths.has(repo.path)) {
      throw new Error(`duplicate repository name or path: ${repo.name}`);
    }
    if (!repo.path.startsWith("../yijie-") || !repo.url.startsWith("https://github.com/36Dge/")) {
      throw new Error(`repository ${repo.name} has an unexpected path or URL`);
    }
    names.add(repo.name);
    paths.add(repo.path);
    repo.branch ??= defaultBranch;
  }

  return manifest;
}

async function main() {
  const command = process.argv[2] ?? "list";
  const manifest = await loadManifest();
  if (command === "validate") {
    console.log(`Validated ${manifest.repos.length} repository entries.`);
    return;
  }
  if (command !== "list") {
    throw new Error(`unknown command: ${command}`);
  }
  for (const repo of manifest.repos) {
    console.log([repo.name, repo.path, repo.url, repo.branch].join("\t"));
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  await main();
}
