from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _phase_status(expected_failures: int, due_in_days: int) -> str:
    if expected_failures > 0 and due_in_days > 3:
        return "breach"
    if expected_failures > 0 and due_in_days > 1:
        return "at_risk"
    if due_in_days > 5:
        return "at_risk"
    return "on_track"


def build_artifact_delivery(
    *,
    artifact_recovery_path: str | Path,
    maintenance_risk_path: str | Path,
    refresh_checklist_path: str | Path,
    output_dir: str | Path,
    today: date | None = None,
) -> dict[str, Any]:
    recovery = _read_json(artifact_recovery_path)
    maintenance_risk = _read_json(maintenance_risk_path)
    refresh_checklist = _read_json(refresh_checklist_path)
    today = today or date.today()

    risk_lookup = {row["artifact"]: row for row in maintenance_risk["rows"]}
    bundle_lookup = {}
    for bundle in refresh_checklist["bundles"]:
        for step in bundle["steps"]:
            bundle_lookup[step["artifact"]] = bundle["bundle"]

    phases = []
    cumulative_days = 0
    for phase in recovery["phases"]:
        focus_rows = [risk_lookup.get(artifact, {"risk_score": 0.0}) for artifact in phase["focus_artifacts"]]
        max_risk = max((row["risk_score"] for row in focus_rows), default=0.0)
        avg_risk = sum(row["risk_score"] for row in focus_rows) / max(len(focus_rows), 1)
        estimated_days = max(1, len(phase["commands"])) + (1 if max_risk >= 1.5 else 0)
        cumulative_days += estimated_days
        due_date = today + timedelta(days=cumulative_days)
        status = _phase_status(phase["expected_failure_count"], cumulative_days)
        phases.append(
            {
                "phase": phase["phase"],
                "name": phase["name"],
                "expected_status": phase["expected_status"],
                "expected_failure_count": phase["expected_failure_count"],
                "estimated_days": estimated_days,
                "due_in_days": cumulative_days,
                "due_date": due_date.isoformat(),
                "status": status,
                "focus_artifact_count": len(phase["focus_artifacts"]),
                "max_risk_score": round(max_risk, 3),
                "avg_risk_score": round(avg_risk, 3),
                "bundle_mix": sorted({bundle_lookup.get(artifact, "unmapped") for artifact in phase["focus_artifacts"]}),
            }
        )

    ordered = sorted(phases, key=lambda row: (_status_rank(row["status"]), row["due_in_days"], row["phase"]))
    payload = {
        "summary": {
            "phase_count": len(phases),
            "breach_count": sum(1 for row in phases if row["status"] == "breach"),
            "at_risk_count": sum(1 for row in phases if row["status"] == "at_risk"),
            "next_due_phase": phases[0]["name"] if phases else None,
            "slowest_phase": max(phases, key=lambda row: row["estimated_days"])["name"] if phases else None,
        },
        "phases": ordered,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact_delivery.json").write_text(json.dumps(payload, indent=2))
    (output / "artifact_delivery.md").write_text(render_artifact_delivery_markdown(payload))
    return payload


def _status_rank(status: str) -> int:
    order = {"breach": 0, "at_risk": 1, "on_track": 2}
    return order.get(status, 99)


def render_artifact_delivery_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Artifact Delivery Forecast",
        "",
        f"- Phases: `{payload['summary']['phase_count']}`",
        f"- At risk: `{payload['summary']['at_risk_count']}`",
        f"- Breaches: `{payload['summary']['breach_count']}`",
        f"- Next due phase: `{payload['summary']['next_due_phase']}`",
        f"- Slowest phase: `{payload['summary']['slowest_phase']}`",
        "",
        "| status | due_date | phase | estimated_days | expected_status | max_risk_score |",
        "| --- | --- | --- | ---: | --- | ---: |",
    ]
    for phase in payload["phases"]:
        lines.append(
            f"| {phase['status']} | {phase['due_date']} | {phase['phase']}: {phase['name']} | "
            f"{phase['estimated_days']} | {phase['expected_status']} | {phase['max_risk_score']:.3f} |"
        )
    return "\n".join(lines)
