from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEPENDENCIES = {
    "dashboard/data.json": [
        "scripts/generate_dashboard.py",
        "outputs/support_readiness/support_readiness.json",
        "outputs/scenario_plan/scenario_plan.json",
        "outputs/ops_review/ops_review.json",
        "outputs/scorecard/scorecard.json",
        "outputs/briefing_note/briefing_note.json",
    ],
    "outputs/support_readiness/support_readiness.json": [
        "scripts/generate_support_readiness.py",
        "outputs/support_ops/support_ops.json",
        "outputs/support_gaps/support_gaps.json",
        "outputs/sla/sla_report.json",
        "outputs/capacity/capacity_plan.json",
        "outputs/releases/latest/release_notes.json",
    ],
    "outputs/scenario_plan/scenario_plan.json": [
        "scripts/generate_scenario_plan.py",
        "outputs/support_readiness/support_readiness.json",
    ],
    "outputs/ops_review/ops_review.json": [
        "scripts/generate_ops_review.py",
        "outputs/support_ops/support_ops.json",
        "outputs/capacity/capacity_plan.json",
        "outputs/anomalies/anomaly_report.json",
    ],
    "outputs/scorecard/scorecard.json": [
        "scripts/generate_scorecard.py",
        "outputs/support_ops/support_ops.json",
        "outputs/support_readiness/support_readiness.json",
        "outputs/scenario_plan/scenario_plan.json",
    ],
    "outputs/briefing_note/briefing_note.json": [
        "scripts/generate_briefing_note.py",
        "outputs/scorecard/scorecard.json",
        "outputs/ops_review/ops_review.json",
        "outputs/scenario_plan/scenario_plan.json",
    ],
}


def build_dependency_map(*, root: str | Path, artifacts: list[str]) -> dict[str, Any]:
    root = Path(root)
    rows = []
    for artifact in artifacts:
        deps = DEPENDENCIES.get(artifact, [])
        rows.append(
            {
                "artifact": artifact,
                "dependency_count": len(deps),
                "dependencies": deps,
                "existing_dependency_count": sum(1 for dep in deps if (root / dep).exists()),
            }
        )
    return {
        "summary": {
            "artifact_count": len(rows),
            "max_dependency_count": max((row["dependency_count"] for row in rows), default=0),
        },
        "rows": rows,
    }


def render_dependency_map_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dependency Map",
        "",
        f"- Artifacts mapped: `{payload['summary']['artifact_count']}`",
        f"- Max dependency count: `{payload['summary']['max_dependency_count']}`",
        "",
        "| artifact | dependency_count | existing_dependency_count |",
        "| --- | ---: | ---: |",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| {row['artifact']} | {row['dependency_count']} | {row['existing_dependency_count']} |"
        )
    lines.extend(["", "## Dependencies", ""])
    for row in payload["rows"]:
        lines.append(f"### {row['artifact']}")
        lines.append("")
        for dep in row["dependencies"]:
            lines.append(f"- {dep}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_dependency_map(*, root: str | Path, output_dir: str | Path, artifacts: list[str]) -> dict[str, Any]:
    payload = build_dependency_map(root=root, artifacts=artifacts)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "dependency_map.json").write_text(json.dumps(payload, indent=2))
    (output / "dependency_map.md").write_text(render_dependency_map_markdown(payload))
    return payload
