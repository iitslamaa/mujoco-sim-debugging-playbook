from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot(
    *,
    dashboard_data_path: str | Path,
    artifact_packet_path: str | Path,
    output_dir: str | Path,
    snapshot_name: str = "latest",
    snapshot_date: date | None = None,
) -> dict[str, Any]:
    dashboard = _read_json(dashboard_data_path)
    packet = _read_json(artifact_packet_path)
    snapshot_date = snapshot_date or date.today()

    payload = {
        "name": snapshot_name,
        "date": snapshot_date.isoformat(),
        "repo": dashboard.get("repo"),
        "baseline_success_rate": dashboard.get("baseline_summary", {}).get("success_rate"),
        "artifact_summary": packet["summary"],
        "highlights": [
            f"Current status: {packet['summary']['current_status']}",
            f"Closeout status: {packet['summary']['closeout_status']}",
            f"Projected terminal status: {packet['summary']['projected_terminal_status']}",
            f"Handoff owner: {packet['summary']['handoff_owner']}",
        ],
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / f"{snapshot_name}.json").write_text(json.dumps(payload, indent=2))
    (output / f"{snapshot_name}.md").write_text(render_dashboard_snapshot_markdown(payload))
    return payload


def render_dashboard_snapshot_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot",
        "",
        f"- Name: `{payload['name']}`",
        f"- Date: `{payload['date']}`",
        f"- Repo: `{payload['repo']}`",
        f"- Baseline success rate: `{payload['baseline_success_rate']}`",
        "",
        "## Artifact Summary",
        "",
        f"- Current status: `{payload['artifact_summary']['current_status']}`",
        f"- Closeout status: `{payload['artifact_summary']['closeout_status']}`",
        f"- Projected terminal status: `{payload['artifact_summary']['projected_terminal_status']}`",
        f"- Handoff owner: `{payload['artifact_summary']['handoff_owner']}`",
        "",
        "## Highlights",
        "",
    ]
    for item in payload["highlights"]:
        lines.append(f"- {item}")
    return "\n".join(lines)
