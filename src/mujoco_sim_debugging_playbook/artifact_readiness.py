from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _status_for(ok: bool, warning: bool) -> str:
    if not ok:
        return "fail"
    if warning:
        return "warn"
    return "pass"


def build_artifact_readiness(
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

    fresh_summary = freshness["summary"]
    risk_summary = maintenance_risk["summary"]
    checklist_summary = refresh_checklist["summary"]
    regen_summary = regeneration_plan["summary"]

    checks = []

    missing_ok = fresh_summary["missing_count"] == 0
    checks.append(
        {
            "name": "missing_artifacts",
            "status": _status_for(missing_ok, False),
            "message": f"{fresh_summary['missing_count']} missing artifacts",
        }
    )

    high_risk_ok = risk_summary["high_risk_count"] == 0
    high_risk_warning = risk_summary["high_risk_count"] == 1
    checks.append(
        {
            "name": "high_risk_artifacts",
            "status": _status_for(high_risk_ok, high_risk_warning),
            "message": f"{risk_summary['high_risk_count']} high-risk artifacts",
        }
    )

    top_risk_ok = risk_summary["top_risk_score"] < 1.5
    top_risk_warning = 1.2 <= risk_summary["top_risk_score"] < 1.5
    checks.append(
        {
            "name": "top_risk_score",
            "status": _status_for(top_risk_ok, top_risk_warning),
            "message": (
                f"top risk {risk_summary['top_risk_artifact'] or 'n/a'} "
                f"at {risk_summary['top_risk_score']:.3f}"
            ),
        }
    )

    backlog_ok = fresh_summary["stale_count"] <= 2
    backlog_warning = 3 <= fresh_summary["stale_count"] <= 5
    checks.append(
        {
            "name": "stale_backlog",
            "status": _status_for(backlog_ok, backlog_warning),
            "message": f"{fresh_summary['stale_count']} stale artifacts",
        }
    )

    refresh_ok = checklist_summary["total_steps"] <= 3
    refresh_warning = 4 <= checklist_summary["total_steps"] <= 5
    checks.append(
        {
            "name": "refresh_effort",
            "status": _status_for(refresh_ok, refresh_warning),
            "message": f"{checklist_summary['total_steps']} refresh steps across {checklist_summary['bundle_count']} bundles",
        }
    )

    priority_ok = regen_summary["high_priority_count"] == 0
    priority_warning = regen_summary["high_priority_count"] == 1
    checks.append(
        {
            "name": "high_priority_refreshes",
            "status": _status_for(priority_ok, priority_warning),
            "message": f"{regen_summary['high_priority_count']} high-priority refresh actions",
        }
    )

    failure_count = sum(1 for check in checks if check["status"] == "fail")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    overall_status = "fail" if failure_count else "warn" if warning_count else "pass"

    return {
        "summary": {
            "status": overall_status,
            "failure_count": failure_count,
            "warning_count": warning_count,
            "top_risk_artifact": risk_summary["top_risk_artifact"],
            "stale_count": fresh_summary["stale_count"],
            "refresh_step_count": checklist_summary["total_steps"],
        },
        "checks": checks,
    }


def render_artifact_readiness_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Artifact Readiness",
        "",
        f"- Status: `{payload['summary']['status']}`",
        f"- Failures: `{payload['summary']['failure_count']}`",
        f"- Warnings: `{payload['summary']['warning_count']}`",
        f"- Top risk artifact: `{payload['summary']['top_risk_artifact']}`",
        f"- Stale artifacts: `{payload['summary']['stale_count']}`",
        f"- Refresh steps: `{payload['summary']['refresh_step_count']}`",
        "",
        "| check | status | message |",
        "| --- | --- | --- |",
    ]
    for check in payload["checks"]:
        lines.append(f"| {check['name']} | {check['status']} | {check['message']} |")
    return "\n".join(lines)


def write_artifact_readiness(
    *,
    artifact_freshness_path: str | Path,
    maintenance_risk_path: str | Path,
    refresh_checklist_path: str | Path,
    regeneration_plan_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    payload = build_artifact_readiness(
        artifact_freshness_path=artifact_freshness_path,
        maintenance_risk_path=maintenance_risk_path,
        refresh_checklist_path=refresh_checklist_path,
        regeneration_plan_path=regeneration_plan_path,
    )
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact_readiness.json").write_text(json.dumps(payload, indent=2))
    (output / "artifact_readiness.md").write_text(render_artifact_readiness_markdown(payload))
    return payload
