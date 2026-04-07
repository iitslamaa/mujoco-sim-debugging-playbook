from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_repro_inventory(
    *,
    support_cases_dir: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    support_paths = sorted(Path(support_cases_dir).glob("*.md"))
    cases = []
    for path in support_paths:
        title = path.stem.replace("_", " ")
        cases.append(
            {
                "case_id": path.stem,
                "title": title,
                "path": str(path),
            }
        )

    payload = {
        "summary": {
            "case_count": len(cases),
            "documented_case_count": len(cases),
        },
        "cases": cases,
    }

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "repro_inventory.json").write_text(json.dumps(payload, indent=2))
    (out_dir / "repro_inventory.md").write_text(render_repro_inventory_markdown(payload))
    return payload


def render_repro_inventory_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Repro Inventory",
        "",
        f"- Cases: `{payload['summary']['case_count']}`",
        f"- Documented cases: `{payload['summary']['documented_case_count']}`",
        "",
    ]
    for case in payload["cases"]:
        lines.append(f"- `{case['case_id']}` | {case['title']} | {case['path']}")
    return "\n".join(lines)
