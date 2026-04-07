from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_artifact_exec_summary(
    *,
    artifact_readiness_path: str | Path,
    maintenance_risk_path: str | Path,
    artifact_delivery_path: str | Path,
    artifact_capacity_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    readiness = _read_json(artifact_readiness_path)
    maintenance = _read_json(maintenance_risk_path)
    delivery = _read_json(artifact_delivery_path)
    capacity = _read_json(artifact_capacity_path)

    top_risk = maintenance["rows"][0] if maintenance.get("rows") else None
    breach_phase = next((row for row in delivery.get("phases", []) if row["status"] == "breach"), None)
    overloaded_owner = next((row for row in capacity.get("owners", []) if row["status"] == "overloaded"), None)

    wins = []
    if readiness["summary"]["warning_count"] == 0:
        wins.append("The artifact-readiness gate is surfacing crisp failures rather than ambiguous warnings.")
    wins.append(
        f"The capacity model narrowed the highest-pressure phase to `{capacity['summary']['highest_pressure_phase']}`."
    )
    wins.append(
        f"The recovery plan can still reach `{readiness['summary']['status']}` -> `pass` with the current three-phase structure."
    )

    risks = []
    if top_risk:
        risks.append(
            f"Top artifact risk remains `{top_risk['artifact']}` at score `{top_risk['risk_score']:.3f}`."
        )
    if breach_phase:
        risks.append(
            f"Delivery forecast shows `{breach_phase['name']}` in breach with due date `{breach_phase['due_date']}`."
        )
    if overloaded_owner:
        risks.append(
            f"Owner `{overloaded_owner['owner']}` is overloaded with `{overloaded_owner['command_count']}` commands across active phases."
        )

    next_actions = []
    for item in capacity.get("rebalance_items", [])[:3]:
        next_actions.append(
            {
                "artifact": item["artifact"],
                "phase": item["phase"],
                "owner": item["recommended_owner"],
                "action": item["reason"],
            }
        )

    payload = {
        "summary": {
            "status": readiness["summary"]["status"],
            "failure_count": readiness["summary"]["failure_count"],
            "top_risk_artifact": top_risk["artifact"] if top_risk else None,
            "top_risk_score": top_risk["risk_score"] if top_risk else 0.0,
            "breach_phase": breach_phase["name"] if breach_phase else None,
            "overloaded_owner": overloaded_owner["owner"] if overloaded_owner else None,
        },
        "wins": wins,
        "risks": risks,
        "next_actions": next_actions,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact_exec_summary.json").write_text(json.dumps(payload, indent=2))
    (output / "artifact_exec_summary.md").write_text(render_artifact_exec_summary_markdown(payload))
    return payload


def render_artifact_exec_summary_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Artifact Executive Summary",
        "",
        f"- Status: `{payload['summary']['status']}`",
        f"- Failures: `{payload['summary']['failure_count']}`",
        f"- Top risk artifact: `{payload['summary']['top_risk_artifact']}`",
        f"- Top risk score: `{payload['summary']['top_risk_score']:.3f}`",
        f"- Breach phase: `{payload['summary']['breach_phase']}`",
        f"- Overloaded owner: `{payload['summary']['overloaded_owner']}`",
        "",
        "## Wins",
        "",
    ]
    for win in payload["wins"]:
        lines.append(f"- {win}")
    lines.extend(["", "## Risks", ""])
    for risk in payload["risks"]:
        lines.append(f"- {risk}")
    lines.extend(["", "## Next Actions", "", "| artifact | phase | owner | action |", "| --- | --- | --- | --- |"])
    for item in payload["next_actions"]:
        lines.append(
            f"| {item['artifact']} | {item['phase']} | {item['owner']} | {item['action']} |"
        )
    return "\n".join(lines)
