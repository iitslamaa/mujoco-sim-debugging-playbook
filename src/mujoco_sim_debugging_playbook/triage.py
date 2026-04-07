from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def build_triage_queue(
    *,
    anomaly_report_path: str | Path,
    recommendation_report_path: str | Path,
    regression_gate_path: str | Path,
    release_notes_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    anomalies = _read_json(anomaly_report_path)
    recommendations = _read_json(recommendation_report_path)
    gate = _read_json(regression_gate_path)
    release_notes = _read_json(release_notes_path)

    queue = []
    rec_lookup = {item["target"]: item for item in recommendations["recommendations"]}

    for case in anomalies["benchmark_anomalies"]["top_cases"][:5]:
        target = f"{case['scenario']} / {case['controller']}"
        recommendation = rec_lookup.get(target)
        queue.append(
            {
                "kind": "benchmark_case",
                "priority_score": float(50 + 100 * case["risk_score"]),
                "target": target,
                "summary": f"Elevated benchmark risk in `{case['scenario']}` for `{case['controller']}`.",
                "evidence": f"Risk score `{case['risk_score']:.4f}`, final error `{case['final_error_mean']:.4f}`.",
                "next_action": recommendation["recommendation"] if recommendation else "Reproduce and compare traces against the best-performing controller.",
            }
        )

    for episode in anomalies["randomization_anomalies"]["episodes"][:5]:
        target = f"episode {episode['episode']}"
        recommendation = rec_lookup.get(target)
        queue.append(
            {
                "kind": "randomized_episode",
                "priority_score": float(100 + 100 * episode["difficulty_score"]),
                "target": target,
                "summary": f"Hard randomized episode with worst controller `{episode['worst_controller']}`.",
                "evidence": (
                    f"Difficulty `{episode['difficulty_score']:.4f}`, success `{episode['success_rate']:.3f}`, "
                    f"delay `{episode['control_delay_steps']}`, noise `{episode['sensor_noise_std']:.4f}`."
                ),
                "next_action": recommendation["recommendation"] if recommendation else "Replay the episode conditions and compare controller outputs.",
            }
        )

    if gate["status"] != "pass":
        queue.append(
            {
                "kind": "regression_gate",
                "priority_score": 250.0,
                "target": "regression gate",
                "summary": "Regression thresholds are currently failing.",
                "evidence": f"Violations: {gate['violation_count']}",
                "next_action": "Inspect the triggered metric deltas and compare the latest snapshots before landing more changes.",
            }
        )

    queue.append(
        {
            "kind": "release_review",
            "priority_score": float(20 + 5 * release_notes["commit_count"]),
            "target": f"{release_notes['base_ref']} -> {release_notes['head_ref']}",
            "summary": "Recent change range to review from a support and release perspective.",
            "evidence": f"{release_notes['diffstat'] or 'n/a'}",
            "next_action": "Check changed areas with the highest file counts first and confirm docs, CI, and artifacts stayed aligned.",
        }
    )

    ordered = sorted(queue, key=lambda item: item["priority_score"], reverse=True)
    payload = {
        "items": ordered,
        "summary": {
            "count": len(ordered),
            "top_priority": ordered[0]["target"] if ordered else None,
            "regression_gate_status": gate["status"],
        },
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "triage_queue.json").write_text(json.dumps(payload, indent=2))
    _write_markdown(payload, output / "triage_queue.md")
    return payload


def _write_markdown(payload: dict[str, Any], path: str | Path) -> None:
    lines = [
        "# Support Triage Queue",
        "",
        f"Open triage items: `{payload['summary']['count']}`",
        "",
        f"Top priority: `{payload['summary']['top_priority']}`",
        "",
        "| priority_score | kind | target | summary | next_action |",
        "| ---: | --- | --- | --- | --- |",
    ]
    for item in payload["items"]:
        lines.append(
            f"| {item['priority_score']:.2f} | {item['kind']} | {item['target']} | {item['summary']} | {item['next_action']} |"
        )

    lines.extend(["", "## Evidence", ""])
    for item in payload["items"]:
        lines.append(f"- `{item['target']}`: {item['evidence']}")

    Path(path).write_text("\n".join(lines))
