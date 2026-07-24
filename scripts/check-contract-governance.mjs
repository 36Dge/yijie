import { readFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import { loadManifest } from "./repo-manifest.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const classification = "contract-impact = none | additive | semantic | breaking";
const riskOrder = "breaking > semantic > additive > none";
const conditionalCompletion = "contract-impact != none";
const boundaryScope = ["跨版本", "持久化"];

const centralRequirements = new Map([
  [
    "AGENTS.md",
    [
      classification,
      "不会自动继承本文件",
      "Contract First 项目级强制评审门禁",
      "dirty 或浮动 sibling",
    ],
  ],
  [
    "docs/dev/contract-first.md",
    [
      "权威源路由",
      "不可绕过的开发与合并流程",
      "兼容方向与发布顺序",
      "例外与紧急变更",
      "fallback 完整 commit",
      "按第 3 节权威源路由",
    ],
  ],
  [
    "docs/adr/ADR-0011-enforce-contract-first-governance.md",
    ["Accepted", "补充并强化 ADR-0004", "不可变引用"],
  ],
  [
    ".github/pull_request_template.md",
    [
      "contract-impact: none",
      "contract-impact: additive",
      "contract-impact: semantic",
      "contract-impact: breaking",
      "计划或已发布 tag / 完整 commit",
      "Consumer Owner 逐项评审 / 例外",
      "权威源类别",
      "N/A + 理由",
      "migration / data / runtime / deployment compatibility",
      "### 临时例外",
      "跟踪 Issue",
    ],
  ],
]);

async function readRequired(relativePath) {
  try {
    return await readFile(path.join(root, relativePath), "utf8");
  } catch (error) {
    throw new Error(`missing governance file: ${relativePath}`, { cause: error });
  }
}

export async function validateContractGovernance({ requireSiblings = false } = {}) {
  for (const [relativePath, requirements] of centralRequirements) {
    const content = await readRequired(relativePath);
    for (const requirement of requirements) {
      if (!content.includes(requirement)) {
        throw new Error(`${relativePath} is missing governance marker: ${requirement}`);
      }
    }
  }

  const manifest = await loadManifest();
  const missing = [];
  let checked = 0;

  for (const repo of manifest.repos) {
    const agentsPath = path.resolve(root, repo.path, "AGENTS.md");
    let content;
    try {
      content = await readFile(agentsPath, "utf8");
    } catch {
      missing.push(repo.name);
      continue;
    }

    checked += 1;
    if (!content.includes(classification)) {
      throw new Error(`${repo.name}/AGENTS.md is missing the Contract First classification gate`);
    }
    if (!content.includes(riskOrder)) {
      throw new Error(`${repo.name}/AGENTS.md is missing the Contract First risk precedence`);
    }
    if (!content.includes(conditionalCompletion)) {
      throw new Error(`${repo.name}/AGENTS.md is missing the conditional completion gate`);
    }
    for (const marker of boundaryScope) {
      if (!content.includes(marker)) {
        throw new Error(`${repo.name}/AGENTS.md is missing boundary scope marker: ${marker}`);
      }
    }
  }

  if (requireSiblings && missing.length > 0) {
    throw new Error(`missing sibling repositories for governance validation: ${missing.join(", ")}`);
  }

  return { checked, missing };
}

async function main() {
  const requireSiblings = process.argv.includes("--require-siblings");
  const { checked, missing } = await validateContractGovernance({ requireSiblings });
  console.log(`Validated central Contract First governance and ${checked} sibling AGENTS.md files.`);
  if (missing.length > 0) {
    console.log(
      `Sibling checks not executed for unavailable repositories: ${missing.join(", ")}.`,
    );
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  await main();
}
