#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT_DIR="${ROOT_DIR}/outputs/debug_bundle/${STAMP}"

mkdir -p "${OUT_DIR}"

copy_if_exists() {
  local src="$1"
  local dest_name="$2"
  if [[ -e "${src}" ]]; then
    cp -R "${src}" "${OUT_DIR}/${dest_name}"
    echo "[bundle] copied ${src}"
  else
    echo "[bundle] skipped missing ${src}"
  fi
}

echo "[bundle] writing to ${OUT_DIR}"

copy_if_exists "${ROOT_DIR}/outputs/diagnostics/diagnostics.md" "diagnostics.md"
copy_if_exists "${ROOT_DIR}/outputs/diagnostics/environment.json" "environment.json"
copy_if_exists "${ROOT_DIR}/outputs/environment_doctor/doctor.md" "environment_doctor.md"
copy_if_exists "${ROOT_DIR}/outputs/support_cases" "support_cases"
copy_if_exists "${ROOT_DIR}/outputs/baseline/summary.json" "baseline_summary.json"
copy_if_exists "${ROOT_DIR}/outputs/controller_benchmark/benchmark_summary.json" "benchmark_summary.json"
copy_if_exists "${ROOT_DIR}/outputs/domain_randomization/evaluation_rows.json" "domain_randomization_rows.json"
copy_if_exists "${ROOT_DIR}/dashboard/data.json" "dashboard_data.json"

cat > "${OUT_DIR}/README.md" <<EOF
# Debug Bundle

- Created: ${STAMP}
- Repo root: ${ROOT_DIR}
- Included: diagnostics, environment, support cases, benchmark summaries, dashboard data

Use this bundle when handing a reproduction off to another engineer or attaching evidence to an issue.
EOF

echo "[bundle] done"
