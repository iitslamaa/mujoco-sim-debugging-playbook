from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_lead(
    *,
    dashboard_snapshot_status_brief_path: str | Path,
    dashboard_snapshot_review_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    status_brief = _read_json(dashboard_snapshot_status_brief_path)
    review = _read_json(dashboard_snapshot_review_path)

    payload = {
        "summary": {
            "handoff_owner": status_brief["summary"]["handoff_owner"],
            "current_status": status_brief["summary"]["current_status"],
            "next_status": status_brief["summary"]["next_status"],
            "projected_terminal_status": status_brief["summary"]["projected_terminal_status"],
            "top_priority": status_brief["summary"]["top_priority"],
            "next_focus": review["summary"]["next_focus"],
            "critical_alerts": status_brief["summary"]["critical_alerts"],
        },
        "headlines": status_brief.get("headlines", [])[:2],
        "blockers": review.get("blockers", [])[:2],
        "lead_statement": (
            f"{status_brief['summary']['handoff_owner']} is driving "
            f"'{status_brief['summary']['top_priority']}' to move the dashboard from "
            f"{status_brief['summary']['current_status']} toward {status_brief['summary']['next_status']}."
        ),
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "lead.json").write_text(json.dumps(payload, indent=2))
    (output / "lead.md").write_text(render_dashboard_snapshot_lead_markdown(payload))
    return payload


def render_dashboard_snapshot_lead_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Lead",
        "",
        f"- Handoff owner: `{payload['summary']['handoff_owner']}`",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Next status: `{payload['summary']['next_status']}`",
        f"- Projected terminal status: `{payload['summary']['projected_terminal_status']}`",
        f"- Top priority: `{payload['summary']['top_priority']}`",
        f"- Next focus: `{payload['summary']['next_focus']}`",
        f"- Critical alerts: `{payload['summary']['critical_alerts']}`",
        f"- Lead statement: {payload['lead_statement']}",
        "",
    ]
    for headline in payload["headlines"]:
        lines.append(f"- Headline: {headline}")
    for blocker in payload["blockers"]:
        lines.append(f"- Blocker: {blocker}")
    return "\n".join(lines)
