from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_digest(
    *,
    dashboard_snapshot_scorecard_path: str | Path,
    dashboard_snapshot_closeout_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    scorecard = _read_json(dashboard_snapshot_scorecard_path)
    closeout = _read_json(dashboard_snapshot_closeout_path)
    summary = scorecard["summary"]

    headlines = [
        f"Dashboard snapshot status remains {summary['current_status']}.",
        f"Projected terminal status is {summary['projected_terminal_status']}.",
        f"Closeout remains {summary['closeout_status']}.",
    ]

    attention_points = []
    if summary["critical_count"] > 0:
        attention_points.append(f"{summary['critical_count']} critical alert remains active.")
    if summary["blocker_count"] > 0:
        attention_points.append(f"{summary['blocker_count']} blockers still prevent closeout.")
    if summary["remaining_item_count"] > 0:
        attention_points.append(f"{summary['remaining_item_count']} remaining items are still open.")

    payload = {
        "summary": {
            "headline_count": len(headlines),
            "attention_count": len(attention_points),
            "current_status": summary["current_status"],
            "closeout_status": summary["closeout_status"],
            "handoff_owner": summary["handoff_owner"],
        },
        "headlines": headlines,
        "attention_points": attention_points,
        "remaining_items": closeout.get("remaining_items", []),
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "digest.json").write_text(json.dumps(payload, indent=2))
    (output / "digest.md").write_text(render_dashboard_snapshot_digest_markdown(payload))
    return payload


def render_dashboard_snapshot_digest_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Digest",
        "",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Closeout status: `{payload['summary']['closeout_status']}`",
        f"- Handoff owner: `{payload['summary']['handoff_owner']}`",
        f"- Headlines: `{payload['summary']['headline_count']}`",
        f"- Attention points: `{payload['summary']['attention_count']}`",
        "",
        "## Headlines",
        "",
    ]
    for headline in payload["headlines"]:
        lines.append(f"- {headline}")
    lines.extend(["", "## Attention Points", ""])
    for point in payload["attention_points"]:
        lines.append(f"- {point}")
    lines.extend(["", "## Remaining Items", ""])
    for item in payload["remaining_items"]:
        lines.append(f"- {item}")
    return "\n".join(lines)
