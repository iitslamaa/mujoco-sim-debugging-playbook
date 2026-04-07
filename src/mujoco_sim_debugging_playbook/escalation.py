from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_escalation_matrix(
    *,
    triage_queue_path: str | Path,
    incidents_index_path: str | Path,
    regression_gate_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    triage = _read_json(triage_queue_path)
    incidents = _read_json(incidents_index_path)
    gate = _read_json(regression_gate_path)

    items = []
    incident_lookup = {bundle["target"]: bundle for bundle in incidents["bundles"]}
    for item in triage["items"]:
        incident = incident_lookup.get(item["target"])
        severity = _severity_for_item(item)
        owner = _owner_for_item(item)
        escalation = _escalation_for_item(item, gate["status"])
        items.append(
            {
                "target": item["target"],
                "kind": item["kind"],
                "priority_score": float(item["priority_score"]),
                "severity": severity,
                "owner": owner,
                "escalation_trigger": escalation["trigger"],
                "escalation_path": escalation["path"],
                "incident_bundle": incident["bundle_path"] if incident else None,
            }
        )

    payload = {
        "summary": {
            "count": len(items),
            "critical_count": sum(1 for item in items if item["severity"] == "critical"),
            "regression_gate_status": gate["status"],
        },
        "items": items,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "escalation_matrix.json").write_text(json.dumps(payload, indent=2))
    (output / "escalation_matrix.md").write_text(_render_markdown(payload))
    return payload


def _severity_for_item(item: dict[str, Any]) -> str:
    score = float(item["priority_score"])
    if score >= 210:
        return "critical"
    if score >= 80:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def _owner_for_item(item: dict[str, Any]) -> str:
    if item["kind"] == "randomized_episode":
        return "simulation-debugging"
    if item["kind"] == "benchmark_case":
        return "controls-and-policy"
    if item["kind"] == "regression_gate":
        return "release-validation"
    return "maintainer-review"


def _escalation_for_item(item: dict[str, Any], gate_status: str) -> dict[str, str]:
    if gate_status != "pass":
        return {
            "trigger": "Regression gate is failing",
            "path": "Escalate to release-validation and block further changes until the gate is green.",
        }
    if item["kind"] == "randomized_episode" and item["priority_score"] >= 210:
        return {
            "trigger": "Repeated zero-success episode under randomized dynamics",
            "path": "Escalate from self-serve debugging to simulator/policy review with incident bundle attached.",
        }
    if item["kind"] == "benchmark_case" and item["priority_score"] >= 80:
        return {
            "trigger": "Sustained benchmark risk in a named stress scenario",
            "path": "Escalate to controls-and-policy owners after reproducing with fixed seeds.",
        }
    return {
        "trigger": "No hard escalation trigger met",
        "path": "Handle in support/self-serve workflow and update documentation if the mitigation is validated.",
    }


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Escalation Matrix",
        "",
        f"Tracked triage items: `{payload['summary']['count']}`",
        "",
        f"Critical items: `{payload['summary']['critical_count']}`",
        "",
        "| severity | owner | target | escalation_trigger | escalation_path | incident_bundle |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in payload["items"]:
        lines.append(
            f"| {item['severity']} | {item['owner']} | {item['target']} | {item['escalation_trigger']} | "
            f"{item['escalation_path']} | {item['incident_bundle'] or '--'} |"
        )
    return "\n".join(lines)
