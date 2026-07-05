#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

echo "Checking repository mount points from repos.yaml..."

awk '/path: / { print $2 }' repos.yaml | while read -r repo_path; do
  sibling_path="../$(basename "$repo_path")"
  if [ -d "$repo_path/.git" ]; then
    echo "OK: $repo_path"
  elif [ -d "$sibling_path/.git" ]; then
    echo "SIBLING: $sibling_path"
  elif [ -d "$repo_path" ]; then
    echo "PLACEHOLDER: $repo_path exists but is not a checked-out repository"
  else
    echo "MISSING: $repo_path"
  fi
done

echo "Repository remotes are not configured yet. Add submodules or clone repos into the paths above."
