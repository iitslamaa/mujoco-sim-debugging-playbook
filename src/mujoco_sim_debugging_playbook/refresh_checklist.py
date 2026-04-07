from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_refresh_checklist(*, refresh_bundle_path: str | Path) -> dict[str, Any]:
    bundle_payload = _read_json(refresh_bundle_path)
    grouped: dict[str, list[dict[str, Any]]] = {}
    for action in bundle_payload["actions"]:
        grouped.setdefault(action["bundle"], []).append(action)

    bundles = []
    for bundle_name, actions in sorted(grouped.items()):
        ordered = sorted(actions, key=lambda item: (item["priority"] != "high", -item["impact_count"], item["artifact"]))
        bundles.append(
            {
                "bundle": bundle_name,
                "step_count": len(ordered),
                "validation_target": ordered[-1]["artifact"],
                "steps": [
                    {
                        "step": index + 1,
                        "artifact": action["artifact"],
                        "command": action["command"],
                        "follow_on_count": len(action["impacted_artifacts"]),
                    }
                    for index, action in enumerate(ordered)
                ],
            }
        )

    return {
        "summary": {
            "bundle_count": len(bundles),
            "total_steps": sum(bundle["step_count"] for bundle in bundles),
        },
        "bundles": bundles,
    }


def render_refresh_checklist_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Refresh Checklist",
        "",
        f"- Bundles: `{payload['summary']['bundle_count']}`",
        f"- Total steps: `{payload['summary']['total_steps']}`",
        "",
    ]
    for bundle in payload["bundles"]:
        lines.append(f"## {bundle['bundle']}")
        lines.append("")
        lines.append(f"- Validation target: `{bundle['validation_target']}`")
        for step in bundle["steps"]:
            lines.append(
                f"{step['step']}. `{step['command']}` to refresh `{step['artifact']}` "
                f"({step['follow_on_count']} downstream artifacts)"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_refresh_checklist(*, refresh_bundle_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    payload = build_refresh_checklist(refresh_bundle_path=refresh_bundle_path)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "refresh_checklist.json").write_text(json.dumps(payload, indent=2))
    (output / "refresh_checklist.md").write_text(render_refresh_checklist_markdown(payload))
    return payload
