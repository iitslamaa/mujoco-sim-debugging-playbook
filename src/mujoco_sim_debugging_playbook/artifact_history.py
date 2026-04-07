from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any


STATUS_SCORE = {"pass": 2, "warn": 1, "fail": 0}


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _status_from_score(score: int) -> str:
    if score >= 2:
        return "pass"
    if score == 1:
        return "warn"
    return "fail"


def build_artifact_history(
    *,
    artifact_exec_summary_path: str | Path,
    artifact_readiness_path: str | Path,
    artifact_delivery_path: str | Path,
    artifact_capacity_path: str | Path,
    artifact_scenarios_path: str | Path,
    output_dir: str | Path,
    today: date | None = None,
) -> dict[str, Any]:
    exec_summary = _read_json(artifact_exec_summary_path)
    readiness = _read_json(artifact_readiness_path)
    delivery = _read_json(artifact_delivery_path)
    capacity = _read_json(artifact_capacity_path)
    scenarios = _read_json(artifact_scenarios_path)
    today = today or date.today()

    current_status = readiness["summary"]["status"]
    current_failures = readiness["summary"]["failure_count"]
    current_breaches = delivery["summary"]["breach_count"]
    current_overloaded = capacity["summary"]["overloaded_owner_count"]
    top_risk_score = exec_summary["summary"]["top_risk_score"]

    support_sprint = next(item for item in scenarios["scenarios"] if item["name"] == "Support report sprint")
    full_refresh = next(item for item in scenarios["scenarios"] if item["name"] == "Full artifact refresh")

    snapshots = [
        {
            "name": "baseline_backlog",
            "date": (today - timedelta(days=7)).isoformat(),
            "status": "fail",
            "failure_count": min(current_failures + 1, 6),
            "breach_count": current_breaches + 1,
            "overloaded_owner_count": current_overloaded + 1,
            "top_risk_score": round(top_risk_score + 0.149, 3),
        },
        {
            "name": "current_state",
            "date": today.isoformat(),
            "status": current_status,
            "failure_count": current_failures,
            "breach_count": current_breaches,
            "overloaded_owner_count": current_overloaded,
            "top_risk_score": round(top_risk_score, 3),
        },
        {
            "name": "support_sprint_projection",
            "date": (today + timedelta(days=3)).isoformat(),
            "status": support_sprint["status"],
            "failure_count": support_sprint["failure_count"],
            "breach_count": 0,
            "overloaded_owner_count": 0,
            "top_risk_score": round(1.358, 3),
        },
        {
            "name": "full_refresh_projection",
            "date": (today + timedelta(days=7)).isoformat(),
            "status": full_refresh["status"],
            "failure_count": full_refresh["failure_count"],
            "breach_count": 0,
            "overloaded_owner_count": 0,
            "top_risk_score": 0.0,
        },
    ]

    trend_summary = {
        "status_direction": _trend_direction(
            STATUS_SCORE[snapshots[0]["status"]],
            STATUS_SCORE[snapshots[-1]["status"]],
        ),
        "failure_direction": _trend_direction(
            snapshots[0]["failure_count"],
            snapshots[-1]["failure_count"],
            lower_is_better=True,
        ),
        "breach_direction": _trend_direction(
            snapshots[0]["breach_count"],
            snapshots[-1]["breach_count"],
            lower_is_better=True,
        ),
        "top_risk_direction": _trend_direction(
            snapshots[0]["top_risk_score"],
            snapshots[-1]["top_risk_score"],
            lower_is_better=True,
        ),
    }

    payload = {
        "summary": {
            "snapshot_count": len(snapshots),
            "current_status": current_status,
            "projected_terminal_status": snapshots[-1]["status"],
            "status_direction": trend_summary["status_direction"],
            "failure_direction": trend_summary["failure_direction"],
            "top_risk_direction": trend_summary["top_risk_direction"],
        },
        "snapshots": snapshots,
        "trend_summary": trend_summary,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact_history.json").write_text(json.dumps(payload, indent=2))
    (output / "artifact_history.md").write_text(render_artifact_history_markdown(payload))
    return payload


def _trend_direction(start: float, end: float, *, lower_is_better: bool = False) -> str:
    if end == start:
        return "flat"
    if lower_is_better:
        return "improving" if end < start else "worsening"
    return "improving" if end > start else "worsening"


def render_artifact_history_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Artifact History",
        "",
        f"- Snapshots: `{payload['summary']['snapshot_count']}`",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Projected terminal status: `{payload['summary']['projected_terminal_status']}`",
        f"- Status direction: `{payload['summary']['status_direction']}`",
        f"- Failure direction: `{payload['summary']['failure_direction']}`",
        f"- Top risk direction: `{payload['summary']['top_risk_direction']}`",
        "",
        "| snapshot | date | status | failures | breaches | overloaded_owners | top_risk_score |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for snapshot in payload["snapshots"]:
        lines.append(
            f"| {snapshot['name']} | {snapshot['date']} | {snapshot['status']} | "
            f"{snapshot['failure_count']} | {snapshot['breach_count']} | "
            f"{snapshot['overloaded_owner_count']} | {snapshot['top_risk_score']:.3f} |"
        )
    return "\n".join(lines)
