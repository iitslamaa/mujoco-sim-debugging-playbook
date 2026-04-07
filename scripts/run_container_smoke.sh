#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

echo "[container-smoke] building image"
docker compose build sim-debug

echo "[container-smoke] running smoke test"
docker compose run --rm sim-debug python scripts/smoke_test.py

echo "[container-smoke] completed"
