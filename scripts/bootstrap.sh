#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

required=(git node pnpm go rustc cargo make)
for cmd in "${required[@]}"; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    exit 1
  fi
done

echo "Installing workspace tooling..."
pnpm install --frozen-lockfile

echo "Checking out child repositories..."
./scripts/checkout-all.sh

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required for local infrastructure but is not installed." >&2
  echo "Repository checkout is complete; install Docker before running make dev-up." >&2
fi

echo "Workspace bootstrap complete: $root"
