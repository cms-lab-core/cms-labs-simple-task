from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "task"


required = [
    ROOT / "README.md",
    ROOT / "description.md",
    ROOT / "catalog.json",
    ROOT / ".devcontainer" / "devcontainer.json",
    ROOT / "scripts" / "lab",
    ROOT / "scripts" / "demo",
    ROOT / "scripts" / "demo-smoke",
    ROOT / ".cms-labs" / "kind.yaml",
    ROOT / ".cms-labs" / "base.yaml",
    ROOT / ".cms-labs" / "seed.yaml",
    ROOT / ".cms-labs" / "app.yaml",
    LAB / "README.md",
    LAB / "task.ipynb",
    LAB / "lab.json",
    LAB / "topology.clab",
    LAB / "topology.template.yaml",
    LAB / "terminal.template.yaml",
    LAB / "node" / "Dockerfile",
    LAB / "node" / "lab_agent.py",
]
missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
assert not missing, f"missing required files: {', '.join(missing)}"

assert not list((ROOT / "modules").glob("**/.git")), "modules must not contain nested Git repositories"

readme = (ROOT / "README.md").read_text(encoding="utf-8")
assert "https://codespaces.new/cms-lab-core/cms-labs-simple-task?quickstart=1" in readme
assert "task/task.ipynb" in readme.lower()

catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
assert catalog["kind"] == "LabCatalog"
assert catalog["metadata"]["name"] == "cms-labs-simple-task"
assert catalog["spec"]["types"]["subject"] == ["network-lab"]
assert catalog["spec"]["types"]["interface"] == ["jupyter-notebook"]
catalog_lab = catalog["spec"]["labs"][0]
assert catalog_lab["id"] == "task"
assert catalog_lab["metadataPath"] == "task/lab.json"

devcontainer = json.loads((ROOT / ".devcontainer" / "devcontainer.json").read_text(encoding="utf-8"))
assert devcontainer["image"] == "ghcr.io/srl-labs/containerlab/devcontainer-dind-slim:latest"
assert 18080 in devcontainer["forwardPorts"]
assert devcontainer["postCreateCommand"] == "bash .devcontainer/post-create.sh"

metadata = json.loads((LAB / "lab.json").read_text(encoding="utf-8"))
assert metadata["spec"]["labPath"] == "task/task.ipynb"
assert metadata["spec"]["testPath"] == "sdn_lab_5"
assert metadata["spec"]["topologyPath"] == "task/topology.template.yaml"
assert metadata["spec"]["types"]["subject"] == "network-lab"
assert metadata["spec"]["types"]["assessment"] == "automatic-checker"
assert "github-codespaces" in metadata["spec"]["execution"]
assert metadata["spec"]["runtime"]["jupyterImage"] == "ghcr.io/cms-lab-core/cms-labs-jupyter:latest"
assert metadata["spec"]["runtime"]["checkerImage"] == "ghcr.io/cms-lab-core/cms-labs-checker:latest"
assert metadata["spec"]["runtime"]["nodeImage"] == "ghcr.io/cms-lab-core/cms-labs-simple-task-node:latest"

app_manifest = (ROOT / ".cms-labs" / "app.yaml").read_text(encoding="utf-8")
seed_manifest = (ROOT / ".cms-labs" / "seed.yaml").read_text(encoding="utf-8")
for component in ["backend", "clabgate", "frontend"]:
    assert f"ghcr.io/cms-lab-core/cms-labs-api/{component}:latest" in app_manifest
assert "CMS_TASK_BRANCH, value: main" in app_manifest
assert "ghcr.io/cms-lab-core/cms-labs-jupyter:latest" in app_manifest
assert "ghcr.io/cms-lab-core/cms-labs-checker:latest" in app_manifest
assert "ghcr.io/cms-lab-core/cms-labs-api/backend:latest" in seed_manifest

topology = (LAB / "topology.clab").read_text(encoding="utf-8")
template = (LAB / "topology.template.yaml").read_text(encoding="utf-8")
terminal_template = (LAB / "terminal.template.yaml").read_text(encoding="utf-8")
for document in [topology, template]:
    assert "r1:" in document and "s1:" in document
    assert "r1:eth1" in document and "s1:eth1" in document
assert topology.count("image: ${SDN_LAB_NODE_IMAGE}") == 2
assert template.count("cms-labs-simple-task-node:latest") == 2
assert "name: $NAME" in template and "namespace: $NAME" in template
assert "apiVersion: c9s.run/v1alpha1" in template
assert "ttyd-shell" not in template
assert "ghcr.io/cms-lab-core/cms-labs-terminal:latest" in terminal_template
assert "command: [/bin/ash, -l]" in terminal_template
assert "name: r1" in terminal_template and "port: 7681" in terminal_template
assert "name: s1" in terminal_template and "port: 7682" in terminal_template
assert "$WORKSPACE_PROXY_NAMESPACE" in terminal_template
for kind in ["ServiceAccount", "Role", "RoleBinding", "ConfigMap", "Deployment", "Service", "NetworkPolicy"]:
    assert f"kind: {kind}" in terminal_template
lab_launcher = (ROOT / "scripts" / "lab").read_text(encoding="utf-8")
assert "cms-labs-simple-task-node:latest" in lab_launcher
assert "export SDN_LAB_NODE_IMAGE=$node_image" in lab_launcher
demo_launcher = (ROOT / "scripts" / "demo").read_text(encoding="utf-8")
assert "oci://ghcr.io/srl-labs/clabernetes/clabernetes" in demo_launcher
assert "launcherImage" not in demo_launcher
assert "clabernetes-launcher:dev-latest" not in demo_launcher
assert "clabernetes_version=0.8.0" in demo_launcher
assert "CMS_LABS_FRONTEND_PORT" in demo_launcher
node_dockerfile = (LAB / "node" / "Dockerfile").read_text(encoding="utf-8")
assert "FROM alpine:3.24.2" in node_dockerfile
assert "FROM alpine:latest" not in node_dockerfile
yaml_files = sorted(path.name for path in LAB.rglob("*") if path.suffix.lower() in {".yaml", ".yml"})
assert yaml_files == ["terminal.template.yaml", "topology.template.yaml"], (
    f"Clabgate would apply unexpected YAML files: {yaml_files}"
)

notebook = json.loads((LAB / "task.ipynb").read_text(encoding="utf-8"))
assert notebook["nbformat"] == 4
assert any("Пример задания" in "".join(cell["source"]) for cell in notebook["cells"])
for index, cell in enumerate(notebook["cells"]):
    if cell["cell_type"] == "code":
        ast.parse("".join(cell["source"]), filename=f"task.ipynb:cell-{index}")

ast.parse((LAB / "node" / "lab_agent.py").read_text(encoding="utf-8"), filename="lab_agent.py")

print(f"validated {len(required)} required files and {len(notebook['cells'])} notebook cells")
