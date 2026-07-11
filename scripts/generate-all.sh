#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

while IFS=$'\t' read -r name repo_path _url _branch; do
  if [ ! -d "$repo_path/.git" ] || [ ! -f "$repo_path/Makefile" ]; then
    echo "Repository is not available: $name ($repo_path)" >&2
    exit 1
  fi
  if make -C "$repo_path" -n generate >/dev/null 2>&1; then
    echo "generate: $name"
    make -C "$repo_path" generate
  else
    echo "no generated artifacts: $name"
  fi
done < <(node scripts/repo-manifest.mjs list)
