from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_release_evidence_packet(
    *,
    release_dry_run_path: str | Path,
    release_blockers_path: str | Path,
    release_matrix_path: str | Path,
    output_dir: str | Path,
) -> dict:
    dry_run = _read_json(release_dry_run_path)
    blockers = _read_json(release_blockers_path)
    matrix = _read_json(release_matrix_path)
    payload = {
        "summary": {
            "status": dry_run["summary"]["status"],
            "blocker_count": blockers["summary"]["blocker_count"],
            "matrix_row_count": matrix["summary"]["row_count"],
        },
        "recommendation": dry_run["recommendation"],
        "blockers": blockers["blockers"],
        "matrix": matrix["rows"],
    }
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "release_evidence_packet.json").write_text(json.dumps(payload, indent=2))
    (out / "release_evidence_packet.md").write_text(
        "# Release Evidence Packet\n\n"
        f"- Status: `{payload['summary']['status']}`\n"
        f"- Blockers: `{payload['summary']['blocker_count']}`\n"
        f"- Matrix rows: `{payload['summary']['matrix_row_count']}`\n"
        f"- Recommendation: {payload['recommendation']}\n"
    )
    return payload
