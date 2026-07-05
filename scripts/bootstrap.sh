#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

echo "Bootstrapping yijie-workspace..."

required=(git)
optional=(go node pnpm rustc cargo docker make)

for cmd in "${required[@]}"; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    exit 1
  fi
done

for cmd in "${optional[@]}"; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Optional command not found: $cmd"
  fi
done

echo "Workspace root: $root"
echo "Next: add repository remotes or submodules, then run ./scripts/checkout-all.sh"
