#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

echo "Checking workspace shell syntax..."
bash -n scripts/*.sh

while IFS=$'\t' read -r name repo_path _url _branch; do
  if [ ! -d "$repo_path/.git" ]; then
    echo "Missing repository: $name ($repo_path)" >&2
    exit 1
  fi
  if [ ! -f "$repo_path/Makefile" ]; then
    echo "Missing Makefile: $name" >&2
    exit 1
  fi
  echo "lint: $name"
  make -C "$repo_path" lint
done < <(node scripts/repo-manifest.mjs list)
