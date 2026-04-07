from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_support_gap_report(
    *,
    triage_queue_path: str | Path,
    incidents_index_path: str | Path,
    knowledge_base_index_path: str | Path,
    escalation_matrix_path: str | Path,
    recommendations_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    triage = _read_json(triage_queue_path)
    incidents = _read_json(incidents_index_path)
    knowledge_base = _read_json(knowledge_base_index_path)
    escalation = _read_json(escalation_matrix_path)
    recommendations = _read_json(recommendations_path)

    incident_targets = {bundle["target"] for bundle in incidents["bundles"]}
    kb_targets = {entry["target"] for entry in knowledge_base["entries"]}
    escalation_lookup = {item["target"]: item for item in escalation["items"]}
    recommendation_targets = {item["target"] for item in recommendations["recommendations"]}

    items = []
    for triage_item in triage["items"]:
        target = triage_item["target"]
        escalation_item = escalation_lookup.get(target, {})
        has_incident = target in incident_targets
        has_kb = target in kb_targets
        has_escalation = target in escalation_lookup
        has_recommendation = target in recommendation_targets
        missing = []
        if not has_incident and triage_item["kind"] != "release_review":
            missing.append("incident_bundle")
        if not has_kb and triage_item["kind"] in {"benchmark_case", "randomized_episode"}:
            missing.append("knowledge_base_entry")
        if not has_recommendation and triage_item["kind"] != "release_review":
            missing.append("mitigation_recommendation")
        if not has_escalation:
            missing.append("escalation_mapping")

        coverage_score = (
            (2 if has_incident else 0)
            + (2 if has_kb else 0)
            + (1 if has_recommendation else 0)
            + (1 if has_escalation else 0)
        )
        gap_score = float(triage_item["priority_score"]) * (len(missing) + 1) / 6.0
        items.append(
            {
                "target": target,
                "kind": triage_item["kind"],
                "priority_score": float(triage_item["priority_score"]),
                "severity": escalation_item.get("severity", "unknown"),
                "owner": escalation_item.get("owner", "unassigned"),
                "has_incident_bundle": has_incident,
                "has_knowledge_base_entry": has_kb,
                "has_recommendation": has_recommendation,
                "has_escalation_mapping": has_escalation,
                "coverage_score": coverage_score,
                "gap_score": gap_score,
                "missing_artifacts": missing,
                "next_best_asset": _next_best_asset(missing, triage_item["kind"]),
            }
        )

    ordered = sorted(items, key=lambda item: (-item["gap_score"], -item["priority_score"], item["target"]))
    uncovered_critical = sum(
        1 for item in ordered if item["severity"] == "critical" and item["missing_artifacts"]
    )
    payload = {
        "summary": {
            "count": len(ordered),
            "fully_covered_count": sum(1 for item in ordered if not item["missing_artifacts"]),
            "needs_follow_up_count": sum(1 for item in ordered if item["missing_artifacts"]),
            "uncovered_critical_count": uncovered_critical,
            "top_gap_target": ordered[0]["target"] if ordered else None,
        },
        "items": ordered,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "support_gaps.json").write_text(json.dumps(payload, indent=2))
    (output / "support_gaps.md").write_text(_render_markdown(payload))
    return payload


def _next_best_asset(missing: list[str], kind: str) -> str:
    if "incident_bundle" in missing:
        return "Capture a reproducible incident bundle with traces and supporting evidence."
    if "knowledge_base_entry" in missing:
        return "Promote the validated mitigation into a self-serve knowledge-base article."
    if "mitigation_recommendation" in missing:
        return "Add a concrete mitigation recommendation tied to sweep or benchmark evidence."
    if "escalation_mapping" in missing:
        return "Assign an owner and escalation path before the item enters the shared queue."
    if kind == "release_review":
        return "No gap detected; keep the release review in the audit trail."
    return "No immediate follow-up needed."


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Support Coverage Gaps",
        "",
        f"- Open triage items: `{payload['summary']['count']}`",
        f"- Fully covered items: `{payload['summary']['fully_covered_count']}`",
        f"- Items needing follow-up: `{payload['summary']['needs_follow_up_count']}`",
        f"- Critical items missing coverage: `{payload['summary']['uncovered_critical_count']}`",
        f"- Top gap target: `{payload['summary']['top_gap_target']}`",
        "",
        "| gap_score | severity | target | missing_artifacts | next_best_asset |",
        "| ---: | --- | --- | --- | --- |",
    ]
    for item in payload["items"]:
        lines.append(
            f"| {item['gap_score']:.2f} | {item['severity']} | {item['target']} | "
            f"{', '.join(item['missing_artifacts']) or '--'} | {item['next_best_asset']} |"
        )

    lines.extend(["", "## Coverage Detail", ""])
    for item in payload["items"]:
        coverage = (
            f"incident={item['has_incident_bundle']}, kb={item['has_knowledge_base_entry']}, "
            f"recommendation={item['has_recommendation']}, escalation={item['has_escalation_mapping']}"
        )
        lines.append(f"- `{item['target']}`: {coverage}")
    return "\n".join(lines)
