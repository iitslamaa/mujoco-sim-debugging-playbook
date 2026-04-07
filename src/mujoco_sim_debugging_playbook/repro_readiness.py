from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_repro_readiness(
    *,
    repro_bundle_index_path: str | Path,
    support_intake_checklist_path: str | Path,
    output_dir: str | Path,
) -> dict:
    repro = _read_json(repro_bundle_index_path)
    intake = _read_json(support_intake_checklist_path)
    ready_items = sum(1 for item in intake["items"] if item["status"] == "pass")
    status = "ready" if repro["summary"]["entry_count"] > 0 and ready_items == len(intake["items"]) else "partial"
    payload = {
        "summary": {
            "status": status,
            "entry_count": repro["summary"]["entry_count"],
            "intake_items_ready": ready_items,
        },
        "covered_cases": [entry["case_id"] for entry in repro["entries"]],
    }
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "repro_readiness.json").write_text(json.dumps(payload, indent=2))
    (out / "repro_readiness.md").write_text(
        "# Repro Readiness\n\n"
        f"- Status: `{payload['summary']['status']}`\n"
        f"- Covered cases: `{payload['summary']['entry_count']}`\n"
        f"- Intake items ready: `{payload['summary']['intake_items_ready']}`\n"
    )
    return payload
