from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.earthmoving import BladePlan, EarthmovingSimulation, load_earthmoving_config, scenario_from_dict
from mujoco_sim_debugging_playbook.provenance import write_manifest


def search_earthmoving_blade_plan(
    *,
    config_path: str | Path,
    scenario_name: str,
    output_dir: str | Path,
    depth_values: list[float] | None = None,
    width_values: list[float] | None = None,
    y_offsets: list[float] | None = None,
) -> dict[str, Any]:
    config = load_earthmoving_config(config_path)
    scenario_payload = next((item for item in config["scenarios"] if item["name"] == scenario_name), None)
    if scenario_payload is None:
        raise ValueError(f"unknown earthmoving scenario: {scenario_name}")
    scenario = scenario_from_dict(scenario_payload)
    depth_values = depth_values or [0.008, 0.012, 0.016, 0.02, 0.024]
    width_values = width_values or [0.16, 0.2, 0.24]
    y_offsets = y_offsets or [-0.04, 0.0, 0.04]

    rows = []
    for depth in depth_values:
        for width in width_values:
            for offset in y_offsets:
                blade = BladePlan(
                    start_x=scenario.blade.start_x,
                    end_x=scenario.blade.end_x,
                    y=scenario.blade.y + offset,
                    yaw=scenario.blade.yaw,
                    width=width,
                    depth=depth,
                    steps=scenario.blade.steps,
                )
                candidate = replace(scenario, name=f"{scenario.name}_d{depth:.3f}_w{width:.2f}_y{offset:+.2f}", blade=blade)
                result = EarthmovingSimulation(candidate).run()
                score = _score(result.metrics)
                rows.append(
                    {
                        "candidate": candidate.name,
                        "depth": depth,
                        "width": width,
                        "y": blade.y,
                        "score": score,
                        "moved_volume": result.metrics.moved_volume,
                        "terrain_profile_rmse": result.metrics.terrain_profile_rmse,
                        "volume_conservation_error": result.metrics.volume_conservation_error,
                        "runtime_s": result.metrics.runtime_s,
                    }
                )
    rows.sort(key=lambda item: item["score"])
    payload = {
        "summary": {
            "scenario": scenario_name,
            "candidate_count": len(rows),
            "best_candidate": rows[0],
            "baseline": _baseline_row(scenario),
        },
        "rows": rows,
    }
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    summary_path = output / "plan_search.json"
    report_path = output / "report.md"
    summary_path.write_text(json.dumps(payload, indent=2))
    _write_report(payload, report_path)
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="earthmoving_plan_search",
        config={"config_path": str(config_path), "scenario_name": scenario_name},
        inputs=[config_path],
        outputs=[summary_path, report_path],
        metadata=payload["summary"],
    )
    return payload


def _baseline_row(scenario: Any) -> dict[str, float | str]:
    result = EarthmovingSimulation(scenario).run()
    return {
        "candidate": scenario.name,
        "depth": scenario.blade.depth,
        "width": scenario.blade.width,
        "y": scenario.blade.y,
        "score": _score(result.metrics),
        "moved_volume": result.metrics.moved_volume,
        "terrain_profile_rmse": result.metrics.terrain_profile_rmse,
        "volume_conservation_error": result.metrics.volume_conservation_error,
        "runtime_s": result.metrics.runtime_s,
    }


def _score(metrics: Any) -> float:
    return (
        metrics.terrain_profile_rmse
        + 8.0 * metrics.volume_conservation_error
        - 0.35 * metrics.moved_volume
        + 0.002 * metrics.runtime_s
    )


def _write_report(payload: dict[str, Any], output_path: Path) -> None:
    best = payload["summary"]["best_candidate"]
    baseline = payload["summary"]["baseline"]
    lines = [
        "# Earthmoving Blade Plan Search",
        "",
        f"Scenario: `{payload['summary']['scenario']}`",
        f"Candidates: `{payload['summary']['candidate_count']}`",
        f"Best candidate: `{best['candidate']}`",
        f"Best score: `{best['score']:.6f}`",
        f"Baseline score: `{baseline['score']:.6f}`",
        "",
        "| candidate | score | depth | width | y | moved_volume | terrain_rmse | volume_error |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in payload["rows"][:12]:
        lines.append(
            f"| {row['candidate']} | {row['score']:.6f} | {row['depth']:.3f} | {row['width']:.2f} | "
            f"{row['y']:.3f} | {row['moved_volume']:.6f} | {row['terrain_profile_rmse']:.6f} | "
            f"{row['volume_conservation_error']:.6f} |"
        )
    output_path.write_text("\n".join(lines))
