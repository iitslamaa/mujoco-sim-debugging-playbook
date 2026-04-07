from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_issue_template_audit(*, template_dir: str | Path, output_dir: str | Path) -> dict[str, Any]:
    templates = []
    for path in sorted(Path(template_dir).glob("*.yml")):
        text = path.read_text()
        templates.append(
            {
                "name": path.name,
                "has_description": "description:" in text,
                "has_title": "name:" in text,
                "path": str(path),
            }
        )

    payload = {
        "summary": {
            "template_count": len(templates),
            "described_count": sum(1 for item in templates if item["has_description"]),
        },
        "templates": templates,
    }

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "issue_template_audit.json").write_text(json.dumps(payload, indent=2))
    (out_dir / "issue_template_audit.md").write_text(render_issue_template_audit_markdown(payload))
    return payload


def render_issue_template_audit_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Issue Template Audit",
        "",
        f"- Templates: `{payload['summary']['template_count']}`",
        f"- With descriptions: `{payload['summary']['described_count']}`",
        "",
    ]
    for item in payload["templates"]:
        lines.append(
            f"- `{item['name']}` | description `{item['has_description']}` | title `{item['has_title']}`"
        )
    return "\n".join(lines)
