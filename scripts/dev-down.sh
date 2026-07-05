#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

compose_file="platform/yijie-infra/docker-compose.local.yml"
sibling_compose_file="../yijie-infra/docker-compose.local.yml"

if [ -f "$compose_file" ]; then
  docker compose -f "$compose_file" down
elif [ -f "$sibling_compose_file" ]; then
  docker compose -f "$sibling_compose_file" down
else
  echo "Local dependency compose file not found: $compose_file"
  echo "Sibling compose file not found: $sibling_compose_file"
fi
