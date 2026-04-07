from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_response_rubric(*, support_case_catalog_path: str | Path, output_dir: str | Path) -> dict:
    catalog = _read_json(support_case_catalog_path)
    rubric = [
        {"criterion": "Clear reproduction command", "status": "required"},
        {"criterion": "Observed behavior summary", "status": "required"},
        {"criterion": "Suggested next action", "status": "required"},
        {"criterion": "Evidence attachment", "status": "recommended"},
    ]
    payload = {
        "summary": {
            "criterion_count": len(rubric),
            "catalog_case_count": catalog["summary"]["case_count"],
        },
        "criteria": rubric,
    }
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "response_rubric.json").write_text(json.dumps(payload, indent=2))
    (out_dir / "response_rubric.md").write_text(
        "# Response Rubric\n\n" + "\n".join(f"- {r['criterion']} | {r['status']}" for r in rubric)
    )
    return payload
