#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

python3 tests/validate_repository.py

for script in .devcontainer/post-create.sh .devcontainer/post-start.sh scripts/demo scripts/demo-smoke scripts/lab scripts/validate.sh task/node/entrypoint.sh; do
  bash -n "$script"
done
