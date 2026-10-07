#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

for script in .devcontainer/post-create.sh .devcontainer/post-start.sh scripts/demo scripts/demo-smoke scripts/lab scripts/validate.sh task/node/entrypoint.sh; do
  bash -n "$script"
done

if command -v helm >/dev/null 2>&1; then
  chart=${CMS_LABS_API_CHART:-oci://ghcr.io/cms-lab-core/cms-labs-api/charts/universal-chart}
  chart_version=${CMS_LABS_API_CHART_VERSION:-^1.0.0}
  if test -d ../cms-labs-urfu/k8s/base-chart && test -z "${CMS_LABS_API_CHART:-}"; then
    chart=../cms-labs-urfu/k8s/base-chart
  fi
  helm_command=(helm template cms-labs-dev "$chart")
  if [[ "$chart" = oci://* ]]; then
    helm_command+=(--version "$chart_version")
  fi
  "${helm_command[@]}" \
    --namespace cms-labs-system \
    --values .cms-labs/cms-labs-values.yaml \
    --set-file 'configMaps.cms-demo-catalog.data.catalog\.json=demo-labs.json' \
    --set-string 'secrets.cms-demo-jwt.data.private\.pem=validation-private-key' \
    --set-string 'secrets.cms-demo-jwt.data.public\.pem=validation-public-key' >/dev/null
fi
