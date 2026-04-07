from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_artifact_actions(
    *,
    artifact_exec_summary_path: str | Path,
    artifact_delivery_path: str | Path,
    artifact_capacity_path: str | Path,
    artifact_history_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    exec_summary = _read_json(artifact_exec_summary_path)
    delivery = _read_json(artifact_delivery_path)
    capacity = _read_json(artifact_capacity_path)
    history = _read_json(artifact_history_path)

    actions = []

    for item in capacity.get("rebalance_items", [])[:3]:
        actions.append(
            {
                "priority": "P0",
                "target": item["artifact"],
                "owner": item["recommended_owner"],
                "phase": item["phase"],
                "reason": item["reason"],
                "expected_impact": "Reduce breach pressure on the support-report bundle.",
            }
        )

    next_due_phase = delivery["summary"].get("next_due_phase")
    if next_due_phase:
        actions.append(
            {
                "priority": "P1",
                "target": next_due_phase,
                "owner": "artifact-integrity",
                "phase": next_due_phase,
                "reason": "This is the nearest-due recovery phase in the current delivery forecast.",
                "expected_impact": "Prevent the current at-risk phase from becoming a breach.",
            }
        )

    if history["summary"]["projected_terminal_status"] == "pass":
        actions.append(
            {
                "priority": "P2",
                "target": "full_refresh_projection",
                "owner": "artifact-program",
                "phase": "Full artifact refresh",
                "reason": "History shows a full refresh is the path to a pass state.",
                "expected_impact": "Move the artifact surface from fail to pass.",
            }
        )

    payload = {
        "summary": {
            "action_count": len(actions),
            "current_status": exec_summary["summary"]["status"],
            "projected_terminal_status": history["summary"]["projected_terminal_status"],
            "top_risk_artifact": exec_summary["summary"]["top_risk_artifact"],
        },
        "actions": actions,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact_actions.json").write_text(json.dumps(payload, indent=2))
    (output / "artifact_actions.md").write_text(render_artifact_actions_markdown(payload))
    return payload


def render_artifact_actions_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Artifact Action Register",
        "",
        f"- Actions: `{payload['summary']['action_count']}`",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Projected terminal status: `{payload['summary']['projected_terminal_status']}`",
        f"- Top risk artifact: `{payload['summary']['top_risk_artifact']}`",
        "",
        "| priority | target | owner | phase | expected_impact |",
        "| --- | --- | --- | --- | --- |",
    ]
    for action in payload["actions"]:
        lines.append(
            f"| {action['priority']} | {action['target']} | {action['owner']} | {action['phase']} | {action['expected_impact']} |"
        )
    lines.extend(["", "## Action Notes", ""])
    for action in payload["actions"]:
        lines.append(f"- `{action['priority']}` `{action['target']}`: {action['reason']}")
    return "\n".join(lines)
