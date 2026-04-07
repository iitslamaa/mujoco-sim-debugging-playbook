from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.readiness import evaluate_support_readiness


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_scenario_plan(
    *,
    support_ops_path: str | Path,
    support_gaps_path: str | Path,
    sla_report_path: str | Path,
    capacity_plan_path: str | Path,
    release_notes_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    support_ops = _read_json(support_ops_path)
    support_gaps = _read_json(support_gaps_path)
    sla = _read_json(sla_report_path)
    capacity = _read_json(capacity_plan_path)
    release_notes = _read_json(release_notes_path)

    baseline = evaluate_support_readiness(
        support_ops=support_ops,
        support_gaps=support_gaps,
        sla=sla,
        capacity=capacity,
        release_notes=release_notes,
    )

    scenarios = [
        _build_scenario(
            name="Clear breaches",
            description="Resolve the currently breaching support items without changing coverage levels.",
            support_ops=support_ops,
            support_gaps=support_gaps,
            sla=_patched_sla(sla, breach_count=0, at_risk_count=max(0, sla["summary"]["at_risk_count"] - 1)),
            capacity=_patched_capacity(capacity, overloaded=max(0, capacity["summary"]["overloaded_owner_count"] - 1)),
            release_notes=release_notes,
        ),
        _build_scenario(
            name="Coverage sprint",
            description="Add support assets for the highest-priority gaps and increase self-serve coverage.",
            support_ops=_patched_support_ops(
                support_ops,
                incident_coverage=min(1.0, support_ops["summary"]["incident_coverage"] + 0.2),
                knowledge_base_coverage=min(1.0, support_ops["summary"]["knowledge_base_coverage"] + 0.2),
            ),
            support_gaps=_patched_support_gaps(
                support_gaps,
                needs_follow_up=max(0, support_gaps["summary"]["needs_follow_up_count"] - 3),
            ),
            sla=sla,
            capacity=capacity,
            release_notes=release_notes,
        ),
        _build_scenario(
            name="Full stabilization",
            description="Resolve breaches, rebalance owners, and close the top coverage gaps in one coordinated pass.",
            support_ops=_patched_support_ops(
                support_ops,
                incident_coverage=min(1.0, support_ops["summary"]["incident_coverage"] + 0.25),
                knowledge_base_coverage=min(1.0, support_ops["summary"]["knowledge_base_coverage"] + 0.25),
            ),
            support_gaps=_patched_support_gaps(
                support_gaps,
                needs_follow_up=max(0, support_gaps["summary"]["needs_follow_up_count"] - 5),
            ),
            sla=_patched_sla(sla, breach_count=0, at_risk_count=max(0, sla["summary"]["at_risk_count"] - 2)),
            capacity=_patched_capacity(capacity, overloaded=0),
            release_notes=release_notes,
        ),
    ]

    payload = {
        "baseline": {
            "status": baseline["summary"]["status"],
            "failure_count": baseline["summary"]["failure_count"],
            "warning_count": baseline["summary"]["warning_count"],
        },
        "scenarios": scenarios,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "scenario_plan.json").write_text(json.dumps(payload, indent=2))
    (output / "scenario_plan.md").write_text(_render_markdown(payload))
    return payload


def _build_scenario(
    *,
    name: str,
    description: str,
    support_ops: dict[str, Any],
    support_gaps: dict[str, Any],
    sla: dict[str, Any],
    capacity: dict[str, Any],
    release_notes: dict[str, Any],
) -> dict[str, Any]:
    evaluation = evaluate_support_readiness(
        support_ops=support_ops,
        support_gaps=support_gaps,
        sla=sla,
        capacity=capacity,
        release_notes=release_notes,
    )
    return {
        "name": name,
        "description": description,
        "status": evaluation["summary"]["status"],
        "failure_count": evaluation["summary"]["failure_count"],
        "warning_count": evaluation["summary"]["warning_count"],
        "check_count": evaluation["summary"]["check_count"],
        "notable_changes": [
            check["message"]
            for check in evaluation["checks"]
            if check["status"] in {"pass", "warn"}
        ][:4],
    }


def _patched_support_ops(payload: dict[str, Any], *, incident_coverage: float, knowledge_base_coverage: float) -> dict[str, Any]:
    copy = json.loads(json.dumps(payload))
    copy["summary"]["incident_coverage"] = incident_coverage
    copy["summary"]["knowledge_base_coverage"] = knowledge_base_coverage
    return copy


def _patched_support_gaps(payload: dict[str, Any], *, needs_follow_up: int) -> dict[str, Any]:
    copy = json.loads(json.dumps(payload))
    copy["summary"]["needs_follow_up_count"] = needs_follow_up
    return copy


def _patched_sla(payload: dict[str, Any], *, breach_count: int, at_risk_count: int) -> dict[str, Any]:
    copy = json.loads(json.dumps(payload))
    copy["summary"]["breach_count"] = breach_count
    copy["summary"]["at_risk_count"] = at_risk_count
    return copy


def _patched_capacity(payload: dict[str, Any], *, overloaded: int) -> dict[str, Any]:
    copy = json.loads(json.dumps(payload))
    copy["summary"]["overloaded_owner_count"] = overloaded
    return copy


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Support Scenario Planner",
        "",
        f"- Baseline status: `{payload['baseline']['status']}`",
        f"- Baseline failures: `{payload['baseline']['failure_count']}`",
        f"- Baseline warnings: `{payload['baseline']['warning_count']}`",
        "",
        "| scenario | status | failures | warnings | description |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for scenario in payload["scenarios"]:
        lines.append(
            f"| {scenario['name']} | {scenario['status']} | {scenario['failure_count']} | "
            f"{scenario['warning_count']} | {scenario['description']} |"
        )
    lines.extend(["", "## Scenario Notes", ""])
    for scenario in payload["scenarios"]:
        lines.append(f"### {scenario['name']}")
        lines.append("")
        for note in scenario["notable_changes"]:
            lines.append(f"- {note}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
