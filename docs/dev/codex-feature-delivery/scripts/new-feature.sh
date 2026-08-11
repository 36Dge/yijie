#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  new-feature.sh FEAT-ID slug [options]

Options:
  --profile lite|standard|controlled
  --target local_engineering|staging|production
  --title TITLE
  --owner OWNER
  --repository-id ID
  --repository-identity ID
  --output-root DIRECTORY
  -h, --help

Defaults: profile=standard, target=local_engineering,
output-root=<git-root>/docs/features,
owner=git user.name (or current OS user),
repository-id=owning framework coverage policy ID (external worktree: Git root basename).

The command must run from inside the Git worktree that owns the new Feature.
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi
if [[ "$#" -lt 2 ]]; then
  usage >&2
  exit 2
fi

feature_id="$1"
feature_slug="$2"
shift 2

profile="standard"
delivery_target="local_engineering"
title="${feature_slug//-/ }"
owner="$(git config --get user.name 2>/dev/null || true)"
if [[ -z "$owner" ]]; then
  owner="$(id -un)"
fi
repository_identity="$(git config --get remote.origin.url 2>/dev/null || true)"
repository_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
[[ -n "$repository_root" ]] || { echo "ERROR: 必须从新 Feature 所属的 Git worktree 内运行。" >&2; exit 2; }
repository_root="$(CDPATH= cd -- "$repository_root" && pwd -P)"
repository_name="${repository_root##*/}"
repository_id=""
output_root="$repository_root/docs/features"

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --profile)
      [[ "$#" -ge 2 ]] || { echo "ERROR: --profile 缺少值。" >&2; exit 2; }
      profile="$2"
      shift 2
      ;;
    --target)
      [[ "$#" -ge 2 ]] || { echo "ERROR: --target 缺少值。" >&2; exit 2; }
      delivery_target="$2"
      shift 2
      ;;
    --title)
      [[ "$#" -ge 2 ]] || { echo "ERROR: --title 缺少值。" >&2; exit 2; }
      title="$2"
      shift 2
      ;;
    --owner)
      [[ "$#" -ge 2 ]] || { echo "ERROR: --owner 缺少值。" >&2; exit 2; }
      owner="$2"
      shift 2
      ;;
    --repository-id)
      [[ "$#" -ge 2 ]] || { echo "ERROR: --repository-id 缺少值。" >&2; exit 2; }
      repository_id="$2"
      shift 2
      ;;
    --repository-identity)
      [[ "$#" -ge 2 ]] || { echo "ERROR: --repository-identity 缺少值。" >&2; exit 2; }
      repository_identity="$2"
      shift 2
      ;;
    --output-root)
      [[ "$#" -ge 2 ]] || { echo "ERROR: --output-root 缺少值。" >&2; exit 2; }
      output_root="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: 未知参数：$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

[[ "$feature_id" =~ ^FEAT-[A-Z0-9][A-Z0-9.-]*$ ]] || { echo "ERROR: FEAT-ID 必须符合 FEAT-*，并使用大写标识。" >&2; exit 2; }
[[ "$feature_slug" =~ ^[a-z0-9][a-z0-9._-]*$ ]] || { echo "ERROR: slug 只能使用小写字母、数字、点、下划线和连字符。" >&2; exit 2; }
case "$profile" in lite|standard|controlled) ;; *) echo "ERROR: 无效 profile：$profile" >&2; exit 2;; esac
case "$delivery_target" in local_engineering|staging|production) ;; *) echo "ERROR: 无效 target：$delivery_target" >&2; exit 2;; esac
if [[ -z "$title" || -z "$owner" || "$title" == *$'\n'* || "$title" == *$'\r'* || "$owner" == *$'\n'* || "$owner" == *$'\r'* || "$title" == *'{{'* || "$owner" == *'{{'* ]]; then
  echo "ERROR: title/owner 不能为空，且不能包含换行或保留模板边界 {{。" >&2
  exit 2
fi
[[ "$repository_name" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || { echo "ERROR: 无法推导安全的 current repository name：$repository_name" >&2; exit 2; }

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
template_dir="$script_dir/../templates/feature-package"
framework_root="$(CDPATH= cd -- "$script_dir/../../../.." && pwd -P)"
if [[ -z "$repository_id" ]]; then
  if [[ "$repository_root" == "$framework_root" ]]; then
    if ! repository_id="$(
      cd "$framework_root"
      node --input-type=module - "$script_dir/../change-coverage-policy.yaml" <<'NODE'
import { readFileSync } from "node:fs";
import YAML from "yaml";
const policy = YAML.parse(readFileSync(process.argv[2], "utf8"), { uniqueKeys: true });
if (typeof policy?.repository_id !== "string" || !policy.repository_id) throw new Error("coverage policy repository_id missing");
process.stdout.write(policy.repository_id);
NODE
    )"; then
      echo "ERROR: 无法从 change-coverage-policy.yaml 读取 repository_id。" >&2
      exit 1
    fi
  else
    repository_id="$(printf '%s' "$repository_name" | LC_ALL=C tr '[:upper:]' '[:lower:]')"
  fi
fi
if [[ -z "$repository_identity" ]]; then
  repository_identity="local:$repository_id"
fi
if [[ -z "$repository_identity" || "$repository_identity" =~ [[:space:]] || "$repository_identity" == "." || "$repository_identity" == ".." || "$repository_identity" == *'{{'* ]]; then
  echo "ERROR: repository identity 必须是无空白的 canonical identity。" >&2
  exit 2
fi
[[ "$repository_id" =~ ^[a-z][a-z0-9._-]*$ ]] || { echo "ERROR: repository ID 必须以小写字母开头，且只能使用小写字母、数字、点、下划线和连字符。" >&2; exit 2; }
today="$(date +%Y-%m-%d)"

[[ -d "$template_dir" ]] || { echo "ERROR: 找不到模板目录：$template_dir" >&2; exit 1; }
mkdir -p "$output_root"
output_root="$(CDPATH= cd -- "$output_root" && pwd -P)"
target_dir="$output_root/$feature_id-$feature_slug"
[[ ! -e "$target_dir" ]] || { echo "ERROR: 目标已存在，不会覆盖：$target_dir" >&2; exit 1; }

# 在目标同级目录完成全部生成与校验；只有校验成功后才用一次 rename 发布。
staging_dir="$(mktemp -d "$output_root/$feature_id-$feature_slug.tmp.XXXXXX")"
cleanup_staging() {
  if [[ -n "${staging_dir:-}" && -d "$staging_dir" ]]; then
    case "$staging_dir" in
      "$output_root/$feature_id-$feature_slug.tmp."*) rm -rf -- "$staging_dir" ;;
      *) echo "ERROR: 拒绝清理非预期临时目录：$staging_dir" >&2 ;;
    esac
  fi
}
trap cleanup_staging EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

copy_template() {
  cp "$template_dir/$1" "$staging_dir/$1"
}

copy_template feature.yaml
copy_template evidence.yaml
copy_template decisions.yaml
copy_template 00-feature-brief.md
copy_template 01-requirements.md
copy_template 02-impact-assessment.md
copy_template 06-test-plan.md
copy_template 07-implementation-plan.md
copy_template 08-verification-report.md

artifact_03_applicability="not_applicable"
artifact_03_reason="lite_profile"
artifact_05_applicability="not_applicable"
artifact_05_reason="lite_profile"
if [[ "$profile" != "lite" ]]; then
  copy_template 03-decisions-and-risks.md
  copy_template 05-technical-design.md
  artifact_03_applicability="required"
  artifact_03_reason="profile_${profile}"
  artifact_05_applicability="required"
  artifact_05_reason="profile_${profile}"
fi

artifact_09_applicability="not_applicable"
artifact_09_reason="local_engineering_target"
if [[ "$delivery_target" != "local_engineering" ]]; then
  copy_template 09-release-and-rollback.md
  artifact_09_applicability="required"
  artifact_09_reason="target_${delivery_target}"
fi

# Contract Plan 只在可声明 Boundary 的 Profile 中按需 materialize；Summary 只在 terminal Gate 后 materialize。
artifact_04_applicability="not_applicable"
artifact_04_reason="lite_profile"
if [[ "$profile" != "lite" ]]; then
  artifact_04_applicability="conditional"
  artifact_04_reason="materialize_when_boundary_declared"
fi

policy_metadata="$(node "$script_dir/policy-registry.mjs" active-metadata)" || { echo "ERROR: active gate policy 或其内容寻址快照无效。" >&2; exit 1; }
IFS=$'\t' read -r policy_id policy_version policy_digest <<< "$policy_metadata"
[[ -n "$policy_id" && "$policy_version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ && "$policy_digest" =~ ^sha256:[0-9a-f]{64}$ ]] || { echo "ERROR: 无法解析 active gate policy metadata。" >&2; exit 1; }

export CFD_FEATURE_ID="$feature_id" CFD_FEATURE_SLUG="$feature_slug"
export CFD_TITLE="$title" CFD_OWNER="$owner"
export CFD_PROFILE="$profile" CFD_DELIVERY_TARGET="$delivery_target" CFD_DATE="$today" CFD_REPOSITORY_ID="$repository_id" CFD_REPOSITORY_IDENTITY="$repository_identity" CFD_REPOSITORY_NAME="$repository_name"
export CFD_POLICY_ID="$policy_id" CFD_POLICY_VERSION="$policy_version" CFD_POLICY_DIGEST="$policy_digest"
export CFD_ARTIFACT_03_APPLICABILITY="$artifact_03_applicability" CFD_ARTIFACT_03_REASON="$artifact_03_reason"
export CFD_ARTIFACT_04_APPLICABILITY="$artifact_04_applicability" CFD_ARTIFACT_04_REASON="$artifact_04_reason"
export CFD_ARTIFACT_05_APPLICABILITY="$artifact_05_applicability" CFD_ARTIFACT_05_REASON="$artifact_05_reason"
export CFD_ARTIFACT_09_APPLICABILITY="$artifact_09_applicability" CFD_ARTIFACT_09_REASON="$artifact_09_reason"

(
cd "$script_dir/../../../.."
node --input-type=module - "$staging_dir" <<'NODE'
import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import YAML from "yaml";

const directory = process.argv[2];
const replacements = {
  FEATURE_ID: process.env.CFD_FEATURE_ID,
  FEATURE_SLUG: process.env.CFD_FEATURE_SLUG,
  TITLE: process.env.CFD_TITLE,
  OWNER: process.env.CFD_OWNER,
  OWNER_ID: process.env.CFD_OWNER,
  PROFILE: process.env.CFD_PROFILE,
  DELIVERY_TARGET: process.env.CFD_DELIVERY_TARGET,
  REPOSITORY_ID: process.env.CFD_REPOSITORY_ID,
  REPOSITORY_IDENTITY: process.env.CFD_REPOSITORY_IDENTITY,
  REPOSITORY_NAME: process.env.CFD_REPOSITORY_NAME,
  DATE: process.env.CFD_DATE,
  POLICY_ID: process.env.CFD_POLICY_ID,
  POLICY_VERSION: process.env.CFD_POLICY_VERSION,
  POLICY_DIGEST: process.env.CFD_POLICY_DIGEST,
  ARTIFACT_03_APPLICABILITY: process.env.CFD_ARTIFACT_03_APPLICABILITY,
  ARTIFACT_03_REASON: process.env.CFD_ARTIFACT_03_REASON,
  ARTIFACT_04_APPLICABILITY: process.env.CFD_ARTIFACT_04_APPLICABILITY,
  ARTIFACT_04_REASON: process.env.CFD_ARTIFACT_04_REASON,
  ARTIFACT_05_APPLICABILITY: process.env.CFD_ARTIFACT_05_APPLICABILITY,
  ARTIFACT_05_REASON: process.env.CFD_ARTIFACT_05_REASON,
  ARTIFACT_09_APPLICABILITY: process.env.CFD_ARTIFACT_09_APPLICABILITY,
  ARTIFACT_09_REASON: process.env.CFD_ARTIFACT_09_REASON,
};

function replaceTokens(source, values, transform = (value) => value) {
  let result = source;
  for (const [key, value] of Object.entries(values)) {
    result = result.replaceAll(`{{${key}}}`, () => transform(String(value)));
  }
  return result;
}

function writeYaml(name, mutate) {
  const path = join(directory, name);
  const document = YAML.parseDocument(readFileSync(path, "utf8"), { uniqueKeys: true });
  if (document.errors.length > 0) throw new Error(`${name}: ${document.errors.map((error) => error.message).join("; ")}`);
  mutate(document);
  // YAML 值一律通过 Document API 写入；文本替换只处理保留下来的注释示例。
  const commentSafe = (value) => value.replaceAll("\r", "\\r").replaceAll("\n", "\\n");
  writeFileSync(path, replaceTokens(document.toString({ lineWidth: 0 }), replacements, commentSafe));
}

writeYaml("feature.yaml", (document) => {
  document.setIn(["policy", "id"], replacements.POLICY_ID);
  document.setIn(["policy", "version"], replacements.POLICY_VERSION);
  document.setIn(["policy", "digest"], replacements.POLICY_DIGEST);
  document.setIn(["feature", "id"], replacements.FEATURE_ID);
  document.setIn(["feature", "slug"], replacements.FEATURE_SLUG);
  document.setIn(["feature", "title"], replacements.TITLE);
  document.setIn(["feature", "summary"], replacements.TITLE);
  document.setIn(["feature", "profile"], replacements.PROFILE);
  document.setIn(["feature", "delivery_target"], replacements.DELIVERY_TARGET);
  document.setIn(["feature", "created_at"], replacements.DATE);
  document.setIn(["feature", "updated_at"], replacements.DATE);
  document.setIn(["feature", "owners", "accountable"], replacements.OWNER);
  document.setIn(["feature", "owners", "role_assignments", 0, "actor"], replacements.OWNER);
  document.setIn(["repositories", 0, "id"], replacements.REPOSITORY_ID);
  document.setIn(["repositories", 0, "identity", "kind"], "current");
  document.setIn(["repositories", 0, "identity", "name"], replacements.REPOSITORY_NAME);
  document.setIn(["repositories", 0, "identity", "url"], replacements.REPOSITORY_IDENTITY);
  document.setIn(["repositories", 0, "identity", "root"], ".");
  document.setIn(["slices", 0, "repositories", 0], replacements.REPOSITORY_ID);
  document.setIn(["slices", 0, "paths", 0, "repository"], replacements.REPOSITORY_ID);
  document.setIn(["acceptance_criteria", 0, "statement"], `${replacements.TITLE} 的最小可验证结果`);
  const artifacts = document.get("artifacts", true)?.items ?? [];
  const settings = new Map([
    ["ART-DECISIONS", [replacements.ARTIFACT_03_APPLICABILITY, replacements.ARTIFACT_03_REASON]],
    ["ART-CONTRACT", [replacements.ARTIFACT_04_APPLICABILITY, replacements.ARTIFACT_04_REASON]],
    ["ART-DESIGN", [replacements.ARTIFACT_05_APPLICABILITY, replacements.ARTIFACT_05_REASON]],
    ["ART-RELEASE", [replacements.ARTIFACT_09_APPLICABILITY, replacements.ARTIFACT_09_REASON]],
  ]);
  for (let index = 0; index < artifacts.length; index += 1) {
    const id = document.getIn(["artifacts", index, "id"]);
    const setting = settings.get(id);
    if (!setting) continue;
    document.setIn(["artifacts", index, "applicability"], setting[0]);
    document.setIn(["artifacts", index, "reason"], setting[1]);
  }
});
writeYaml("evidence.yaml", (document) => document.set("feature_id", replacements.FEATURE_ID));
writeYaml("decisions.yaml", (document) => document.set("feature_id", replacements.FEATURE_ID));

for (const name of readdirSync(directory)) {
  const path = join(directory, name);
  if (!/\.md$/.test(name)) continue;
  writeFileSync(path, replaceTokens(readFileSync(path, "utf8"), replacements));
}
NODE
)

validation_output=""
if ! validation_output="$(node "$script_dir/evaluate-feature-package.mjs" --repository-root "$repository_root" "$staging_dir" 2>&1)"; then
  echo "ERROR: 生成结果未通过 Feature Package v2 校验；目标未发布。" >&2
  printf '%s\n' "$validation_output" >&2
  exit 1
fi

# rename 在同一文件系统内原子发布。发布前再次检查，绝不主动覆盖现有目标。
[[ ! -e "$target_dir" ]] || { echo "ERROR: 目标在生成期间已出现，不会覆盖：$target_dir" >&2; exit 1; }
mv -- "$staging_dir" "$target_dir"
staging_dir=""

echo "Created Feature Package v2:"
echo "  $target_dir"
echo "  profile=$profile target=$delivery_target repository=$repository_id"
echo
echo "Next:"
echo "  1. 完成当前 Profile 已 materialize 的规范文件，并删除不适用的示例行。"
echo "  2. 记录真实 baseline 到 evidence.yaml，再把完整 SHA/Evidence ID 写入 feature.yaml。"
echo "  3. 运行：$script_dir/check-feature-package.sh \"$target_dir\""
echo "  4. 运行 --json，按 Gate 选择 intake/scope/build、boundary/slice、engineering/release digest lane，再追加决策草案并在受保护审批面签名。"
