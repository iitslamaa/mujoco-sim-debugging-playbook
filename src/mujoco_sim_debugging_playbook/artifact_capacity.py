from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _recommended_owner(artifact: str) -> str:
    if artifact == "dashboard/data.json":
        return "dashboard-maintenance"
    if "support_readiness" in artifact or "scenario_plan" in artifact:
        return "artifact-integrity"
    if "ops_review" in artifact or "scorecard" in artifact or "briefing_note" in artifact:
        return "artifact-reporting"
    return "artifact-generalist"


def _owner_label_for_phase(name: str) -> str:
    lowered = name.lower()
    if "dashboard" in lowered:
        return "dashboard-maintenance"
    if "support report" in lowered:
        return "artifact-reporting"
    return "artifact-integrity"


def build_artifact_capacity(
    *,
    artifact_delivery_path: str | Path,
    artifact_recovery_path: str | Path,
    maintenance_risk_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    delivery = _read_json(artifact_delivery_path)
    recovery = _read_json(artifact_recovery_path)
    maintenance_risk = _read_json(maintenance_risk_path)

    recovery_lookup = {phase["phase"]: phase for phase in recovery["phases"]}
    risk_lookup = {row["artifact"]: row for row in maintenance_risk["rows"]}

    phase_rows = []
    owner_load: dict[str, dict[str, Any]] = {}
    rebalance_actions = []

    for phase in delivery["phases"]:
        recovery_phase = recovery_lookup[phase["phase"]]
        owner = _owner_label_for_phase(phase["name"])
        command_count = len(recovery_phase["commands"])
        suggested_split = phase["status"] in {"breach", "at_risk"} and command_count >= 3

        phase_rows.append(
            {
                "phase": phase["phase"],
                "name": phase["name"],
                "owner": owner,
                "status": phase["status"],
                "estimated_days": phase["estimated_days"],
                "command_count": command_count,
                "focus_artifact_count": len(recovery_phase["focus_artifacts"]),
                "suggested_capacity_shift": max(0, command_count - 2) + (1 if phase["status"] == "breach" else 0),
                "action": (
                    "Split this phase across reporting and integrity owners."
                    if suggested_split
                    else "Keep current staffing and monitor progress."
                ),
            }
        )

        owner_entry = owner_load.setdefault(
            owner,
            {"owner": owner, "phase_count": 0, "command_count": 0, "breach_count": 0, "at_risk_count": 0}
        )
        owner_entry["phase_count"] += 1
        owner_entry["command_count"] += command_count
        owner_entry["breach_count"] += 1 if phase["status"] == "breach" else 0
        owner_entry["at_risk_count"] += 1 if phase["status"] == "at_risk" else 0

        if phase["status"] == "on_track":
            continue
        for artifact in recovery_phase["focus_artifacts"]:
            risk_row = risk_lookup.get(artifact, {"risk_score": 0.0})
            recommended_owner = _recommended_owner(artifact)
            if recommended_owner == owner:
                continue
            rebalance_actions.append(
                {
                    "phase": phase["name"],
                    "artifact": artifact,
                    "status": phase["status"],
                    "current_owner": owner,
                    "recommended_owner": recommended_owner,
                    "risk_score": risk_row["risk_score"],
                    "reason": (
                        "High-risk artifact should move to a more specialized owner."
                        if risk_row["risk_score"] >= 1.4
                        else "Parallelize lower-risk artifact work to reduce phase duration."
                    ),
                }
            )

    owners = []
    for owner, row in owner_load.items():
        overloaded = row["breach_count"] > 0 or row["command_count"] >= 5
        owners.append(
            {
                **row,
                "status": "overloaded" if overloaded else "healthy",
            }
        )

    payload = {
        "summary": {
            "owner_count": len(owners),
            "overloaded_owner_count": sum(1 for owner in owners if owner["status"] == "overloaded"),
            "phase_count": len(phase_rows),
            "rebalance_item_count": len(rebalance_actions),
            "highest_pressure_phase": max(phase_rows, key=lambda row: row["suggested_capacity_shift"])["name"] if phase_rows else None,
        },
        "owners": sorted(owners, key=lambda row: (row["status"] != "overloaded", -row["command_count"], row["owner"])),
        "phases": sorted(phase_rows, key=lambda row: (-row["suggested_capacity_shift"], row["phase"])),
        "rebalance_items": sorted(rebalance_actions, key=lambda row: (row["status"] != "breach", -row["risk_score"], row["artifact"])),
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact_capacity.json").write_text(json.dumps(payload, indent=2))
    (output / "artifact_capacity.md").write_text(render_artifact_capacity_markdown(payload))
    return payload


def render_artifact_capacity_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Artifact Capacity Plan",
        "",
        f"- Owners tracked: `{payload['summary']['owner_count']}`",
        f"- Overloaded owners: `{payload['summary']['overloaded_owner_count']}`",
        f"- Phases tracked: `{payload['summary']['phase_count']}`",
        f"- Rebalance items: `{payload['summary']['rebalance_item_count']}`",
        f"- Highest-pressure phase: `{payload['summary']['highest_pressure_phase']}`",
        "",
        "## Owner Load",
        "",
        "| owner | status | phases | commands | breaches | at_risk |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for owner in payload["owners"]:
        lines.append(
            f"| {owner['owner']} | {owner['status']} | {owner['phase_count']} | {owner['command_count']} | "
            f"{owner['breach_count']} | {owner['at_risk_count']} |"
        )

    lines.extend(["", "## Phase Actions", "", "| phase | owner | status | commands | shift | action |", "| --- | --- | --- | ---: | ---: | --- |"])
    for phase in payload["phases"]:
        lines.append(
            f"| {phase['name']} | {phase['owner']} | {phase['status']} | {phase['command_count']} | "
            f"{phase['suggested_capacity_shift']} | {phase['action']} |"
        )

    lines.extend(["", "## Rebalance Items", "", "| status | phase | artifact | current_owner | recommended_owner | risk_score | reason |", "| --- | --- | --- | --- | --- | ---: | --- |"])
    for item in payload["rebalance_items"]:
        lines.append(
            f"| {item['status']} | {item['phase']} | {item['artifact']} | {item['current_owner']} | "
            f"{item['recommended_owner']} | {item['risk_score']:.3f} | {item['reason']} |"
        )
    return "\n".join(lines)
