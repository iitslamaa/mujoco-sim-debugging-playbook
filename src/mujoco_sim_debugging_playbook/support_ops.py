from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_support_ops_report(
    *,
    triage_queue_path: str | Path,
    incidents_index_path: str | Path,
    knowledge_base_index_path: str | Path,
    escalation_matrix_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    triage = _read_json(triage_queue_path)
    incidents = _read_json(incidents_index_path)
    knowledge_base = _read_json(knowledge_base_index_path)
    escalation = _read_json(escalation_matrix_path)

    triage_targets = {item["target"] for item in triage["items"]}
    incident_targets = {bundle["target"] for bundle in incidents["bundles"]}
    kb_targets = {entry["target"] for entry in knowledge_base["entries"]}

    severity_counts = Counter(item["severity"] for item in escalation["items"])
    owner_counts = Counter(item["owner"] for item in escalation["items"])

    queue_count = len(triage["items"])
    incident_coverage = len(incident_targets & triage_targets) / queue_count if queue_count else 0.0
    knowledge_base_coverage = len(kb_targets & triage_targets) / queue_count if queue_count else 0.0
    escalated_count = sum(
        1
        for item in escalation["items"]
        if "Escalate" in item["escalation_path"]
    )
    self_serve_count = queue_count - escalated_count

    payload = {
        "summary": {
            "queue_count": queue_count,
            "incident_count": len(incidents["bundles"]),
            "knowledge_base_count": len(knowledge_base["entries"]),
            "escalated_count": escalated_count,
            "self_serve_count": self_serve_count,
            "incident_coverage": incident_coverage,
            "knowledge_base_coverage": knowledge_base_coverage,
        },
        "severity_counts": dict(severity_counts),
        "owner_counts": dict(owner_counts),
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "support_ops.json").write_text(json.dumps(payload, indent=2))
    (output / "support_ops.md").write_text(_render_markdown(payload))
    return payload


def _render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Support Ops Report",
        "",
        f"- Queue count: `{summary['queue_count']}`",
        f"- Incident bundles: `{summary['incident_count']}`",
        f"- Knowledge base entries: `{summary['knowledge_base_count']}`",
        f"- Escalated items: `{summary['escalated_count']}`",
        f"- Self-serve items: `{summary['self_serve_count']}`",
        f"- Incident coverage: `{summary['incident_coverage']:.3f}`",
        f"- Knowledge base coverage: `{summary['knowledge_base_coverage']:.3f}`",
        "",
        "## Severity Mix",
        "",
        "| severity | count |",
        "| --- | ---: |",
    ]
    for severity, count in sorted(payload["severity_counts"].items()):
        lines.append(f"| {severity} | {count} |")

    lines.extend(["", "## Owner Mix", "", "| owner | count |", "| --- | ---: |"])
    for owner, count in sorted(payload["owner_counts"].items()):
        lines.append(f"| {owner} | {count} |")
    return "\n".join(lines)
