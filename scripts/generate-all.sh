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
    if make -C "$actual_path" -n generate >/dev/null 2>&1; then
      echo "generate: $actual_path"
      make -C "$actual_path" generate
    else
      echo "skip generate: $actual_path"
    fi
  else
    echo "skip generate: $actual_path"
  fi
done
