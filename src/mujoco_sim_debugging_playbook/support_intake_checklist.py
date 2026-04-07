from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_support_intake_checklist(*, issue_template_audit_path: str | Path, response_rubric_path: str | Path, output_dir: str | Path) -> dict:
    audit = _read_json(issue_template_audit_path)
    rubric = _read_json(response_rubric_path)
    items = [
        {"name": "issue_templates_present", "status": "pass" if audit["summary"]["template_count"] >= 2 else "warn"},
        {"name": "template_descriptions_present", "status": "pass" if audit["summary"]["described_count"] >= 1 else "warn"},
        {"name": "response_criteria_available", "status": "pass" if rubric["summary"]["criterion_count"] >= 3 else "warn"},
    ]
    payload = {"summary": {"item_count": len(items)}, "items": items}
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    (out / "support_intake_checklist.json").write_text(json.dumps(payload, indent=2))
    (out / "support_intake_checklist.md").write_text("# Support Intake Checklist\n\n" + "\n".join(f"- `{i['name']}`: `{i['status']}`" for i in items))
    return payload
