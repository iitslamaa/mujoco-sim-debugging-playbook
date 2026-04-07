from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_bundle_coverage(
    *,
    bundle_quality_path: str | Path,
    repro_bundle_index_path: str | Path,
    output_dir: str | Path,
) -> dict:
    quality = _read_json(bundle_quality_path)
    repro_index = _read_json(repro_bundle_index_path)
    entry_count = repro_index["summary"]["entry_count"]
    status = "pass" if quality["summary"]["status"] == "pass" and entry_count > 0 else "warn"
    payload = {
        "summary": {
            "status": status,
            "entry_count": entry_count,
            "high_value_file_count": quality["summary"]["evidence_hit_count"],
        },
        "covered_cases": [entry["case_id"] for entry in repro_index["entries"]],
    }
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "bundle_coverage.json").write_text(json.dumps(payload, indent=2))
    (out / "bundle_coverage.md").write_text(
        "# Bundle Coverage\n\n"
        f"- Status: `{payload['summary']['status']}`\n"
        f"- Covered cases: `{payload['summary']['entry_count']}`\n"
        f"- High-value files: `{payload['summary']['high_value_file_count']}`\n"
    )
    return payload
