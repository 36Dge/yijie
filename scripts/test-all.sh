#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

while IFS=$'\t' read -r name repo_path _url _branch; do
  if [ ! -d "$repo_path/.git" ] || [ ! -f "$repo_path/Makefile" ]; then
    echo "Repository is not testable: $name ($repo_path)" >&2
    exit 1
  fi
  echo "test: $name"
  make -C "$repo_path" test
done < <(node scripts/repo-manifest.mjs list)
