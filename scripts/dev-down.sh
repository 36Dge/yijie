#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

compose_file="../yijie-infra/docker-compose.local.yml"

if [ -f "$compose_file" ]; then
  docker compose -f "$compose_file" down
else
  echo "Local dependency compose file not found: $compose_file"
  exit 1
fi
