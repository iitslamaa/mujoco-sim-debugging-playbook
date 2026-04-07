from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_review(
    *,
    dashboard_snapshot_monitor_path: str | Path,
    dashboard_snapshot_alerts_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    monitor = _read_json(dashboard_snapshot_monitor_path)
    alerts = _read_json(dashboard_snapshot_alerts_path)

    top_alert = monitor.get("highest_priority_alert")
    next_focus = None
    if top_alert:
        next_focus = top_alert["title"]
    elif monitor["summary"].get("dominant_transition"):
        next_focus = monitor["summary"]["dominant_transition"]

    blockers = []
    if monitor["summary"]["current_status"] != "pass":
        blockers.append("Current dashboard status is not yet pass.")
    if alerts["summary"]["critical_count"] > 0:
        blockers.append("Critical snapshot alerts are still active.")
    if monitor["summary"]["projected_terminal_status"] != "pass":
        blockers.append("Projected terminal status has not yet converged to pass.")

    payload = {
        "summary": {
            "current_status": monitor["summary"]["current_status"],
            "projected_terminal_status": monitor["summary"]["projected_terminal_status"],
            "blocker_count": len(blockers),
            "headline_count": monitor["summary"]["headline_count"],
            "critical_count": alerts["summary"]["critical_count"],
            "next_focus": next_focus,
        },
        "headlines": monitor.get("headlines", []),
        "top_alert": top_alert,
        "blockers": blockers,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "review.json").write_text(json.dumps(payload, indent=2))
    (output / "review.md").write_text(render_dashboard_snapshot_review_markdown(payload))
    return payload


def render_dashboard_snapshot_review_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Review",
        "",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Projected terminal status: `{payload['summary']['projected_terminal_status']}`",
        f"- Headlines: `{payload['summary']['headline_count']}`",
        f"- Critical alerts: `{payload['summary']['critical_count']}`",
        f"- Blockers: `{payload['summary']['blocker_count']}`",
        f"- Next focus: `{payload['summary']['next_focus']}`",
        "",
        "## Headlines",
        "",
    ]
    for headline in payload["headlines"]:
        lines.append(f"- {headline}")
    lines.extend(["", "## Top Alert", ""])
    if payload["top_alert"]:
        alert = payload["top_alert"]
        lines.append(f"- [{alert['severity']}] {alert['title']}: {alert['message']}")
    else:
        lines.append("- None")
    lines.extend(["", "## Blockers", ""])
    if payload["blockers"]:
        for blocker in payload["blockers"]:
            lines.append(f"- {blocker}")
    else:
        lines.append("- None")
    return "\n".join(lines)
