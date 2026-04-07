from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_ops_review(
    *,
    support_ops_path: str | Path,
    support_gaps_path: str | Path,
    sla_report_path: str | Path,
    capacity_plan_path: str | Path,
    release_notes_path: str | Path,
    anomaly_report_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    support_ops = _read_json(support_ops_path)
    support_gaps = _read_json(support_gaps_path)
    sla = _read_json(sla_report_path)
    capacity = _read_json(capacity_plan_path)
    release_notes = _read_json(release_notes_path)
    anomalies = _read_json(anomaly_report_path)

    top_gap = support_gaps["summary"]["top_gap_target"]
    highest_pressure_lane = capacity["summary"]["highest_pressure_lane"]
    overloaded_owner = capacity["owners"][0]["owner"] if capacity["owners"] else None
    top_anomaly = anomalies["benchmark_anomalies"]["top_cases"][0] if anomalies["benchmark_anomalies"]["top_cases"] else None

    wins = [
        f"Knowledge base coverage is {support_ops['summary']['knowledge_base_coverage'] * 100:.1f}% of the open queue.",
        f"The triage system has {support_ops['summary']['incident_count']} incident bundles and {support_ops['summary']['knowledge_base_count']} knowledge-base entries ready for reuse.",
        f"Regression gate status remains `{release_notes['regression_gate']['status']}` across the latest release range.",
    ]

    risks = [
        f"{sla['summary']['breach_count']} items are already in breach and {sla['summary']['at_risk_count']} more are at risk.",
        f"The highest-pressure lane is `{highest_pressure_lane}` and the most overloaded owner is `{overloaded_owner}`.",
        f"The top uncovered support gap is `{top_gap}`.",
    ]
    if top_anomaly:
        risks.append(
            f"The riskiest benchmark scenario remains `{top_anomaly['scenario']} / {top_anomaly['controller']}` "
            f"with risk score `{top_anomaly['risk_score']:.3f}`."
        )

    next_actions = []
    for item in capacity["rebalance_items"][:3]:
        next_actions.append(
            {
                "target": item["target"],
                "owner": item["recommended_owner"],
                "action": item["recommended_action"],
                "reason": item["handoff_reason"],
            }
        )

    payload = {
        "summary": {
            "queue_count": support_ops["summary"]["queue_count"],
            "incident_coverage": support_ops["summary"]["incident_coverage"],
            "knowledge_base_coverage": support_ops["summary"]["knowledge_base_coverage"],
            "breach_count": sla["summary"]["breach_count"],
            "at_risk_count": sla["summary"]["at_risk_count"],
            "highest_pressure_lane": highest_pressure_lane,
            "overloaded_owner": overloaded_owner,
            "top_gap_target": top_gap,
            "release_commit_count": release_notes["commit_count"],
        },
        "wins": wins,
        "risks": risks,
        "next_actions": next_actions,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "ops_review.json").write_text(json.dumps(payload, indent=2))
    (output / "ops_review.md").write_text(_render_markdown(payload))
    return payload


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Support Ops Review",
        "",
        f"- Queue count: `{payload['summary']['queue_count']}`",
        f"- Incident coverage: `{payload['summary']['incident_coverage'] * 100:.1f}%`",
        f"- Knowledge base coverage: `{payload['summary']['knowledge_base_coverage'] * 100:.1f}%`",
        f"- Breaches: `{payload['summary']['breach_count']}`",
        f"- At risk: `{payload['summary']['at_risk_count']}`",
        f"- Highest-pressure lane: `{payload['summary']['highest_pressure_lane']}`",
        f"- Overloaded owner: `{payload['summary']['overloaded_owner']}`",
        f"- Top gap: `{payload['summary']['top_gap_target']}`",
        "",
        "## Wins",
        "",
    ]
    for win in payload["wins"]:
        lines.append(f"- {win}")

    lines.extend(["", "## Risks", ""])
    for risk in payload["risks"]:
        lines.append(f"- {risk}")

    lines.extend(["", "## Next Actions", "", "| target | owner | action | reason |", "| --- | --- | --- | --- |"])
    for item in payload["next_actions"]:
        lines.append(
            f"| {item['target']} | {item['owner']} | {item['action']} | {item['reason']} |"
        )
    return "\n".join(lines)
