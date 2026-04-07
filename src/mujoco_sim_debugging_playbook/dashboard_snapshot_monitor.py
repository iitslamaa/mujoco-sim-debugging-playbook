from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_monitor(
    *,
    dashboard_snapshot_history_path: str | Path,
    dashboard_snapshot_drift_path: str | Path,
    dashboard_snapshot_alerts_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    history = _read_json(dashboard_snapshot_history_path)
    drift = _read_json(dashboard_snapshot_drift_path)
    alerts = _read_json(dashboard_snapshot_alerts_path)

    current_status = history["summary"]["current_status"]
    projected_status = history["summary"]["projected_terminal_status"]
    first_pass_snapshot = drift["summary"].get("first_pass_snapshot")
    dominant_transition = drift["summary"].get("largest_failure_drop_transition")

    headlines = [
        f"Current dashboard status is {current_status}.",
        f"Projected terminal status is {projected_status}.",
        f"Largest recovery step is {dominant_transition}.",
    ]
    if first_pass_snapshot:
        headlines.append(f"First preserved pass state appears at {first_pass_snapshot}.")

    highest_priority_alert = alerts["alerts"][0] if alerts.get("alerts") else None

    payload = {
        "summary": {
            "current_status": current_status,
            "projected_terminal_status": projected_status,
            "headline_count": len(headlines),
            "alert_count": alerts["summary"]["alert_count"],
            "critical_count": alerts["summary"]["critical_count"],
            "dominant_transition": dominant_transition,
            "first_pass_snapshot": first_pass_snapshot,
        },
        "headlines": headlines,
        "highest_priority_alert": highest_priority_alert,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "monitor.json").write_text(json.dumps(payload, indent=2))
    (output / "monitor.md").write_text(render_dashboard_snapshot_monitor_markdown(payload))
    return payload


def render_dashboard_snapshot_monitor_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Monitor",
        "",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Projected terminal status: `{payload['summary']['projected_terminal_status']}`",
        f"- Headlines: `{payload['summary']['headline_count']}`",
        f"- Alerts: `{payload['summary']['alert_count']}`",
        f"- Critical alerts: `{payload['summary']['critical_count']}`",
        f"- Dominant transition: `{payload['summary']['dominant_transition']}`",
        f"- First pass snapshot: `{payload['summary']['first_pass_snapshot']}`",
        "",
        "## Headlines",
        "",
    ]
    for headline in payload["headlines"]:
        lines.append(f"- {headline}")
    lines.extend(["", "## Highest Priority Alert", ""])
    if payload["highest_priority_alert"]:
        alert = payload["highest_priority_alert"]
        lines.append(f"- [{alert['severity']}] {alert['title']}: {alert['message']}")
    else:
        lines.append("- None")
    return "\n".join(lines)
