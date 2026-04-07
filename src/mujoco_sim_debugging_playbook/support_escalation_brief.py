from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_support_escalation_brief(
    *,
    support_triage_reply_path: str | Path,
    support_session_note_path: str | Path,
    release_blockers_path: str | Path,
    output_dir: str | Path,
) -> dict:
    triage = _read_json(support_triage_reply_path)
    session = _read_json(support_session_note_path)
    blockers = _read_json(release_blockers_path)
    status = "escalate" if blockers["summary"]["blocker_count"] > 0 else "monitor"
    payload = {
        "summary": {
            "status": status,
            "blocker_count": blockers["summary"]["blocker_count"],
            "reply_status": triage["summary"]["status"],
            "session_status": session["summary"]["status"],
        },
        "handoff_note": session["next_step"],
    }
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "support_escalation_brief.json").write_text(json.dumps(payload, indent=2))
    (out / "support_escalation_brief.md").write_text(
        "# Support Escalation Brief\n\n"
        f"- Status: `{payload['summary']['status']}`\n"
        f"- Blockers: `{payload['summary']['blocker_count']}`\n"
        f"- Reply status: `{payload['summary']['reply_status']}`\n"
        f"- Session status: `{payload['summary']['session_status']}`\n"
        f"- Handoff note: {payload['handoff_note']}\n"
    )
    return payload
