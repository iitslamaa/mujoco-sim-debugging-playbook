from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_support_session_note(
    *,
    intake_path: str | Path,
    repro_inventory_path: str | Path,
    response_rubric_path: str | Path,
    output_dir: str | Path,
) -> dict:
    intake = _read_json(intake_path)
    repro = _read_json(repro_inventory_path)
    rubric = _read_json(response_rubric_path)
    required_items = sum(1 for item in intake["items"] if item["status"] == "pass")
    required_criteria = sum(1 for item in rubric["criteria"] if item["status"] == "required")
    payload = {
        "summary": {
            "status": "pass" if required_items >= 3 and repro["summary"]["case_count"] >= 1 else "warn",
            "intake_items_ready": required_items,
            "repro_case_count": repro["summary"]["case_count"],
            "required_response_criteria": required_criteria,
        },
        "next_step": "Start from the highest-signal repro case and attach a clear reproduction command.",
    }

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "support_session_note.json").write_text(json.dumps(payload, indent=2))
    (out / "support_session_note.md").write_text(
        "# Support Session Note\n\n"
        f"- Status: `{payload['summary']['status']}`\n"
        f"- Intake items ready: `{payload['summary']['intake_items_ready']}`\n"
        f"- Repro cases: `{payload['summary']['repro_case_count']}`\n"
        f"- Required response criteria: `{payload['summary']['required_response_criteria']}`\n"
        f"- Next step: {payload['next_step']}\n"
    )
    return payload
