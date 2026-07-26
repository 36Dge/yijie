#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  ./scripts/new-feature.sh FEATURE_ID FEATURE_SLUG [OUTPUT_ROOT]

Example:
  ./scripts/new-feature.sh FEAT-123 task-history-export ./work

OUTPUT_ROOT defaults to "$PWD/features".
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ "$#" -lt 2 || "$#" -gt 3 ]]; then
  usage >&2
  exit 2
fi

feature_id="$1"
feature_slug="$2"
output_root="${3:-$PWD/features}"

if [[ ! "$feature_id" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "ERROR: FEATURE_ID 只能包含字母、数字、点、下划线和连字符。" >&2
  exit 2
fi

if [[ ! "$feature_slug" =~ ^[a-z0-9][a-z0-9._-]*$ ]]; then
  echo "ERROR: FEATURE_SLUG 必须以小写字母或数字开头，且只能包含小写字母、数字、点、下划线和连字符。" >&2
  exit 2
fi

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
template_dir="$script_dir/../templates/feature-package"
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
    "$file" > "$temp_file"
  mv "$temp_file" "$file"
done < <(find "$target_dir" -type f -print0)

echo "Created feature package:"
echo "  $target_dir"
echo
echo "Next:"
echo "  1. 先完成 00—07 文档并通过 G2。"
echo "  2. 执行：$script_dir/check-feature-package.sh --gate G2 \"$target_dir\""
echo "  3. G2 通过后，契约变更先完成 Gate 2A，再开始下游业务代码实现。"
