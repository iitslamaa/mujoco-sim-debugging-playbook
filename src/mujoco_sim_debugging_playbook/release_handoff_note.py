from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_release_handoff_note(
    *,
    release_evidence_packet_path: str | Path,
    release_dry_run_path: str | Path,
    output_dir: str | Path,
) -> dict:
    packet = _read_json(release_evidence_packet_path)
    dry_run = _read_json(release_dry_run_path)
    payload = {
        "summary": {
            "status": dry_run["summary"]["status"],
            "blocker_count": packet["summary"]["blocker_count"],
            "matrix_row_count": packet["summary"]["matrix_row_count"],
        },
        "next_owner": "release-review",
        "note": dry_run["recommendation"],
    }
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "release_handoff_note.json").write_text(json.dumps(payload, indent=2))
    (out / "release_handoff_note.md").write_text(
        "# Release Handoff Note\n\n"
        f"- Status: `{payload['summary']['status']}`\n"
        f"- Blockers: `{payload['summary']['blocker_count']}`\n"
        f"- Matrix rows: `{payload['summary']['matrix_row_count']}`\n"
        f"- Next owner: `{payload['next_owner']}`\n"
        f"- Note: {payload['note']}\n"
    )
    return payload
