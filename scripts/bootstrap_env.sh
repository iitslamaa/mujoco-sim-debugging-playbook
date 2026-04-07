#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

echo "[bootstrap] repo: ${ROOT_DIR}"

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "[bootstrap] creating virtual environment at ${VENV_DIR}"
  python3 -m venv "${VENV_DIR}"
else
  echo "[bootstrap] reusing existing virtual environment at ${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"

echo "[bootstrap] upgrading packaging tools"
python -m pip install --upgrade pip setuptools wheel

echo "[bootstrap] installing project dependencies"
python -m pip install -e . --no-build-isolation

echo "[bootstrap] installed versions"
python - <<'PY'
import importlib

for module_name in ("numpy", "mujoco", "torch"):
    module = importlib.import_module(module_name)
    print(f"{module_name}={module.__version__}")
PY

echo "[bootstrap] done"
