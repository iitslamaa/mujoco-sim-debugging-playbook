from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_artifact_recovery(
    *,
    artifact_readiness_path: str | Path,
    artifact_scenarios_path: str | Path,
    maintenance_risk_path: str | Path,
    refresh_checklist_path: str | Path,
) -> dict[str, Any]:
    readiness = _read_json(artifact_readiness_path)
    scenarios = _read_json(artifact_scenarios_path)
    maintenance_risk = _read_json(maintenance_risk_path)
    refresh_checklist = _read_json(refresh_checklist_path)

    top_risks = maintenance_risk["rows"][:5]
    scenario_lookup = {row["name"]: row for row in scenarios["scenarios"]}
    checklist_lookup = {bundle["bundle"]: bundle for bundle in refresh_checklist["bundles"]}

    phases = [
        {
            "phase": 1,
            "name": "Stabilize top risks",
            "goal": "Reduce the highest-impact stale artifacts first to shrink maintenance risk quickly.",
            "expected_status": scenario_lookup["Top-risk stabilization"]["status"],
            "expected_failure_count": scenario_lookup["Top-risk stabilization"]["failure_count"],
            "commands": [
                row["command"]
                for row in top_risks[:2]
            ],
            "focus_artifacts": [row["artifact"] for row in top_risks[:2]],
        },
        {
            "phase": 2,
            "name": "Clear support report bundle",
            "goal": "Refresh the support-report bundle so the public support surface is nearly current.",
            "expected_status": scenario_lookup["Support report sprint"]["status"],
            "expected_failure_count": scenario_lookup["Support report sprint"]["failure_count"],
            "commands": [
                step["command"]
                for step in checklist_lookup["support_report_refresh"]["steps"]
            ],
            "focus_artifacts": [
                step["artifact"]
                for step in checklist_lookup["support_report_refresh"]["steps"]
            ],
        },
        {
            "phase": 3,
            "name": "Clear dashboard lag",
            "goal": "Refresh the public dashboard so the surfaced state matches the refreshed support reports.",
            "expected_status": scenario_lookup["Full artifact refresh"]["status"],
            "expected_failure_count": scenario_lookup["Full artifact refresh"]["failure_count"],
            "commands": [
                step["command"]
                for step in checklist_lookup["dashboard_refresh"]["steps"]
            ],
            "focus_artifacts": [
                step["artifact"]
                for step in checklist_lookup["dashboard_refresh"]["steps"]
            ],
        },
    ]

    summary = {
        "current_status": readiness["summary"]["status"],
        "current_failure_count": readiness["summary"]["failure_count"],
        "phase_count": len(phases),
        "top_risk_artifact": maintenance_risk["summary"]["top_risk_artifact"],
        "target_status": phases[-1]["expected_status"],
    }
    return {
        "summary": summary,
        "phases": phases,
    }


def render_artifact_recovery_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Artifact Recovery Roadmap",
        "",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Current failures: `{payload['summary']['current_failure_count']}`",
        f"- Phases: `{payload['summary']['phase_count']}`",
        f"- Top risk artifact: `{payload['summary']['top_risk_artifact']}`",
        f"- Target status: `{payload['summary']['target_status']}`",
        "",
        "| phase | expected_status | expected_failures | goal |",
        "| --- | --- | ---: | --- |",
    ]
    for phase in payload["phases"]:
        lines.append(
            f"| {phase['phase']}: {phase['name']} | {phase['expected_status']} | "
            f"{phase['expected_failure_count']} | {phase['goal']} |"
        )
    lines.extend(["", "## Phase Plan", ""])
    for phase in payload["phases"]:
        lines.append(f"### Phase {phase['phase']}: {phase['name']}")
        lines.append("")
        lines.append(f"- Goal: {phase['goal']}")
        lines.append(f"- Expected status after phase: `{phase['expected_status']}`")
        lines.append(f"- Expected failures after phase: `{phase['expected_failure_count']}`")
        lines.append("- Focus artifacts:")
        for artifact in phase["focus_artifacts"]:
            lines.append(f"- `{artifact}`")
        lines.append("- Commands:")
        for command in phase["commands"]:
            lines.append(f"- `{command}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_artifact_recovery(
    *,
    artifact_readiness_path: str | Path,
    artifact_scenarios_path: str | Path,
    maintenance_risk_path: str | Path,
    refresh_checklist_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    payload = build_artifact_recovery(
        artifact_readiness_path=artifact_readiness_path,
        artifact_scenarios_path=artifact_scenarios_path,
        maintenance_risk_path=maintenance_risk_path,
        refresh_checklist_path=refresh_checklist_path,
    )
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact_recovery.json").write_text(json.dumps(payload, indent=2))
    (output / "artifact_recovery.md").write_text(render_artifact_recovery_markdown(payload))
    return payload
