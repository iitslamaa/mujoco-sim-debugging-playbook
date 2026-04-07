from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_release_blockers(
    *,
    release_checklist_path: str | Path,
    release_matrix_path: str | Path,
    output_dir: str | Path,
) -> dict:
    checklist = _read_json(release_checklist_path)
    matrix = _read_json(release_matrix_path)
    blockers = [item["name"] for item in checklist["items"] if item["status"] != "pass"]
    blockers.extend(row["dimension"] for row in matrix["rows"] if row["status"] != "pass")
    unique_blockers = sorted(set(blockers))
    payload = {
        "summary": {
            "status": "pass" if not unique_blockers else "warn",
            "blocker_count": len(unique_blockers),
        },
        "blockers": unique_blockers,
    }

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "release_blockers.json").write_text(json.dumps(payload, indent=2))
    (out / "release_blockers.md").write_text(
        "# Release Blockers\n\n"
        f"- Status: `{payload['summary']['status']}`\n"
        f"- Blockers: `{payload['summary']['blocker_count']}`\n"
    )
    return payload
