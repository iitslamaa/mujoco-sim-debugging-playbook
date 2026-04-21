from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.earthmoving import EarthmovingSimulation, load_earthmoving_config, result_to_dict, scenario_from_dict
from mujoco_sim_debugging_playbook.provenance import write_manifest


def build_earthmoving_replay_bundle(
    *,
    config_path: str | Path,
    scenario_name: str,
    output_dir: str | Path,
) -> dict[str, Any]:
    config = load_earthmoving_config(config_path)
    scenario_payload = next((item for item in config["scenarios"] if item["name"] == scenario_name), None)
    if scenario_payload is None:
        raise ValueError(f"unknown earthmoving scenario: {scenario_name}")

    scenario = scenario_from_dict(scenario_payload)
    result = EarthmovingSimulation(scenario).run()
    result_payload = result_to_dict(result)
    bundle = {
        "scenario": scenario_name,
        "metrics": result_payload["metrics"],
        "soil": scenario_payload["soil"],
        "blade": scenario_payload["blade"],
        "target": scenario_payload["target"],
        "blade_path": result_payload["blade_path"],
        "terrain_stats": {
            "initial": _terrain_stats(result_payload["initial_terrain"]),
            "final": _terrain_stats(result_payload["final_terrain"]),
            "target": _terrain_stats(result_payload["target_terrain"]),
        },
        "debug_hypotheses": _debug_hypotheses(result_payload["metrics"], scenario_payload["soil"]),
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    bundle_path = output / f"{scenario_name}_replay.json"
    note_path = output / f"{scenario_name}_replay.md"
    bundle_path.write_text(json.dumps(bundle, indent=2))
    note_path.write_text(render_replay_markdown(bundle))
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="earthmoving_replay",
        config={"config_path": str(config_path), "scenario_name": scenario_name},
        inputs=[config_path],
        outputs=[bundle_path, note_path],
        metadata={"scenario": scenario_name, **bundle["metrics"]},
    )
    return bundle


def render_replay_markdown(bundle: dict[str, Any]) -> str:
    metrics = bundle["metrics"]
    lines = [
        f"# Earthmoving Replay: {bundle['scenario']}",
        "",
        "## Metrics",
        "",
        f"- Moved volume: `{metrics['moved_volume']:.6f}`",
        f"- Terrain profile RMSE: `{metrics['terrain_profile_rmse']:.6f}`",
        f"- Volume conservation error: `{metrics['volume_conservation_error']:.6f}`",
        f"- Runtime: `{metrics['runtime_s']:.5f}`",
        "",
        "## Terrain Stats",
        "",
        "| surface | min | max | mean | volume |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for name, stats in bundle["terrain_stats"].items():
        lines.append(
            f"| {name} | {stats['min_height']:.6f} | {stats['max_height']:.6f} | "
            f"{stats['mean_height']:.6f} | {stats['volume']:.6f} |"
        )
    lines.extend(["", "## Debug Hypotheses", ""])
    for item in bundle["debug_hypotheses"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


def _terrain_stats(terrain: dict[str, Any]) -> dict[str, float]:
    heights = [height for row in terrain["heights"] for height in row]
    return {
        "min_height": min(heights),
        "max_height": max(heights),
        "mean_height": sum(heights) / len(heights),
        "volume": float(terrain["volume"]),
    }


def _debug_hypotheses(metrics: dict[str, float], soil: dict[str, float]) -> list[str]:
    hypotheses = []
    if metrics["moved_volume"] < 0.0008:
        hypotheses.append("Low moved volume: inspect blade depth, coupling, and soil resistance parameters.")
    if metrics["terrain_profile_rmse"] > 0.04:
        hypotheses.append("High target-profile error: tune deposit spread and validate target berm geometry.")
    if metrics["volume_conservation_error"] > 0.00025:
        hypotheses.append("Volume residual is elevated: check compaction assumptions and spillover distribution.")
    if soil["cohesion"] > 0.3:
        hypotheses.append("Cohesive soil scenario: expect reduced cutting efficiency and stronger calibration dependence.")
    if not hypotheses:
        hypotheses.append("Replay is within nominal debug thresholds; use as a reference case.")
    return hypotheses
