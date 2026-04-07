from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_status_brief(
    *,
    dashboard_snapshot_priorities_path: str | Path,
    dashboard_snapshot_monitor_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    priorities = _read_json(dashboard_snapshot_priorities_path)
    monitor = _read_json(dashboard_snapshot_monitor_path)

    top_priority = priorities.get("priorities", [{}])[0]
    payload = {
        "summary": {
            "current_status": priorities["summary"]["current_status"],
            "next_status": priorities["summary"]["next_status"],
            "projected_terminal_status": monitor["summary"]["projected_terminal_status"],
            "handoff_owner": priorities["summary"]["handoff_owner"],
            "top_priority": top_priority.get("objective", "Maintain dashboard stability"),
            "critical_alerts": monitor["summary"]["critical_count"],
        },
        "headlines": monitor.get("headlines", [])[:3],
        "blockers": priorities.get("blockers", [])[:2],
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "status_brief.json").write_text(json.dumps(payload, indent=2))
    (output / "status_brief.md").write_text(render_dashboard_snapshot_status_brief_markdown(payload))
    return payload


def render_dashboard_snapshot_status_brief_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Status Brief",
        "",
        f"- Handoff owner: `{payload['summary']['handoff_owner']}`",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Next status: `{payload['summary']['next_status']}`",
        f"- Projected terminal status: `{payload['summary']['projected_terminal_status']}`",
        f"- Top priority: `{payload['summary']['top_priority']}`",
        f"- Critical alerts: `{payload['summary']['critical_alerts']}`",
        "",
    ]
    for headline in payload["headlines"]:
        lines.append(f"- Headline: {headline}")
    for blocker in payload["blockers"]:
        lines.append(f"- Blocker: {blocker}")
    return "\n".join(lines)
