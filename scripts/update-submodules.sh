#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

if git config --file .gitmodules --get-regexp path >/dev/null 2>&1; then
  git submodule update --init --recursive
else
  echo "No submodules configured yet."
fi
