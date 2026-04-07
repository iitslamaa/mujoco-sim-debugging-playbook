from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_release_packet(
    *,
    release_notes_path: str | Path,
    support_readiness_path: str | Path,
    ops_review_path: str | Path,
) -> dict[str, Any]:
    release_notes = _read_json(release_notes_path)
    support_readiness = _read_json(support_readiness_path)
    ops_review = _read_json(ops_review_path)
    return {
        "summary": {
            "base_ref": release_notes["base_ref"],
            "head_ref": release_notes["head_ref"],
            "commit_count": release_notes["commit_count"],
            "support_status": support_readiness["summary"]["status"],
            "breach_count": ops_review["summary"]["breach_count"],
        },
        "highlights": ops_review["wins"][:2],
        "risks": ops_review["risks"][:3],
    }
