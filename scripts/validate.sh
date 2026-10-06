#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

for script in .devcontainer/post-create.sh .devcontainer/post-start.sh scripts/demo scripts/demo-smoke scripts/lab scripts/validate.sh task/node/entrypoint.sh; do
  bash -n "$script"
done

if command -v helm >/dev/null 2>&1; then
  helm lint .cms-labs/chart \
    --set-file demo.catalog=demo-labs.json \
    --set-string jwt.privateKey=validation-private-key \
    --set-string jwt.publicKey=validation-public-key
  helm template cms-labs-dev .cms-labs/chart \
    --namespace cms-labs-system \
    --set-file demo.catalog=demo-labs.json \
    --set-string jwt.privateKey=validation-private-key \
    --set-string jwt.publicKey=validation-public-key >/dev/null
fi
