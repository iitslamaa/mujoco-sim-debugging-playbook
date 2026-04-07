from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_support_triage_reply(
    *,
    support_response_template_path: str | Path,
    support_session_note_path: str | Path,
    support_intake_checklist_path: str | Path,
    output_dir: str | Path,
) -> dict:
    template = _read_json(support_response_template_path)
    session = _read_json(support_session_note_path)
    intake = _read_json(support_intake_checklist_path)
    ready_items = sum(1 for item in intake["items"] if item["status"] == "pass")
    payload = {
        "summary": {
            "status": "ready" if ready_items == len(intake["items"]) else "draft",
            "section_count": len(template["sections"]),
            "intake_items_ready": ready_items,
        },
        "reply": [
            "Thanks for the report. I was able to narrow this down to a reproducible path.",
            f"Current session status: {session['summary']['status']}.",
            f"Recommended next step: {session['next_step']}",
        ],
    }
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "support_triage_reply.json").write_text(json.dumps(payload, indent=2))
    (out / "support_triage_reply.md").write_text(
        "# Support Triage Reply\n\n"
        f"- Status: `{payload['summary']['status']}`\n"
        f"- Sections: `{payload['summary']['section_count']}`\n"
        f"- Intake items ready: `{payload['summary']['intake_items_ready']}`\n\n"
        + "\n".join(f"- {line}" for line in payload["reply"])
        + "\n"
    )
    return payload
