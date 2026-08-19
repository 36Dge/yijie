#!/usr/bin/env node

import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { lstatSync, readFileSync, realpathSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import process from "node:process";
import Ajv2020 from "ajv/dist/2020.js";
import YAML from "yaml";
import { validateApprovalTrustRoot } from "./approval-attestation.mjs";
import { serializedManifest } from "./release-manifest.mjs";

const MODULE_PATH = fileURLToPath(import.meta.url);
const FRAMEWORK_ROOT = resolve(dirname(MODULE_PATH), "..");
const DOMAIN = "codex-feature-delivery/first-bootstrap/v1";
const SHA_RE = /^(?:[0-9a-f]{40}|[0-9a-f]{64})$/;
const DIGEST_RE = /^sha256:[0-9a-f]{64}$/;
const REPOSITORY_RE = /^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/;
const ID_RE = /^[A-Za-z0-9][A-Za-z0-9._:@-]{0,127}$/;
const MAX_FILE_BYTES = 32 * 1024 * 1024;
const MAX_TOTAL_BYTES = 256 * 1024 * 1024;
const MAX_COMMITS = 500;
const MAX_TTL_MS = 24 * 60 * 60 * 1000;
const FATAL_UTF8 = new TextDecoder("utf-8", { fatal: true });

class VerificationError extends Error {
  constructor(message, code = "INVALID") {
    super(message);
    this.code = code;
  }
}

function fail(message, code = "INVALID") {
  throw new VerificationError(message, code);
}

function sha256(bytes) {
  return `sha256:${createHash("sha256").update(bytes).digest("hex")}`;
}

function compareUtf8(left, right) {
  return Buffer.compare(Buffer.from(left, "utf8"), Buffer.from(right, "utf8"));
}

export function decodeGitUtf8(buffer, label = "Git output") {
  if (!Buffer.isBuffer(buffer)) fail(`${label} 必须是 Buffer`);
  try {
    return FATAL_UTF8.decode(buffer);
  } catch {
    fail(`${label} 含非法 UTF-8；为避免 path/digest 别名，拒绝处理`);
  }
}

export function canonicalGitPath(value, label = "Git path") {
  if (typeof value !== "string" || value.length === 0 || value.includes("\0")) fail(`${label} 必须是非空、无 NUL 的 UTF-8 路径`);
  if (value !== value.normalize("NFC")) fail(`${label} 不是 NFC 规范路径：${JSON.stringify(value)}`);
  if (value.startsWith("/") || value.endsWith("/") || value.includes("\\") || value.includes("//")) fail(`${label} 不是规范 repo-relative POSIX 路径：${JSON.stringify(value)}`);
  if (/[\u0000-\u001f\u007f]/u.test(value)) fail(`${label} 含控制字符`);
  const segments = value.split("/");
  if (segments.some((segment) => segment === "" || segment === "." || segment === ".." || segment === ".git")) fail(`${label} 含非法 segment：${JSON.stringify(value)}`);
  return value;
}

function runGit(repoRoot, args, { binary = false, allowFailure = false, maxBuffer = 64 * 1024 * 1024 } = {}) {
  const result = spawnSync("git", ["-C", repoRoot, ...args], { encoding: binary ? null : "utf8", maxBuffer });
  if (!allowFailure && result.status !== 0) {
    const detail = binary ? Buffer.concat([result.stderr ?? Buffer.alloc(0), result.stdout ?? Buffer.alloc(0)]).toString("utf8") : `${result.stderr ?? ""}${result.stdout ?? ""}`;
    fail(`git ${args.join(" ")} 失败：${detail.trim()}`);
  }
  return result;
}

function exactCommit(repoRoot, value, label) {
  if (!SHA_RE.test(value)) fail(`${label} 必须是完整 40 或 64 位小写 Git SHA`);
  const result = runGit(repoRoot, ["rev-parse", "--verify", `${value}^{commit}`]);
  const resolved = result.stdout.trim();
  if (resolved !== value) fail(`${label} 未精确解析为 ${value}，实际 ${resolved}`);
  return resolved;
}

function strictYaml(source, label) {
  const document = YAML.parseDocument(source, { prettyErrors: true, uniqueKeys: true });
  if (document.errors.length > 0) fail(`${label}: ${document.errors.map((error) => error.message).join("; ")}`);
  return document.toJS({ maxAliasCount: 0 });
}

function canonicalJson(value) {
  if (value === null || typeof value === "boolean" || typeof value === "number" || typeof value === "string") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  if (value && typeof value === "object") return `{${Object.keys(value).sort(compareUtf8).map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(",")}}`;
  fail(`无法 canonicalize ${typeof value}`);
}

function validateSchema(name, value, label) {
  const schemaPath = resolve(FRAMEWORK_ROOT, "schemas", name);
  const schema = JSON.parse(readFileSync(schemaPath, "utf8"));
  const ajv = new Ajv2020({ allErrors: true, strict: true, validateFormats: false });
  const validate = ajv.compile(schema);
  if (validate(value)) return;
  const details = validate.errors?.map((error) => `${error.instancePath || "/"} ${error.message}`).join("; ") || "unknown schema error";
  fail(`${label} 不符合 canonical ${name}：${details}`);
}

function gitTreeEntries(repoRoot, commit) {
  const result = runGit(repoRoot, ["ls-tree", "-rz", "--full-tree", commit], { binary: true, maxBuffer: 128 * 1024 * 1024 });
  const records = decodeGitUtf8(result.stdout, `git ls-tree ${commit}`).split("\0").filter(Boolean);
  const entries = new Map();
  for (const record of records) {
    const tab = record.indexOf("\t");
    if (tab < 0) fail(`${commit} tree entry 编码无效`);
    const [mode, type, object] = record.slice(0, tab).split(" ");
    const path = canonicalGitPath(record.slice(tab + 1), `${commit} tree path`);
    if (entries.has(path)) fail(`${commit}:${path} tree entry 重复`);
    entries.set(path, { path, mode, type, object });
  }
  return entries;
}

function blobBytes(repoRoot, entry, label) {
  if (!entry) fail(`${label} 不存在`);
  if (entry.type !== "blob" || !["100644", "100755"].includes(entry.mode)) {
    fail(`${label} 必须是 100644|100755 普通 Git blob；拒绝 symlink/submodule/special mode=${entry.mode} type=${entry.type}`);
  }
  const sizeResult = runGit(repoRoot, ["cat-file", "-s", entry.object]);
  const size = Number(sizeResult.stdout.trim());
  if (!Number.isSafeInteger(size) || size < 0 || size > MAX_FILE_BYTES) fail(`${label} 超过单文件 ${MAX_FILE_BYTES} bytes 上限`);
  const result = runGit(repoRoot, ["cat-file", "blob", entry.object], { binary: true, maxBuffer: MAX_FILE_BYTES + 1024 });
  if (result.stdout.length !== size) fail(`${label} blob size 漂移`);
  return result.stdout;
}

function requiredBlob(repoRoot, tree, path, label = path) {
  const canonical = canonicalGitPath(path, label);
  return blobBytes(repoRoot, tree.get(canonical), label);
}

function changedFiles(repoRoot, base, head, headTree) {
  const result = runGit(repoRoot, ["diff", "--name-only", "-z", "--no-renames", base, head], { binary: true });
  const paths = decodeGitUtf8(result.stdout, `git diff ${base}..${head}`).split("\0").filter(Boolean).map((path) => canonicalGitPath(path, "changed path"));
  paths.sort(compareUtf8);
  if (paths.length === 0) fail("first bootstrap candidate 没有变更");
  if (new Set(paths).size !== paths.length) fail("changed-file set 含规范化重复路径");
  const files = [];
  let total = 0;
  for (const path of paths) {
    const entry = headTree.get(path);
    if (!entry) fail(`${path}: first bootstrap 不允许删除路径`);
    const bytes = blobBytes(repoRoot, entry, `${head}:${path}`);
    total += bytes.length;
    if (total > MAX_TOTAL_BYTES) fail(`first bootstrap payload 超过 ${MAX_TOTAL_BYTES} bytes 上限`);
    files.push({ path, mode: entry.mode, size: bytes.length, sha256: sha256(bytes), bytes });
  }
  return files;
}

function ensureLinearHistory(repoRoot, base, head) {
  const ancestor = runGit(repoRoot, ["merge-base", "--is-ancestor", base, head], { allowFailure: true });
  if (ancestor.status !== 0) fail(`base ${base} 不是 head ${head} 的祖先`, "OUT_OF_DATE");
  const lines = runGit(repoRoot, ["rev-list", "--reverse", "--parents", `${base}..${head}`]).stdout.trim().split("\n").filter(Boolean);
  if (lines.length === 0) fail("base 与 head 相同，缺少 bootstrap candidate");
  if (lines.length > MAX_COMMITS) fail(`bootstrap history 超过 ${MAX_COMMITS} commits`);
  let expectedParent = base;
  for (const line of lines) {
    const [commit, ...parents] = line.split(" ");
    if (parents.length !== 1 || parents[0] !== expectedParent) fail(`${commit}: first-bootstrap history 必须是从 base 开始的无 merge 线性链`);
    expectedParent = commit;
  }
  if (expectedParent !== head) fail("线性 history 未终止于指定 head");
  return lines.length;
}

function normalizeGitHubRemote(url) {
  const value = String(url).trim();
  let match = value.match(/^https:\/\/github\.com\/([^/]+)\/([^/]+?)(?:\.git)?$/i);
  if (!match) match = value.match(/^git@github\.com:([^/]+)\/([^/]+?)(?:\.git)?$/i);
  if (!match) match = value.match(/^ssh:\/\/git@github\.com\/([^/]+)\/([^/]+?)(?:\.git)?$/i);
  if (!match) fail(`origin remote 必须是 GitHub HTTPS/SSH repository URL：${JSON.stringify(value)}`);
  return `${match[1]}/${match[2]}`;
}

function parseTime(value, label) {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}T/.test(value)) fail(`${label} 必须是 ISO-8601 date-time`);
  const milliseconds = Date.parse(value);
  if (!Number.isFinite(milliseconds)) fail(`${label} 必须是有效 ISO-8601 date-time`);
  return { milliseconds, canonical: new Date(milliseconds).toISOString() };
}

function validateTimes(createdAt, expiresAt, now) {
  const created = parseTime(createdAt, "--created-at");
  const expires = parseTime(expiresAt, "--expires-at");
  if (created.milliseconds > now) fail("created_at 不得位于未来");
  if (expires.milliseconds <= now) fail("first-bootstrap authorization 已过期", "AUTHORIZATION_EXPIRED");
  if (expires.milliseconds <= created.milliseconds) fail("expires_at 必须晚于 created_at");
  if (expires.milliseconds - created.milliseconds > MAX_TTL_MS) fail("first-bootstrap authorization 有效期不得超过 24 小时");
  return { createdAt: created.canonical, expiresAt: expires.canonical };
}

function expectedCoveragePolicy(config, repoId) {
  const frameworkRoot = config.paths.framework_root;
  const governanceRoot = config.paths.governance_root;
  return {
    schema_version: 1,
    kind: "FeatureChangeCoveragePolicy",
    repository_id: repoId,
    feature_root: config.paths.feature_root,
    required_gate: config.ci.required_gate,
    protected_paths: [
      { path: ".github/workflows", match: "prefix", mode: "external_digest_only" },
      { path: ".feature-delivery.yaml", match: "exact", mode: "external_digest_only" },
      { path: frameworkRoot, match: "prefix", mode: "controlled_g4_or_exemption" },
      ...["gate-policy.yaml", "package.json", "package-lock.json", "RELEASE-MANIFEST.json"].map((name) => ({ path: `${frameworkRoot}/${name}`, match: "exact", mode: "external_digest_only" })),
      ...["policies", "schemas", "scripts"].map((name) => ({ path: `${frameworkRoot}/${name}`, match: "prefix", mode: "external_digest_only" })),
      { path: governanceRoot, match: "prefix", mode: "controlled_g4_or_exemption" },
      ...["approval-trust.yaml", "change-coverage-policy.yaml", "legacy-v1-allowlist.txt", "repository-registry.yaml"].map((name) => ({ path: `${governanceRoot}/${name}`, match: "exact", mode: "external_digest_only" })),
    ],
    exemptions: [],
  };
}

function renderWorkflow(config, repoId) {
  let source = readFileSync(resolve(FRAMEWORK_ROOT, "integrations/github/feature-delivery-coverage.yml"), "utf8");
  const replacements = {
    __FRAMEWORK_ROOT__: config.paths.framework_root,
    __FEATURE_ROOT__: config.paths.feature_root,
    __REPOSITORY_ID__: repoId,
    __TRUSTED_ENVIRONMENT__: "feature-delivery-trusted",
  };
  for (const [token, value] of Object.entries(replacements)) source = source.replaceAll(token, () => value);
  if (/__[A-Z0-9_]+__/.test(source)) fail("canonical workflow template 含未替换 token");
  return Buffer.from(source, "utf8");
}

function validateCodexEntrances(repoRoot, head, tree) {
  const exact = ["AGENTS.md", ".codex/config.toml", ".github/pull_request_template.md"];
  const prompts = [...tree.keys()].filter((path) => path.startsWith(".codex/prompts/") && path.endsWith(".md"));
  const tasks = [...tree.keys()].filter((path) => path.startsWith(".codex/tasks/") && path.endsWith(".md"));
  if (prompts.length === 0 || tasks.length === 0) fail("candidate 必须安装至少一个 Codex prompt 与 task 入口");
  const texts = [];
  for (const path of [...exact, ...prompts, ...tasks]) {
    const bytes = requiredBlob(repoRoot, tree, path, `${head}:${path}`);
    texts.push(decodeGitUtf8(bytes, `${head}:${path}`));
  }
  const aggregate = texts.join("\n");
  for (const token of ["Feature Delivery v2", "schema_version: 2", "G2C", "feature-delivery/trusted-coverage-status"]) {
    if (!aggregate.includes(token)) fail(`Codex/协作入口未完整声明 ${token}`);
  }
  const expectedPrTemplate = readFileSync(resolve(FRAMEWORK_ROOT, "integrations/github/pull_request_template.md"));
  const actualPrTemplate = requiredBlob(repoRoot, tree, ".github/pull_request_template.md", `${head}:.github/pull_request_template.md`);
  const expectedLines = decodeGitUtf8(expectedPrTemplate, "canonical PR template").split("\n").filter((line) => line.trim() !== "");
  const actualLines = decodeGitUtf8(actualPrTemplate, `${head}:.github/pull_request_template.md`).split("\n");
  let cursor = 0;
  for (const line of actualLines) if (cursor < expectedLines.length && line === expectedLines[cursor]) cursor += 1;
  if (cursor !== expectedLines.length) fail("candidate PR template 必须按原顺序保留全部 canonical 非空行；只允许附加项目专属段落");
}

function validateRelease(repoRoot, head, tree, frameworkPath) {
  const canonicalManifestPath = resolve(FRAMEWORK_ROOT, "RELEASE-MANIFEST.json");
  const canonicalManifestSource = readFileSync(canonicalManifestPath, "utf8");
  if (canonicalManifestSource !== serializedManifest(FRAMEWORK_ROOT)) fail("canonical RELEASE-MANIFEST.json 与当前 canonical payload 不一致");
  const manifest = JSON.parse(canonicalManifestSource);
  const manifestRelative = `${frameworkPath}/RELEASE-MANIFEST.json`;
  const candidateManifest = requiredBlob(repoRoot, tree, manifestRelative, `${head}:${manifestRelative}`);
  let candidateManifestValue;
  try {
    candidateManifestValue = JSON.parse(decodeGitUtf8(candidateManifest, `${head}:${manifestRelative}`));
  } catch (error) {
    fail(`${head}:${manifestRelative} 不是有效 JSON：${error.message}`);
  }
  if (candidateManifestValue?.distribution?.version !== manifest.distribution.version
      || candidateManifestValue?.distribution_digest !== manifest.distribution_digest) {
    fail(`candidate distribution ${candidateManifestValue?.distribution?.version ?? "UNKNOWN"} ${candidateManifestValue?.distribution_digest ?? "UNKNOWN"} 已过期；canonical 要求 ${manifest.distribution.version} ${manifest.distribution_digest}`, "STALE_DISTRIBUTION");
  }
  if (!candidateManifest.equals(Buffer.from(canonicalManifestSource, "utf8"))) fail("candidate RELEASE-MANIFEST.json 与 canonical 字节不一致");
  const expected = new Map(manifest.files.map((file) => [`${frameworkPath}/${file.path}`, file]));
  expected.set(manifestRelative, { path: "RELEASE-MANIFEST.json", mode: "100644", size: candidateManifest.length, sha256: sha256(candidateManifest) });
  const actualPaths = [...tree.keys()].filter((path) => path.startsWith(`${frameworkPath}/`)).sort(compareUtf8);
  const expectedPaths = [...expected.keys()].sort(compareUtf8);
  if (canonicalJson(actualPaths) !== canonicalJson(expectedPaths)) {
    const missing = expectedPaths.filter((path) => !tree.has(path));
    const extra = actualPaths.filter((path) => !expected.has(path));
    fail(`candidate runtime 文件集与 canonical manifest 不一致；missing=${missing.join(",") || "NONE"}; extra=${extra.join(",") || "NONE"}`);
  }
  for (const path of expectedPaths) {
    const entry = tree.get(path);
    const bytes = blobBytes(repoRoot, entry, `${head}:${path}`);
    const expectedFile = expected.get(path);
    if (entry.mode !== expectedFile.mode || bytes.length !== expectedFile.size || sha256(bytes) !== expectedFile.sha256) {
      fail(`${head}:${path} 未匹配 canonical mode/size/SHA-256`);
    }
  }
  const active = requiredBlob(repoRoot, tree, `${frameworkPath}/gate-policy.yaml`, `${head}:active policy`);
  const snapshot = requiredBlob(repoRoot, tree, `${frameworkPath}/${manifest.active_policy.snapshot}`, `${head}:policy snapshot`);
  const canonicalActive = readFileSync(resolve(FRAMEWORK_ROOT, "gate-policy.yaml"));
  if (!active.equals(snapshot) || !active.equals(canonicalActive) || sha256(active) !== manifest.active_policy.digest) {
    fail("candidate active policy、content-addressed snapshot 与 canonical policy 不一致");
  }
  return manifest;
}

class LengthPrefixedDigest {
  constructor() {
    this.hash = createHash("sha256");
  }

  field(name, value) {
    const label = Buffer.from(name, "utf8");
    const bytes = Buffer.isBuffer(value) ? value : Buffer.from(String(value), "utf8");
    const header = Buffer.alloc(12);
    header.writeUInt32BE(label.length, 0);
    header.writeBigUInt64BE(BigInt(bytes.length), 4);
    this.hash.update(header);
    this.hash.update(label);
    this.hash.update(bytes);
  }

  finish() {
    return `sha256:${this.hash.digest("hex")}`;
  }
}

export function computeFirstBootstrapDigest(bindings, files) {
  const digest = new LengthPrefixedDigest();
  digest.field("domain", DOMAIN);
  for (const [name, value] of [
    ["distribution.version", bindings.distributionVersion],
    ["distribution.digest", bindings.distributionDigest],
    ["policy.digest", bindings.policyDigest],
    ["repository.full_name", bindings.repository],
    ["repository.id", bindings.repoId],
    ["target.branch", bindings.targetBranch],
    ["git.base", bindings.base],
    ["git.head", bindings.head],
    ["git.tree", bindings.tree],
    ["authorization.id", bindings.authorizationId],
    ["authorization.approval_reference", bindings.approvalReference],
    ["authorization.created_at", bindings.createdAt],
    ["authorization.expires_at", bindings.expiresAt],
    ["component.project_config", bindings.projectConfigDigest],
    ["component.repository_registry", bindings.registryDigest],
    ["component.coverage_policy", bindings.coveragePolicyDigest],
    ["component.empty_trust_root", bindings.trustRootDigest],
    ["component.workflow", bindings.workflowDigest],
    ["changed_file.count", files.length],
  ]) digest.field(name, value);
  files.forEach((file, index) => {
    const prefix = `changed_file.${String(index).padStart(6, "0")}`;
    digest.field(`${prefix}.path`, file.path);
    digest.field(`${prefix}.mode`, file.mode);
    digest.field(`${prefix}.size`, file.size);
    digest.field(`${prefix}.content`, file.bytes);
  });
  return digest.finish();
}

function validateBaseTarget(repoRoot, base, targetBranch) {
  const branchCheck = runGit(repoRoot, ["check-ref-format", "--branch", targetBranch], { allowFailure: true });
  if (branchCheck.status !== 0 || targetBranch.startsWith("refs/")) fail(`--target-branch 不是安全短分支名：${targetBranch}`);
  const remoteRef = `refs/remotes/origin/${targetBranch}`;
  const remote = runGit(repoRoot, ["rev-parse", "--verify", `${remoteRef}^{commit}`], { allowFailure: true });
  if (remote.status !== 0) fail(`本地缺少精确 target base ref ${remoteRef}；请先 fetch`);
  if (remote.stdout.trim() !== base) fail(`${remoteRef}=${remote.stdout.trim()}，与 --base=${base} 漂移`, "OUT_OF_DATE");
}

function validateInputs(options) {
  if (!REPOSITORY_RE.test(options.repository)) fail("--repository 必须是 GitHub owner/repo");
  if (!/^[a-z][a-z0-9._-]*$/.test(options.repoId)) fail("--repo-id 无效");
  if (!ID_RE.test(options.authorizationId)) fail("--authorization-id 无效");
  if (typeof options.approvalReference !== "string" || !options.approvalReference.trim() || options.approvalReference.length > 512 || /[\u0000-\u001f\u007f]/u.test(options.approvalReference)) fail("--approval-reference 必须是 1..512 字符的无控制字符引用");
  if (options.bootstrapDigest && !DIGEST_RE.test(options.bootstrapDigest)) fail("--bootstrap-digest 必须是 sha256:<64 lowercase hex>");
}

export function verifyFirstBootstrap(options, { now = Date.now() } = {}) {
  validateInputs(options);
  const requestedRoot = resolve(options.repoRoot);
  const requestedMetadata = lstatSync(requestedRoot);
  if (!requestedMetadata.isDirectory() || requestedMetadata.isSymbolicLink()) fail("--repo-root leaf 必须是非 symlink Git worktree 根目录");
  const repoRoot = realpathSync(requestedRoot);
  const rootMetadata = lstatSync(repoRoot);
  if (!rootMetadata.isDirectory() || rootMetadata.isSymbolicLink()) fail("--repo-root 必须是非 symlink Git worktree 根目录");
  const exactRoot = runGit(repoRoot, ["rev-parse", "--show-toplevel"]).stdout.trim();
  if (realpathSync(exactRoot) !== repoRoot) fail("--repo-root 必须精确指向 Git worktree 根");
  const base = exactCommit(repoRoot, options.base, "--base");
  const head = exactCommit(repoRoot, options.head, "--head");
  validateBaseTarget(repoRoot, base, options.targetBranch);
  const actualRepository = normalizeGitHubRemote(runGit(repoRoot, ["remote", "get-url", "origin"]).stdout);
  if (actualRepository.toLowerCase() !== options.repository.toLowerCase()) fail(`origin=${actualRepository} 与 --repository=${options.repository} 不一致`);
  const commitCount = ensureLinearHistory(repoRoot, base, head);
  const baseTree = gitTreeEntries(repoRoot, base);
  if (baseTree.has(".feature-delivery.yaml")) fail("target base 已存在 Feature Delivery 项目配置；禁止 first-bootstrap，必须使用普通 coverage checker", "BASE_ALREADY_INITIALIZED");
  const headTree = gitTreeEntries(repoRoot, head);
  const files = changedFiles(repoRoot, base, head, headTree);
  const tree = runGit(repoRoot, ["rev-parse", "--verify", `${head}^{tree}`]).stdout.trim();
  const times = validateTimes(options.createdAt, options.expiresAt, now);

  const configBytes = requiredBlob(repoRoot, headTree, ".feature-delivery.yaml", `${head}:.feature-delivery.yaml`);
  const config = strictYaml(decodeGitUtf8(configBytes, `${head}:.feature-delivery.yaml`), `${head}:.feature-delivery.yaml`);
  validateSchema("project-config.schema.json", config, "candidate project config");
  const logicalRoots = [config.paths.framework_root, config.paths.feature_root, config.paths.governance_root].map((path, index) => canonicalGitPath(path, `project root[${index}]`));
  for (let left = 0; left < logicalRoots.length; left += 1) {
    for (let right = left + 1; right < logicalRoots.length; right += 1) {
      const a = logicalRoots[left];
      const b = logicalRoots[right];
      if (a === b || a.startsWith(`${b}/`) || b.startsWith(`${a}/`)) fail("framework_root、feature_root、governance_root 必须互不重叠");
    }
  }
  if (config.repository.current_id !== options.repoId) fail("project config repository.current_id 必须与 --repo-id 一致");
  if (config.scm.primary_branch !== options.targetBranch) fail("project config scm.primary_branch 与 --target-branch 不一致");
  if (config.ci.provider !== "github") fail("first-bootstrap GitHub verifier 只接受 ci.provider=github");

  const registryPath = canonicalGitPath(config.paths.repository_registry, "paths.repository_registry");
  const registryBytes = requiredBlob(repoRoot, headTree, registryPath, `${head}:${registryPath}`);
  const registry = strictYaml(decodeGitUtf8(registryBytes, `${head}:${registryPath}`), `${head}:${registryPath}`);
  validateSchema("repository-registry.schema.json", registry, "candidate repository registry");
  const repositoryIds = registry.repositories.map((item) => item.id);
  if (new Set(repositoryIds).size !== repositoryIds.length) fail("repository registry 含重复 id");
  for (const [index, repository] of registry.repositories.entries()) {
    if (repository.kind === "current" && repository.root !== ".") fail(`registry.repositories[${index}] current root 必须为 .`);
    if (repository.kind === "external" && (!/^\.\.\/[A-Za-z0-9][A-Za-z0-9._-]*$/.test(repository.root) || repository.root.slice(3) !== repository.name)) {
      fail(`registry.repositories[${index}] external root 必须是匹配 name 的单层 ../<name>`);
    }
    if (repository.kind === "managed") canonicalGitPath(repository.root, `registry.repositories[${index}].root`);
  }
  const current = registry.repositories.filter((item) => item.kind === "current");
  if (current.length !== 1 || current[0].id !== options.repoId || current[0].name !== options.repoId || current[0].root !== ".") fail("repository registry 必须恰好包含匹配 --repo-id 的 current repository");
  if (normalizeGitHubRemote(current[0].url).toLowerCase() !== options.repository.toLowerCase()) fail("repository registry URL 与 --repository/actual origin 不一致");

  const governanceRoot = canonicalGitPath(config.paths.governance_root, "paths.governance_root");
  if (!registryPath.startsWith(`${governanceRoot}/`)) fail("repository registry 必须位于 governance root 内");
  const trustPath = `${governanceRoot}/approval-trust.yaml`;
  const trustBytes = requiredBlob(repoRoot, headTree, trustPath, `${head}:${trustPath}`);
  const trust = strictYaml(decodeGitUtf8(trustBytes, `${head}:${trustPath}`), `${head}:${trustPath}`);
  validateSchema("approval-trust.schema.json", trust, "candidate approval trust");
  const trustErrors = validateApprovalTrustRoot(trust);
  if (trustErrors.length > 0) fail(`candidate approval trust 无效：${trustErrors.join("; ")}`);
  if (trust.keys.length !== 0) fail("first bootstrap approval trust 必须严格为 keys: []");

  const policyPath = `${governanceRoot}/change-coverage-policy.yaml`;
  const coverageBytes = requiredBlob(repoRoot, headTree, policyPath, `${head}:${policyPath}`);
  const coverage = strictYaml(decodeGitUtf8(coverageBytes, `${head}:${policyPath}`), `${head}:${policyPath}`);
  validateSchema("change-coverage-policy.schema.json", coverage, "candidate coverage policy");
  if (coverage.exemptions.length !== 0) fail("candidate 最终 coverage policy 必须 exemptions: []");
  if (canonicalJson(coverage) !== canonicalJson(expectedCoveragePolicy(config, options.repoId))) fail("candidate coverage policy 未精确匹配 canonical fail-closed routing");

  const workflowPath = ".github/workflows/feature-delivery-coverage.yml";
  const workflowBytes = requiredBlob(repoRoot, headTree, workflowPath, `${head}:${workflowPath}`);
  if (!workflowBytes.equals(renderWorkflow(config, options.repoId))) fail("candidate base-trusted workflow 与 canonical rendered workflow 字节不一致");
  validateCodexEntrances(repoRoot, head, headTree);
  const manifest = validateRelease(repoRoot, head, headTree, canonicalGitPath(config.paths.framework_root, "paths.framework_root"));

  const bootstrapRoots = [config.paths.framework_root, governanceRoot];
  const baseOwnedPaths = [".feature-delivery.yaml", workflowPath];
  const preexisting = [...baseTree.keys()].filter((path) => baseOwnedPaths.includes(path)
    || bootstrapRoots.some((root) => path === root || path.startsWith(`${root}/`)));
  if (preexisting.length > 0) fail(`target base 含 partial/ambiguous v2 control paths，拒绝 first-bootstrap：${preexisting.join(", ")}`);

  const legacyPath = `${governanceRoot}/legacy-v1-allowlist.txt`;
  const legacy = decodeGitUtf8(requiredBlob(repoRoot, headTree, legacyPath, `${head}:${legacyPath}`), `${head}:${legacyPath}`);
  if (legacy.split(/\r?\n/u).some((line) => line.trim() && !line.trim().startsWith("#"))) fail("全新 bootstrap 的 legacy allowlist 必须为空");

  const bindings = {
    distributionVersion: manifest.distribution.version,
    distributionDigest: manifest.distribution_digest,
    policyDigest: manifest.active_policy.digest,
    repository: options.repository,
    repoId: options.repoId,
    targetBranch: options.targetBranch,
    base,
    head,
    tree,
    authorizationId: options.authorizationId,
    approvalReference: options.approvalReference,
    createdAt: times.createdAt,
    expiresAt: times.expiresAt,
    projectConfigDigest: sha256(configBytes),
    registryDigest: sha256(registryBytes),
    coveragePolicyDigest: sha256(coverageBytes),
    trustRootDigest: sha256(trustBytes),
    workflowDigest: sha256(workflowBytes),
  };
  const digest = computeFirstBootstrapDigest(bindings, files);
  const summaryFiles = files.map(({ bytes: _bytes, ...file }) => file);
  const report = {
    valid: options.bootstrapDigest === digest,
    verdict: options.bootstrapDigest === digest ? "BOOTSTRAP_DIGEST_APPLIED" : "BOOTSTRAP_DIGEST_REQUIRED",
    domain: DOMAIN,
    repository: options.repository,
    repository_id: options.repoId,
    target_branch: options.targetBranch,
    base_sha: base,
    head_sha: head,
    candidate_tree_sha: tree,
    linear_commit_count: commitCount,
    distribution: { version: manifest.distribution.version, digest: manifest.distribution_digest },
    active_policy_digest: manifest.active_policy.digest,
    authorization: { id: options.authorizationId, approval_reference: options.approvalReference, created_at: times.createdAt, expires_at: times.expiresAt },
    component_digests: {
      project_config: bindings.projectConfigDigest,
      repository_registry: bindings.registryDigest,
      coverage_policy: bindings.coveragePolicyDigest,
      empty_trust_root: bindings.trustRootDigest,
      workflow: bindings.workflowDigest,
    },
    changed_file_count: summaryFiles.length,
    changed_files: summaryFiles,
    expected_bootstrap_digest: digest,
    errors: options.bootstrapDigest === digest ? [] : ["仓库外 bootstrap digest 未提供或与当前 exact candidate 不一致"],
    warnings: ["本报告只验证首次安装候选；不配置 GitHub App、Environment、required checks 或 branch protection。"],
  };
  return report;
}

function usage(stream = process.stdout) {
  stream.write(`Usage:
  verify-first-bootstrap.mjs \\
    --repo-root DIR --repository OWNER/REPO --repo-id ID --target-branch BRANCH \\
    --base SHA --head SHA --authorization-id ID --approval-reference REF \\
    --created-at ISO --expires-at ISO [--bootstrap-digest sha256:...] [--json]

The bootstrap digest may also come from CFD_BOOTSTRAP_APPROVAL_DIGEST.
No candidate checkout, script, workflow, hook, or dependency is executed.
`);
}

function parseArgs(argv) {
  const options = { repoRoot: null, repository: null, repoId: null, targetBranch: null, base: null, head: null, authorizationId: null, approvalReference: null, createdAt: null, expiresAt: null, bootstrapDigest: process.env.CFD_BOOTSTRAP_APPROVAL_DIGEST || null, json: false };
  const names = new Map([
    ["--repo-root", "repoRoot"], ["--repository", "repository"], ["--repo-id", "repoId"], ["--target-branch", "targetBranch"],
    ["--base", "base"], ["--head", "head"], ["--authorization-id", "authorizationId"], ["--approval-reference", "approvalReference"],
    ["--created-at", "createdAt"], ["--expires-at", "expiresAt"], ["--bootstrap-digest", "bootstrapDigest"],
  ]);
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "-h" || arg === "--help") return { help: true };
    if (arg === "--json") { options.json = true; continue; }
    const field = names.get(arg);
    if (!field) fail(`未知参数：${arg}`);
    const value = argv[++index];
    if (!value) fail(`${arg} 缺少值`);
    options[field] = value;
  }
  for (const [arg, field] of names) {
    if (arg === "--bootstrap-digest") continue;
    if (!options[field]) fail(`${arg} 必填`);
  }
  return options;
}

export function main(argv = process.argv.slice(2)) {
  let options;
  try {
    options = parseArgs(argv);
    if (options.help) { usage(); return; }
    const report = verifyFirstBootstrap(options);
    if (options.json) process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
    else process.stdout.write(`${report.verdict} ${report.expected_bootstrap_digest}\n`);
    process.exitCode = report.valid ? 0 : 1;
  } catch (error) {
    const report = { valid: false, verdict: error.code || "INVALID", errors: [error.message] };
    if (options?.json || argv.includes("--json")) process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
    else process.stderr.write(`verify-first-bootstrap: ${error.message}\n`);
    process.exitCode = error.code === "OUT_OF_DATE" ? 1 : 2;
  }
}

function isDirectInvocation() {
  if (!process.argv[1]) return false;
  try {
    return realpathSync(resolve(process.argv[1])) === realpathSync(MODULE_PATH);
  } catch {
    return false;
  }
}

if (isDirectInvocation()) main();
