from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.artifact_readiness import build_artifact_readiness


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _copy(payload: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(payload))


def _status_for(ok: bool, warning: bool) -> str:
    if not ok:
        return "fail"
    if warning:
        return "warn"
    return "pass"


def build_artifact_scenarios(
    *,
    artifact_freshness_path: str | Path,
    maintenance_risk_path: str | Path,
    refresh_checklist_path: str | Path,
    regeneration_plan_path: str | Path,
) -> dict[str, Any]:
    freshness = _read_json(artifact_freshness_path)
    maintenance_risk = _read_json(maintenance_risk_path)
    refresh_checklist = _read_json(refresh_checklist_path)
    regeneration_plan = _read_json(regeneration_plan_path)

    baseline = build_artifact_readiness(
        artifact_freshness_path=artifact_freshness_path,
        maintenance_risk_path=maintenance_risk_path,
        refresh_checklist_path=refresh_checklist_path,
        regeneration_plan_path=regeneration_plan_path,
    )

    scenarios = [
        _evaluate_scenario(
            name="Dashboard refresh only",
            description="Refresh the public dashboard artifact while leaving the support-report bundle untouched.",
            freshness=_patched_freshness(freshness, fresh_artifacts=["dashboard/data.json"]),
            maintenance_risk=_patched_maintenance_risk(
                maintenance_risk,
                cleared_artifacts=["dashboard/data.json"],
            ),
            refresh_checklist=_patched_refresh_checklist(refresh_checklist, removed_artifacts=["dashboard/data.json"]),
            regeneration_plan=_patched_regeneration_plan(regeneration_plan, removed_artifacts=["dashboard/data.json"]),
        ),
        _evaluate_scenario(
            name="Support report sprint",
            description="Refresh the support-report bundle but leave the dashboard artifact stale.",
            freshness=_patched_freshness(
                freshness,
                fresh_artifacts=[
                    "outputs/support_readiness/support_readiness.json",
                    "outputs/scenario_plan/scenario_plan.json",
                    "outputs/ops_review/ops_review.json",
                    "outputs/scorecard/scorecard.json",
                    "outputs/briefing_note/briefing_note.json",
                ],
            ),
            maintenance_risk=_patched_maintenance_risk(
                maintenance_risk,
                cleared_artifacts=[
                    "outputs/support_readiness/support_readiness.json",
                    "outputs/scenario_plan/scenario_plan.json",
                    "outputs/ops_review/ops_review.json",
                    "outputs/scorecard/scorecard.json",
                    "outputs/briefing_note/briefing_note.json",
                ],
            ),
            refresh_checklist=_patched_refresh_checklist(
                refresh_checklist,
                removed_artifacts=[
                    "outputs/support_readiness/support_readiness.json",
                    "outputs/scenario_plan/scenario_plan.json",
                    "outputs/ops_review/ops_review.json",
                    "outputs/scorecard/scorecard.json",
                    "outputs/briefing_note/briefing_note.json",
                ],
            ),
            regeneration_plan=_patched_regeneration_plan(
                regeneration_plan,
                removed_artifacts=[
                    "outputs/support_readiness/support_readiness.json",
                    "outputs/scenario_plan/scenario_plan.json",
                    "outputs/ops_review/ops_review.json",
                    "outputs/scorecard/scorecard.json",
                    "outputs/briefing_note/briefing_note.json",
                ],
            ),
        ),
        _evaluate_scenario(
            name="Top-risk stabilization",
            description="Refresh the highest-risk support outputs first, but leave lower-risk artifacts pending.",
            freshness=_patched_freshness(
                freshness,
                fresh_artifacts=[
                    "outputs/support_readiness/support_readiness.json",
                    "outputs/scenario_plan/scenario_plan.json",
                ],
            ),
            maintenance_risk=_patched_maintenance_risk(
                maintenance_risk,
                cleared_artifacts=[
                    "outputs/support_readiness/support_readiness.json",
                    "outputs/scenario_plan/scenario_plan.json",
                ],
            ),
            refresh_checklist=_patched_refresh_checklist(
                refresh_checklist,
                removed_artifacts=[
                    "outputs/support_readiness/support_readiness.json",
                    "outputs/scenario_plan/scenario_plan.json",
                ],
            ),
            regeneration_plan=_patched_regeneration_plan(
                regeneration_plan,
                removed_artifacts=[
                    "outputs/support_readiness/support_readiness.json",
                    "outputs/scenario_plan/scenario_plan.json",
                ],
            ),
        ),
        _evaluate_scenario(
            name="Full artifact refresh",
            description="Refresh every stale artifact so the published surface is fully current.",
            freshness=_patched_freshness(
                freshness,
                fresh_artifacts=[row["artifact"] for row in freshness["rows"]],
            ),
            maintenance_risk=_patched_maintenance_risk(
                maintenance_risk,
                cleared_artifacts=[row["artifact"] for row in maintenance_risk["rows"]],
            ),
            refresh_checklist=_patched_refresh_checklist(
                refresh_checklist,
                removed_artifacts=[row["artifact"] for bundle in refresh_checklist["bundles"] for row in bundle["steps"]],
            ),
            regeneration_plan=_patched_regeneration_plan(
                regeneration_plan,
                removed_artifacts=[row["artifact"] for row in regeneration_plan["actions"]],
            ),
        ),
    ]

    return {
        "baseline": baseline["summary"],
        "scenarios": scenarios,
    }


def _evaluate_scenario(
    *,
    name: str,
    description: str,
    freshness: dict[str, Any],
    maintenance_risk: dict[str, Any],
    refresh_checklist: dict[str, Any],
    regeneration_plan: dict[str, Any],
) -> dict[str, Any]:
    readiness = _evaluate_from_payloads(
        freshness=freshness,
        maintenance_risk=maintenance_risk,
        refresh_checklist=refresh_checklist,
        regeneration_plan=regeneration_plan,
    )
    return {
        "name": name,
        "description": description,
        "status": readiness["summary"]["status"],
        "failure_count": readiness["summary"]["failure_count"],
        "warning_count": readiness["summary"]["warning_count"],
        "top_risk_artifact": readiness["summary"]["top_risk_artifact"],
        "stale_count": readiness["summary"]["stale_count"],
        "refresh_step_count": readiness["summary"]["refresh_step_count"],
    }


def _evaluate_from_payloads(
    *,
    freshness: dict[str, Any],
    maintenance_risk: dict[str, Any],
    refresh_checklist: dict[str, Any],
    regeneration_plan: dict[str, Any],
) -> dict[str, Any]:
    tmp_root = Path("/tmp")
    freshness_path = tmp_root / "artifact_scenario_freshness.json"
    maintenance_risk_path = tmp_root / "artifact_scenario_maintenance_risk.json"
    refresh_checklist_path = tmp_root / "artifact_scenario_refresh_checklist.json"
    regeneration_plan_path = tmp_root / "artifact_scenario_regeneration_plan.json"
    freshness_path.write_text(json.dumps(freshness))
    maintenance_risk_path.write_text(json.dumps(maintenance_risk))
    refresh_checklist_path.write_text(json.dumps(refresh_checklist))
    regeneration_plan_path.write_text(json.dumps(regeneration_plan))
    return build_artifact_readiness(
        artifact_freshness_path=freshness_path,
        maintenance_risk_path=maintenance_risk_path,
        refresh_checklist_path=refresh_checklist_path,
        regeneration_plan_path=regeneration_plan_path,
    )


def _patched_freshness(payload: dict[str, Any], *, fresh_artifacts: list[str]) -> dict[str, Any]:
    copy = _copy(payload)
    fresh = set(fresh_artifacts)
    for row in copy["rows"]:
        if row["artifact"] in fresh:
            row["status"] = "fresh"
            row["age_delta_seconds"] = 0.0
    copy["summary"]["fresh_count"] = sum(1 for row in copy["rows"] if row["status"] == "fresh")
    copy["summary"]["stale_count"] = sum(1 for row in copy["rows"] if row["status"] == "stale")
    copy["summary"]["missing_count"] = sum(1 for row in copy["rows"] if row["status"] == "missing")
    return copy


def _patched_maintenance_risk(payload: dict[str, Any], *, cleared_artifacts: list[str]) -> dict[str, Any]:
    copy = _copy(payload)
    cleared = set(cleared_artifacts)
    for row in copy["rows"]:
        if row["artifact"] in cleared:
            row["status"] = "fresh"
            row["risk_score"] = 0.0
            row["priority"] = "low"
    copy["rows"].sort(key=lambda row: (-row["risk_score"], -row["impact_count"], row["artifact"]))
    copy["summary"]["high_risk_count"] = sum(1 for row in copy["rows"] if row["risk_score"] >= 1.5)
    copy["summary"]["medium_risk_count"] = sum(1 for row in copy["rows"] if 0.75 <= row["risk_score"] < 1.5)
    copy["summary"]["top_risk_artifact"] = copy["rows"][0]["artifact"] if copy["rows"] else None
    copy["summary"]["top_risk_score"] = copy["rows"][0]["risk_score"] if copy["rows"] else 0.0
    return copy


def _patched_refresh_checklist(payload: dict[str, Any], *, removed_artifacts: list[str]) -> dict[str, Any]:
    copy = _copy(payload)
    removed = set(removed_artifacts)
    bundles = []
    total_steps = 0
    for bundle in copy["bundles"]:
        steps = [step for step in bundle["steps"] if step["artifact"] not in removed]
        if not steps:
            continue
        bundle["steps"] = steps
        bundle["step_count"] = len(steps)
        bundle["validation_target"] = steps[-1]["artifact"]
        bundles.append(bundle)
        total_steps += len(steps)
    copy["bundles"] = bundles
    copy["summary"]["bundle_count"] = len(bundles)
    copy["summary"]["total_steps"] = total_steps
    return copy


def _patched_regeneration_plan(payload: dict[str, Any], *, removed_artifacts: list[str]) -> dict[str, Any]:
    copy = _copy(payload)
    removed = set(removed_artifacts)
    actions = [action for action in copy["actions"] if action["artifact"] not in removed]
    copy["actions"] = actions
    copy["summary"]["count"] = len(actions)
    copy["summary"]["high_priority_count"] = sum(1 for action in actions if action["priority"] == "high")
    return copy


def render_artifact_scenarios_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Artifact Scenarios",
        "",
        f"- Baseline status: `{payload['baseline']['status']}`",
        f"- Baseline failures: `{payload['baseline']['failure_count']}`",
        f"- Baseline warnings: `{payload['baseline']['warning_count']}`",
        "",
        "| scenario | status | failures | warnings | stale_count | refresh_steps |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for scenario in payload["scenarios"]:
        lines.append(
            f"| {scenario['name']} | {scenario['status']} | {scenario['failure_count']} | "
            f"{scenario['warning_count']} | {scenario['stale_count']} | {scenario['refresh_step_count']} |"
        )
    lines.extend(["", "## Scenario Notes", ""])
    for scenario in payload["scenarios"]:
        lines.append(f"### {scenario['name']}")
        lines.append("")
        lines.append(f"- {scenario['description']}")
        lines.append(f"- Top risk artifact after changes: `{scenario['top_risk_artifact']}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_artifact_scenarios(
    *,
    artifact_freshness_path: str | Path,
    maintenance_risk_path: str | Path,
    refresh_checklist_path: str | Path,
    regeneration_plan_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    payload = build_artifact_scenarios(
        artifact_freshness_path=artifact_freshness_path,
        maintenance_risk_path=maintenance_risk_path,
        refresh_checklist_path=refresh_checklist_path,
        regeneration_plan_path=regeneration_plan_path,
    )
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact_scenarios.json").write_text(json.dumps(payload, indent=2))
    (output / "artifact_scenarios.md").write_text(render_artifact_scenarios_markdown(payload))
    return payload
