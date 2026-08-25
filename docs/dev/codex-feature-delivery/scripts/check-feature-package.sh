#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  ./scripts/check-feature-package.sh [--strict] [--gate D0|D4|DP|G0|G1|G2|G2A|G2V|G3|G4|G5|G6] [--slice SLICE_ID] FEATURE_DIR

Checks:
  default       Required files exist and template placeholders were replaced.
  --strict      Also rejects TBD, TODO, 待补充 and 待确认 in all documents.
  --gate Dx/Gx  Validates the selected demo_fast or production_hardened checkpoint.
  --slice ID    Required for schema v2 G3; validates exactly one per-slice gate.

This script checks document structure and incomplete markers. It does not replace
human approval, CI, security review, compatibility checks, or production evidence.
USAGE
}

strict=0
gate=""
slice_id=""
feature_dir=""

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --strict)
      strict=1
      shift
      ;;
    --gate)
      if [[ "$#" -lt 2 ]]; then
        echo "ERROR: --gate 缺少值。" >&2
        usage >&2
        exit 2
      fi
      gate="$2"
      shift 2
      ;;
    --slice)
      if [[ "$#" -lt 2 ]]; then
        echo "ERROR: --slice 缺少值。" >&2
        usage >&2
        exit 2
      fi
      slice_id="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "ERROR: 未知参数：$1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [[ -n "$feature_dir" ]]; then
        echo "ERROR: 只能指定一个 FEATURE_DIR。" >&2
        usage >&2
        exit 2
      fi
      feature_dir="$1"
      shift
      ;;
  esac
done

if [[ -z "$feature_dir" ]]; then
  usage >&2
  exit 2
fi

case "$gate" in
  ""|D0|D4|DP|G0|G1|G2|G2A|G2V|G3|G4|G5|G6) ;;
  *)
    echo "ERROR: gate 必须是 D0、D4、DP、G0、G1、G2、G2A、G2V、G3、G4、G5 或 G6。" >&2
    exit 2
    ;;
esac

if [[ -n "$slice_id" && "$gate" != "G3" ]]; then
  echo "ERROR: --slice 只能与 --gate G3 一起使用。" >&2
  exit 2
fi

if [[ ! -d "$feature_dir" ]]; then
  echo "ERROR: 目录不存在：$feature_dir" >&2
  exit 1
fi

schema_version="$(sed -nE 's/^[[:space:]]*"?schema_version"?[[:space:]]*:[[:space:]]*([0-9]+),?([[:space:]]*#.*)?[[:space:]]*$/\1/p' "$feature_dir/feature.yaml" 2>/dev/null || true)"
delivery_profile="$(sed -nE 's/^[[:space:]]*"?delivery_profile"?[[:space:]]*:[[:space:]]*"?([a-z_]+)"?,?([[:space:]]*#.*)?[[:space:]]*$/\1/p' "$feature_dir/feature.yaml" 2>/dev/null || true)"
if [[ "$schema_version" == "3" && "$delivery_profile" == "demo_fast" ]]; then
  required_files=(
    "feature.yaml"
    "00-feature-brief.md"
    "01-delivery-log.md"
    "02-verification.md"
  )
else
  required_files=(
    "feature.yaml"
    "00-feature-brief.md"
    "01-requirements.md"
    "02-impact-assessment.md"
    "03-decisions-and-risks.md"
    "04-contract-change-plan.md"
    "05-technical-design.md"
    "06-test-plan.md"
    "07-implementation-plan.md"
    "08-verification-report.md"
    "09-release-and-rollback.md"
    "10-delivery-summary.md"
  )
  if [[ "$schema_version" == "2" || "$schema_version" == "3" ]]; then
    required_files+=("04A-temporal-contract-matrix.md")
  fi
fi

if [[ "$delivery_profile" == "demo_fast" && "$gate" == G* ]]; then
  echo "ERROR: demo_fast 只能使用 D0、D4 或 DP。" >&2
  exit 2
fi
if [[ "$delivery_profile" != "demo_fast" && "$gate" == D* ]]; then
  echo "ERROR: D0、D4、DP 只适用于 schema v3 demo_fast。" >&2
  exit 2
fi

errors=0
all_paths=()

for relative_path in "${required_files[@]}"; do
  full_path="$feature_dir/$relative_path"
  all_paths+=("$full_path")
  if [[ ! -f "$full_path" ]]; then
    echo "MISSING: $relative_path" >&2
    errors=$((errors + 1))
  elif [[ ! -s "$full_path" ]]; then
    echo "EMPTY: $relative_path" >&2
    errors=$((errors + 1))
  fi
done

if [[ "$errors" -gt 0 ]]; then
  echo "FAIL: 缺少或存在空文件，共 $errors 项。" >&2
  exit 1
fi

placeholder_output="$(grep -HnE '\{\{FEATURE_ID\}\}|\{\{FEATURE_SLUG\}\}|\{\{DATE\}\}|\{\{DELIVERY_PROFILE\}\}|\{\{EXPOSURE\}\}|\{\{PUBLIC_REQUIRED\}\}|\{\{PUBLIC_STATUS\}\}' "${all_paths[@]}" || true)"
if [[ -n "$placeholder_output" ]]; then
  echo "FAIL: 仍有未替换的模板变量：" >&2
  echo "$placeholder_output" >&2
  exit 1
fi

scope_files=()
add_scope_file() {
  scope_files+=("$feature_dir/$1")
}

if [[ -n "$gate" && "$delivery_profile" == "demo_fast" ]]; then
  case "$gate" in
    D0)
      add_scope_file "00-feature-brief.md"
      ;;
    D4|DP)
      add_scope_file "00-feature-brief.md"
      add_scope_file "01-delivery-log.md"
      add_scope_file "02-verification.md"
      ;;
  esac
elif [[ -n "$gate" ]]; then
  # schema v2 的 feature.yaml 由 gate-aware semantic validator 负责。不得因未来
  # slice/G4 字段仍为 TBD 而阻断较早 Gate；schema v1 保留原 marker 行为。
  if [[ "$schema_version" != "2" && "$schema_version" != "3" ]]; then
    add_scope_file "feature.yaml"
  fi
  add_scope_file "00-feature-brief.md"

  case "$gate" in
    G1|G2|G2A|G2V|G3|G4|G5|G6)
      add_scope_file "01-requirements.md"
      add_scope_file "02-impact-assessment.md"
      add_scope_file "03-decisions-and-risks.md"
      ;;
  esac

  case "$gate" in
    G2|G2A|G2V|G3|G4|G5|G6)
      add_scope_file "04-contract-change-plan.md"
      if [[ "$schema_version" == "2" || "$schema_version" == "3" ]]; then
        add_scope_file "04A-temporal-contract-matrix.md"
      fi
      add_scope_file "05-technical-design.md"
      add_scope_file "06-test-plan.md"
      add_scope_file "07-implementation-plan.md"
      ;;
  esac

  case "$gate" in
    G4|G5|G6)
      add_scope_file "08-verification-report.md"
      ;;
  esac

  if [[ "$gate" == "G3" && "$schema_version" != "2" && "$schema_version" != "3" ]]; then
    add_scope_file "08-verification-report.md"
  fi

  case "$gate" in
    G5|G6)
      add_scope_file "09-release-and-rollback.md"
      ;;
  esac

  if [[ "$gate" == "G6" ]]; then
    add_scope_file "10-delivery-summary.md"
  fi
elif [[ "$strict" -eq 1 ]]; then
  scope_files=("${all_paths[@]}")
fi

if [[ "${#scope_files[@]}" -gt 0 ]]; then
  incomplete_output="$(grep -HnE '(^|[^A-Za-z])(TBD|TODO)([^A-Za-z]|$)|待补充|待确认' "${scope_files[@]}" || true)"
  if [[ -n "$incomplete_output" ]]; then
    echo "FAIL: 检查范围仍有未完成标记：" >&2
    echo "$incomplete_output" >&2
    exit 1
  fi
fi

validator_args=()
if [[ -n "$gate" ]]; then
  validator_args+=(--gate "$gate")
fi
if [[ -n "$slice_id" ]]; then
  validator_args+=(--slice "$slice_id")
fi
validator_args+=("$feature_dir")
node "$(dirname -- "$0")/validate-feature-package.mjs" "${validator_args[@]}"

if [[ -n "$gate" ]]; then
  if [[ -n "$slice_id" ]]; then
    echo "PASS: 文档结构完整，且 $gate/$slice_id 范围与语义门禁通过。"
  else
    echo "PASS: 文档结构完整，且 $gate 范围与语义门禁通过。"
  fi
elif [[ "$strict" -eq 1 ]]; then
  echo "PASS: 文档结构完整，所有模板变量和未完成标记已处理。"
else
  echo "PASS: 文档结构完整，模板变量已替换。"
fi

if [[ "$delivery_profile" == "demo_fast" ]]; then
  echo "NOTE: demo_fast 只证明声明的真实本地/公开 Demo 检查；不等于 production_hardened。"
else
  echo "NOTE: 此结果不证明未声明的代码、测试、安全、兼容或生产门禁已经通过。"
fi
