from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.provenance import write_manifest


def build_earthmoving_role_brief(
    *,
    review_packet_path: str | Path,
    dataset_summary_path: str | Path,
    failure_modes_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    review = _read_json(review_packet_path)
    dataset = _read_json(dataset_summary_path)
    failure_modes = _read_json(failure_modes_path)
    summary = review["summary"]
    payload = {
        "headline": "Construction-machine simulation track with deformable terrain, calibration, scale, and debug artifacts.",
        "fit_signals": [
            "Built a MuJoCo dozer/blade task instead of only toy robot control.",
            "Implemented heightmap terrain deformation with soil parameters and volume accounting.",
            "Mapped simulation outputs to deployment-style productivity, cycle-time, placement, and rework-risk decisions.",
            "Added sim-to-field calibration against observed construction-style logs.",
            "Generated randomized scale runs and throughput metrics for batch evaluation.",
            "Created ML-ready feature/label datasets for learned evaluators or surrogate models.",
            "Added C++ terrain-kernel smoke coverage for low-level geometry/physics implementation.",
            "Packaged failure replay, quality gates, dashboards, and review packets like production simulation infrastructure.",
        ],
        "metrics": {
            "gate_status": summary["gate_status"],
            "scenario_count": summary["scenario_count"],
            "scale_episode_count": summary["scale_episode_count"],
            "episodes_per_second": summary["episodes_per_second"],
            "dataset_rows": dataset["summary"]["row_count"],
            "failure_mode_items": failure_modes["summary"]["item_count"],
            "mean_calibration_error": summary["mean_calibration_error"],
            "jobsite_decision": summary.get("jobsite_decision", "not_evaluated"),
            "mean_productivity_m3_per_hr": summary.get("mean_productivity_m3_per_hr", 0.0),
        },
        "talking_points": _talking_points(summary, dataset, failure_modes),
    }
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    brief_path = output / "role_brief.json"
    markdown_path = output / "role_brief.md"
    brief_path.write_text(json.dumps(payload, indent=2))
    markdown_path.write_text(_write_markdown(payload))
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="earthmoving_role_brief",
        config={
            "review_packet": str(review_packet_path),
            "dataset_summary": str(dataset_summary_path),
            "failure_modes": str(failure_modes_path),
        },
        inputs=[review_packet_path, dataset_summary_path, failure_modes_path],
        outputs=[brief_path, markdown_path],
        metadata=payload["metrics"],
    )
    return payload


def _talking_points(summary: dict[str, Any], dataset: dict[str, Any], failure_modes: dict[str, Any]) -> list[str]:
    top_mode = failure_modes["summary"]["top_mode"]
    return [
        f"The current earthmoving gate is `{summary['gate_status']}`, so the track has release-style pass/fail semantics.",
        f"The scale harness ran `{summary['scale_episode_count']}` randomized episodes at `{summary['episodes_per_second']:.2f}` episodes/s.",
        f"The generated dataset has `{dataset['summary']['row_count']}` rows with `{len(dataset['summary']['feature_names'])}` features and `{len(dataset['summary']['label_names'])}` labels.",
        f"The failure-mode queue currently prioritizes `{top_mode}` as the highest-ranked debugging theme.",
    ]


def _write_markdown(payload: dict[str, Any]) -> str:
    metrics = payload["metrics"]
    lines = [
        "# Earthmoving Simulation Role Brief",
        "",
        payload["headline"],
        "",
        "## Fit Signals",
        "",
    ]
    for item in payload["fit_signals"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Metrics",
            "",
            f"- Gate status: `{metrics['gate_status']}`",
            f"- Scenarios: `{metrics['scenario_count']}`",
            f"- Scale episodes: `{metrics['scale_episode_count']}`",
            f"- Throughput: `{metrics['episodes_per_second']:.2f}` episodes/s",
            f"- Dataset rows: `{metrics['dataset_rows']}`",
            f"- Failure-mode items: `{metrics['failure_mode_items']}`",
            f"- Mean calibration error: `{metrics['mean_calibration_error']:.4f}`",
            f"- Jobsite decision: `{metrics['jobsite_decision']}`",
            f"- Mean scaled productivity: `{metrics['mean_productivity_m3_per_hr']:.2f}` m3/hr",
            "",
            "## Talking Points",
            "",
        ]
    )
    for item in payload["talking_points"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())
