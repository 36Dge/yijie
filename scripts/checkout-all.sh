#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

node scripts/repo-manifest.mjs validate

while IFS=$'\t' read -r name repo_path url branch; do
  if [ ! -e "$repo_path" ]; then
    echo "Cloning $name into $repo_path..."
    git clone --branch "$branch" "$url" "$repo_path"
    continue
  fi

  if [ ! -d "$repo_path/.git" ]; then
    echo "Cannot use $repo_path: path exists but is not a Git repository." >&2
    exit 1
  fi

  current_url="$(git -C "$repo_path" remote get-url origin 2>/dev/null || true)"
  if [ -z "$current_url" ]; then
    git -C "$repo_path" remote add origin "$url"
  elif [ "$current_url" != "$url" ]; then
    echo "$name has unexpected origin: $current_url" >&2
    echo "Expected: $url" >&2
    exit 1
  fi

  echo "Fetching $name..."
  git -C "$repo_path" fetch --prune origin
  if ! git -C "$repo_path" show-ref --verify --quiet "refs/heads/$branch"; then
    git -C "$repo_path" branch --track "$branch" "origin/$branch"
  fi
  echo "Ready: $name (current branch: $(git -C "$repo_path" branch --show-current))"
done < <(node scripts/repo-manifest.mjs list)

echo "All repositories are available. Existing working trees were not modified."
