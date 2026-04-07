from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_history(
    *,
    dashboard_snapshot_path: str | Path,
    artifact_history_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    latest = _read_json(dashboard_snapshot_path)
    artifact_history = _read_json(artifact_history_path)

    snapshots = []
    for row in artifact_history["snapshots"]:
        snapshots.append(
            {
                "name": row["name"],
                "date": row["date"],
                "status": row["status"],
                "failure_count": row["failure_count"],
                "top_risk_score": row["top_risk_score"],
                "baseline_success_rate": latest["baseline_success_rate"],
            }
        )

    payload = {
        "summary": {
            "snapshot_count": len(snapshots),
            "current_status": latest["artifact_summary"]["current_status"],
            "status_direction": artifact_history["summary"]["status_direction"],
            "projected_terminal_status": artifact_history["summary"]["projected_terminal_status"],
        },
        "snapshots": snapshots,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "history.json").write_text(json.dumps(payload, indent=2))
    (output / "history.md").write_text(render_dashboard_snapshot_history_markdown(payload))
    return payload


def render_dashboard_snapshot_history_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot History",
        "",
        f"- Snapshots: `{payload['summary']['snapshot_count']}`",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Status direction: `{payload['summary']['status_direction']}`",
        f"- Projected terminal status: `{payload['summary']['projected_terminal_status']}`",
        "",
        "| snapshot | date | status | failures | top_risk_score | baseline_success_rate |",
        "| --- | --- | --- | ---: | ---: | ---: |",
    ]
    for row in payload["snapshots"]:
        lines.append(
            f"| {row['name']} | {row['date']} | {row['status']} | {row['failure_count']} | "
            f"{row['top_risk_score']:.3f} | {row['baseline_success_rate']:.3f} |"
        )
    return "\n".join(lines)
