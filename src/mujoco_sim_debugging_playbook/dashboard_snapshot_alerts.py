from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_alerts(
    *,
    dashboard_snapshot_drift_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    drift = _read_json(dashboard_snapshot_drift_path)
    alerts: list[dict[str, Any]] = []

    first_pass = drift["summary"].get("first_pass_snapshot")
    if first_pass:
        alerts.append(
            {
                "severity": "info",
                "title": "First pass milestone reached",
                "message": f"Dashboard state first reaches pass at {first_pass}.",
            }
        )

    for transition in drift.get("transitions", []):
        label = f"{transition['from']} -> {transition['to']}"
        if transition["status_changed"] and transition["to_status"] == "pass":
            alerts.append(
                {
                    "severity": "critical",
                    "title": "Status transition to pass",
                    "message": f"{label} changes status from {transition['from_status']} to pass.",
                }
            )
        if transition["failure_delta"] <= -3:
            alerts.append(
                {
                    "severity": "warning",
                    "title": "Large failure drop detected",
                    "message": f"{label} reduces failures by {abs(transition['failure_delta'])}.",
                }
            )
        if transition["risk_delta"] <= -1.0:
            alerts.append(
                {
                    "severity": "warning",
                    "title": "Large risk drop detected",
                    "message": f"{label} reduces top risk by {abs(transition['risk_delta']):.3f}.",
                }
            )

    severity_order = {"critical": 0, "warning": 1, "info": 2}
    alerts.sort(key=lambda item: (severity_order[item["severity"]], item["title"]))

    counts = {key: 0 for key in severity_order}
    for alert in alerts:
        counts[alert["severity"]] += 1

    payload = {
        "summary": {
            "alert_count": len(alerts),
            "critical_count": counts["critical"],
            "warning_count": counts["warning"],
            "info_count": counts["info"],
        },
        "alerts": alerts,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "alerts.json").write_text(json.dumps(payload, indent=2))
    (output / "alerts.md").write_text(render_dashboard_snapshot_alerts_markdown(payload))
    return payload


def render_dashboard_snapshot_alerts_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Alerts",
        "",
        f"- Alerts: `{payload['summary']['alert_count']}`",
        f"- Critical: `{payload['summary']['critical_count']}`",
        f"- Warning: `{payload['summary']['warning_count']}`",
        f"- Info: `{payload['summary']['info_count']}`",
        "",
    ]
    for alert in payload["alerts"]:
        lines.append(f"- [{alert['severity']}] {alert['title']}: {alert['message']}")
    return "\n".join(lines)
