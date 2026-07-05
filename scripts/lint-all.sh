#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

echo "Checking shell syntax..."
bash -n scripts/*.sh

echo "Checking repository lint commands..."
awk '/path: / { print $2 }' repos.yaml | while read -r repo_path; do
  sibling_path="../$(basename "$repo_path")"
  actual_path="$repo_path"
  if [ ! -d "$actual_path/.git" ] && [ -d "$sibling_path/.git" ]; then
    actual_path="$sibling_path"
  fi

  if [ -f "$actual_path/Makefile" ]; then
    echo "lint: $actual_path"
    make -C "$actual_path" lint
  elif [ -f "$actual_path/package.json" ] && command -v pnpm >/dev/null 2>&1; then
    echo "lint: $actual_path"
    (cd "$actual_path" && pnpm lint)
  else
    echo "skip lint: $actual_path"
  fi
done
