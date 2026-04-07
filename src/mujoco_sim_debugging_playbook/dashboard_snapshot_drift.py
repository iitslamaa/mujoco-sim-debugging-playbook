from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_dashboard_snapshot_drift(
    *,
    dashboard_snapshot_history_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    history = _read_json(dashboard_snapshot_history_path)
    snapshots = history.get("snapshots", [])

    transitions: list[dict[str, Any]] = []
    first_pass_snapshot = None

    for index, snapshot in enumerate(snapshots):
        if snapshot["status"] == "pass" and first_pass_snapshot is None:
            first_pass_snapshot = snapshot["name"]
        if index == 0:
            continue

        previous = snapshots[index - 1]
        current = snapshot
        failure_delta = current["failure_count"] - previous["failure_count"]
        risk_delta = current["top_risk_score"] - previous["top_risk_score"]
        success_delta = current["baseline_success_rate"] - previous["baseline_success_rate"]

        transitions.append(
            {
                "from": previous["name"],
                "to": current["name"],
                "from_status": previous["status"],
                "to_status": current["status"],
                "failure_delta": failure_delta,
                "risk_delta": risk_delta,
                "baseline_success_rate_delta": success_delta,
                "status_changed": current["status"] != previous["status"],
                "improved_failures": failure_delta < 0,
                "improved_risk": risk_delta < 0,
            }
        )

    largest_failure_drop = min(transitions, key=lambda item: item["failure_delta"], default=None)
    largest_risk_drop = min(transitions, key=lambda item: item["risk_delta"], default=None)

    payload = {
        "summary": {
            "transition_count": len(transitions),
            "first_pass_snapshot": first_pass_snapshot,
            "largest_failure_drop_transition": (
                f"{largest_failure_drop['from']} -> {largest_failure_drop['to']}"
                if largest_failure_drop
                else None
            ),
            "largest_failure_drop": (
                abs(largest_failure_drop["failure_delta"]) if largest_failure_drop else 0
            ),
            "largest_risk_drop_transition": (
                f"{largest_risk_drop['from']} -> {largest_risk_drop['to']}"
                if largest_risk_drop
                else None
            ),
            "largest_risk_drop": (
                abs(largest_risk_drop["risk_delta"]) if largest_risk_drop else 0.0
            ),
        },
        "transitions": transitions,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "drift.json").write_text(json.dumps(payload, indent=2))
    (output / "drift.md").write_text(render_dashboard_snapshot_drift_markdown(payload))
    return payload


def render_dashboard_snapshot_drift_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Snapshot Drift",
        "",
        f"- Transitions: `{payload['summary']['transition_count']}`",
        f"- First pass snapshot: `{payload['summary']['first_pass_snapshot']}`",
        f"- Largest failure drop: `{payload['summary']['largest_failure_drop_transition']}` "
        f"(`{payload['summary']['largest_failure_drop']}`)",
        f"- Largest risk drop: `{payload['summary']['largest_risk_drop_transition']}` "
        f"(`{payload['summary']['largest_risk_drop']:.3f}`)",
        "",
        "| from | to | status | failure_delta | risk_delta | baseline_success_rate_delta |",
        "| --- | --- | --- | ---: | ---: | ---: |",
    ]
    for transition in payload["transitions"]:
        lines.append(
            f"| {transition['from']} | {transition['to']} | "
            f"{transition['from_status']} -> {transition['to_status']} | "
            f"{transition['failure_delta']} | "
            f"{transition['risk_delta']:.3f} | "
            f"{transition['baseline_success_rate_delta']:.3f} |"
        )
    return "\n".join(lines)
