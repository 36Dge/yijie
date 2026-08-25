#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  ./scripts/new-feature.sh [--profile demo_fast|production_hardened] [--exposure local|public] FEATURE_ID FEATURE_SLUG [OUTPUT_ROOT]

Example:
  ./scripts/new-feature.sh FEAT-123 task-history-export ./work
  ./scripts/new-feature.sh --profile production_hardened --exposure public FEAT-124 billing-export ./work

OUTPUT_ROOT defaults to "$PWD/features".
New features default to profile demo_fast with local exposure.
USAGE
}

profile="demo_fast"
exposure="local"
positionals=()
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --profile)
      [[ "$#" -ge 2 ]] || { echo "ERROR: --profile 缺少值。" >&2; exit 2; }
      profile="$2"
      shift 2
      ;;
    --exposure)
      [[ "$#" -ge 2 ]] || { echo "ERROR: --exposure 缺少值。" >&2; exit 2; }
      exposure="$2"
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
      positionals+=("$1")
      shift
      ;;
  esac
done

if [[ "${#positionals[@]}" -lt 2 || "${#positionals[@]}" -gt 3 ]]; then
  usage >&2
  exit 2
fi

case "$profile" in
  demo_fast|production_hardened) ;;
  *) echo "ERROR: --profile 必须是 demo_fast 或 production_hardened。" >&2; exit 2 ;;
esac
case "$exposure" in
  local|public) ;;
  *) echo "ERROR: --exposure 必须是 local 或 public。" >&2; exit 2 ;;
esac

feature_id="${positionals[0]}"
feature_slug="${positionals[1]}"
output_root="${positionals[2]:-$PWD/features}"

if [[ ! "$feature_id" =~ ^FEAT-[0-9]+$ ]]; then
  echo "ERROR: FEATURE_ID 必须匹配 FEAT-<数字>。" >&2
  exit 2
fi

if [[ ! "$feature_slug" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "ERROR: FEATURE_SLUG 必须是小写 kebab-case。" >&2
  exit 2
fi

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if [[ "$profile" == "demo_fast" ]]; then
  template_dir="$script_dir/../templates/demo-fast-feature-package"
else
  template_dir="$script_dir/../templates/feature-package"
fi
if [[ "$exposure" == "public" ]]; then
  public_required="true"
  public_status="pending"
else
  public_required="false"
  public_status="not_applicable"
fi
target_dir="$output_root/$feature_id-$feature_slug"
today="$(date +%Y-%m-%d)"

if [[ ! -d "$template_dir" ]]; then
  echo "ERROR: 找不到模板目录：$template_dir" >&2
  exit 1
fi

if [[ -e "$target_dir" ]]; then
  echo "ERROR: 目标已存在，不会覆盖：$target_dir" >&2
  exit 1
fi

mkdir -p "$output_root"
mkdir "$target_dir"
cp -R "$template_dir"/. "$target_dir"/

while IFS= read -r -d '' file; do
  temp_file="${file}.tmp.$$"
  sed \
    -e "s/{{FEATURE_ID}}/$feature_id/g" \
    -e "s/{{FEATURE_SLUG}}/$feature_slug/g" \
    -e "s/{{DATE}}/$today/g" \
    -e "s/{{DELIVERY_PROFILE}}/$profile/g" \
    -e "s/{{EXPOSURE}}/$exposure/g" \
    -e "s/{{PUBLIC_REQUIRED}}/$public_required/g" \
    -e "s/{{PUBLIC_STATUS}}/$public_status/g" \
    "$file" > "$temp_file"
  mv "$temp_file" "$file"
done < <(find "$target_dir" -type f -print0)

echo "Created feature package:"
echo "  $target_dir"
echo "  profile=$profile exposure=$exposure schema=v3"
echo
echo "Next:"
if [[ "$profile" == "demo_fast" ]]; then
  echo "  1. 一次补全产品逻辑、交互、UI 状态和 Must AC。"
  echo "  2. 执行：$script_dir/check-feature-package.sh --gate D0 \"$target_dir\""
  echo "  3. 整体实现后启动真实服务，修复 Bug 直到一次 fresh run 通过。"
  echo "  4. 执行：$script_dir/check-feature-package.sh --gate D4 \"$target_dir\""
  if [[ "$exposure" == "public" ]]; then
    echo "  5. 对外公开前执行：$script_dir/check-feature-package.sh --gate DP \"$target_dir\""
  fi
else
  echo "  1. 先完成 00—07 文档并通过 G2。"
  echo "  2. 执行：$script_dir/check-feature-package.sh --gate G2 \"$target_dir\""
  echo "  3. 按 G2A → Harness Qualification → G2V → per-slice G3 → G4 → G5 → G6 推进。"
fi
