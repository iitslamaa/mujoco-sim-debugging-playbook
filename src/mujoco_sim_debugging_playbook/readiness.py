from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_support_readiness_report(
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

    payload = evaluate_support_readiness(
        support_ops=support_ops,
        support_gaps=support_gaps,
        sla=sla,
        capacity=capacity,
        release_notes=release_notes,
    )

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "support_readiness.json").write_text(json.dumps(payload, indent=2))
    (output / "support_readiness.md").write_text(_render_markdown(payload))
    return payload


def evaluate_support_readiness(
    *,
    support_ops: dict[str, Any],
    support_gaps: dict[str, Any],
    sla: dict[str, Any],
    capacity: dict[str, Any],
    release_notes: dict[str, Any],
) -> dict[str, Any]:

    checks = [
        _check_incident_coverage(support_ops),
        _check_kb_coverage(support_ops),
        _check_breaches(sla),
        _check_at_risk(sla),
        _check_overloaded_owners(capacity),
        _check_gap_backlog(support_gaps),
        _check_regression_gate(release_notes),
    ]
    failure_count = sum(1 for check in checks if check["status"] == "fail")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    status = "fail" if failure_count else "warn" if warning_count else "pass"

    payload = {
        "summary": {
            "status": status,
            "failure_count": failure_count,
            "warning_count": warning_count,
            "check_count": len(checks),
        },
        "checks": checks,
    }
    return payload


def _check_incident_coverage(support_ops: dict[str, Any]) -> dict[str, Any]:
    coverage = support_ops["summary"]["incident_coverage"]
    status = "pass" if coverage >= 0.5 else "warn"
    return {
        "name": "incident_coverage",
        "status": status,
        "value": coverage,
        "message": f"Incident coverage is {coverage * 100:.1f}% of the queue.",
    }


def _check_kb_coverage(support_ops: dict[str, Any]) -> dict[str, Any]:
    coverage = support_ops["summary"]["knowledge_base_coverage"]
    status = "pass" if coverage >= 0.5 else "warn"
    return {
        "name": "knowledge_base_coverage",
        "status": status,
        "value": coverage,
        "message": f"Knowledge-base coverage is {coverage * 100:.1f}% of the queue.",
    }


def _check_breaches(sla: dict[str, Any]) -> dict[str, Any]:
    breaches = sla["summary"]["breach_count"]
    status = "fail" if breaches > 0 else "pass"
    return {
        "name": "delivery_breaches",
        "status": status,
        "value": breaches,
        "message": f"{breaches} forecasted support items are in breach.",
    }


def _check_at_risk(sla: dict[str, Any]) -> dict[str, Any]:
    at_risk = sla["summary"]["at_risk_count"]
    status = "warn" if at_risk > 2 else "pass"
    return {
        "name": "delivery_at_risk",
        "status": status,
        "value": at_risk,
        "message": f"{at_risk} support items are forecasted as at risk.",
    }


def _check_overloaded_owners(capacity: dict[str, Any]) -> dict[str, Any]:
    overloaded = capacity["summary"]["overloaded_owner_count"]
    status = "warn" if overloaded > 0 else "pass"
    return {
        "name": "overloaded_owners",
        "status": status,
        "value": overloaded,
        "message": f"{overloaded} owners are currently overloaded.",
    }


def _check_gap_backlog(support_gaps: dict[str, Any]) -> dict[str, Any]:
    needs_follow_up = support_gaps["summary"]["needs_follow_up_count"]
    status = "warn" if needs_follow_up > 3 else "pass"
    return {
        "name": "gap_backlog",
        "status": status,
        "value": needs_follow_up,
        "message": f"{needs_follow_up} support gaps still need follow-up work.",
    }


def _check_regression_gate(release_notes: dict[str, Any]) -> dict[str, Any]:
    gate = release_notes["regression_gate"]
    status = "pass" if gate["status"] == "pass" else "fail"
    return {
        "name": "regression_gate",
        "status": status,
        "value": gate["status"],
        "message": f"Regression gate status is {gate['status']} with {gate['violation_count']} violations.",
    }


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Support Readiness Gate",
        "",
        f"- Status: `{payload['summary']['status']}`",
        f"- Failures: `{payload['summary']['failure_count']}`",
        f"- Warnings: `{payload['summary']['warning_count']}`",
        f"- Checks: `{payload['summary']['check_count']}`",
        "",
        "| check | status | message |",
        "| --- | --- | --- |",
    ]
    for check in payload["checks"]:
        lines.append(f"| {check['name']} | {check['status']} | {check['message']} |")
    return "\n".join(lines)
