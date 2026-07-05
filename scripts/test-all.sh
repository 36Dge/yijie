#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

awk '/path: / { print $2 }' repos.yaml | while read -r repo_path; do
  sibling_path="../$(basename "$repo_path")"
  actual_path="$repo_path"
  if [ ! -d "$actual_path/.git" ] && [ -d "$sibling_path/.git" ]; then
    actual_path="$sibling_path"
  fi

  if [ -f "$actual_path/Makefile" ]; then
    echo "test: $actual_path"
    make -C "$actual_path" test
  elif [ -f "$actual_path/package.json" ] && command -v pnpm >/dev/null 2>&1; then
    echo "test: $actual_path"
    (cd "$actual_path" && pnpm test)
  else
    echo "skip test: $actual_path"
  fi
done
