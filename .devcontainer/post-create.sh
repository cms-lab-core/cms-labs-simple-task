#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

./scripts/validate.sh
./scripts/demo up

printf '\nCMS Labs environment is ready.\n'
./scripts/demo open
