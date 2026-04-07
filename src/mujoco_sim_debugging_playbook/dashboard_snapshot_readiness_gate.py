from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_readiness_gate(
    *,
    dashboard_snapshot_owner_load_path: str | Path,
    dashboard_snapshot_closeout_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    owner_load = _read_json(dashboard_snapshot_owner_load_path)
    closeout = _read_json(dashboard_snapshot_closeout_path)

    failures = []
    warnings = []

    if closeout["summary"]["closeout_status"] != "ready_to_close":
        failures.append("Closeout has not reached ready_to_close.")
    if owner_load["summary"]["critical_alert_count"] > 0:
        failures.append("Critical alert pressure remains active.")
    if owner_load["summary"]["planned_item_count"] > 1:
        warnings.append("Planned follow-up workload is still elevated.")

    status = "pass"
    if failures:
        status = "fail"
    elif warnings:
        status = "warn"

    payload = {
        "summary": {
            "status": status,
            "owner": owner_load["summary"]["owner"],
            "failure_count": len(failures),
            "warning_count": len(warnings),
            "current_status": owner_load["summary"]["current_status"],
        },
        "failures": failures,
        "warnings": warnings,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "readiness_gate.json").write_text(json.dumps(payload, indent=2))
    (output / "readiness_gate.md").write_text(render_dashboard_snapshot_readiness_gate_markdown(payload))
    return payload


def render_dashboard_snapshot_readiness_gate_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Readiness Gate",
        "",
        f"- Status: `{payload['summary']['status']}`",
        f"- Owner: `{payload['summary']['owner']}`",
        f"- Current status: `{payload['summary']['current_status']}`",
        f"- Failures: `{payload['summary']['failure_count']}`",
        f"- Warnings: `{payload['summary']['warning_count']}`",
        "",
        "## Failures",
        "",
    ]
    if payload["failures"]:
        for failure in payload["failures"]:
            lines.append(f"- {failure}")
    else:
        lines.append("- None")
    lines.extend(["", "## Warnings", ""])
    if payload["warnings"]:
        for warning in payload["warnings"]:
            lines.append(f"- {warning}")
    else:
        lines.append("- None")
    return "\n".join(lines)
