from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_scorecard(
    *,
    dashboard_snapshot_monitor_path: str | Path,
    dashboard_snapshot_handoff_path: str | Path,
    dashboard_snapshot_closeout_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    monitor = _read_json(dashboard_snapshot_monitor_path)
    handoff = _read_json(dashboard_snapshot_handoff_path)
    closeout = _read_json(dashboard_snapshot_closeout_path)

    payload = {
        "summary": {
            "current_status": monitor["summary"]["current_status"],
            "projected_terminal_status": monitor["summary"]["projected_terminal_status"],
            "closeout_status": closeout["summary"]["closeout_status"],
            "handoff_owner": handoff["summary"]["handoff_owner"],
            "headline_count": monitor["summary"]["headline_count"],
            "alert_count": monitor["summary"]["alert_count"],
            "critical_count": monitor["summary"]["critical_count"],
            "blocker_count": closeout["summary"]["blocker_count"],
            "remaining_item_count": closeout["summary"]["remaining_item_count"],
            "dominant_transition": monitor["summary"]["dominant_transition"],
        }
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "scorecard.json").write_text(json.dumps(payload, indent=2))
    (output / "scorecard.md").write_text(render_dashboard_snapshot_scorecard_markdown(payload))
    return payload


def render_dashboard_snapshot_scorecard_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Dashboard Snapshot Scorecard",
        "",
        f"- Current status: `{summary['current_status']}`",
        f"- Projected terminal status: `{summary['projected_terminal_status']}`",
        f"- Closeout status: `{summary['closeout_status']}`",
        f"- Handoff owner: `{summary['handoff_owner']}`",
        f"- Headlines: `{summary['headline_count']}`",
        f"- Alerts: `{summary['alert_count']}`",
        f"- Critical alerts: `{summary['critical_count']}`",
        f"- Blockers: `{summary['blocker_count']}`",
        f"- Remaining items: `{summary['remaining_item_count']}`",
        f"- Dominant transition: `{summary['dominant_transition']}`",
    ]
    return "\n".join(lines)
