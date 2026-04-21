from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np

from mujoco_sim_debugging_playbook.earthmoving import load_earthmoving_config, scenario_from_dict
from mujoco_sim_debugging_playbook.multipass_plan_eval import _evaluate_sequence
from mujoco_sim_debugging_playbook.provenance import write_manifest
from mujoco_sim_debugging_playbook.terrain import SoilConfig


def build_task_plan_robustness(
    *,
    benchmark_config_path: str | Path,
    jobsite_config_path: str | Path,
    scenario_name: str,
    output_dir: str | Path,
    seed: int = 13,
    episodes: int = 36,
) -> dict[str, Any]:
    config = load_earthmoving_config(benchmark_config_path)
    jobsite = _read_json(jobsite_config_path)
    scenario_payload = next((item for item in config["scenarios"] if item["name"] == scenario_name), None)
    if scenario_payload is None:
        raise ValueError(f"unknown earthmoving scenario: {scenario_name}")
    scenario = scenario_from_dict(scenario_payload)
    machine = jobsite["machine_profile"]
    targets = jobsite["targets"]
    plan = replace(
        scenario.blade,
        y=scenario.blade.y,
        depth=scenario.blade.depth * 0.45,
        width=scenario.blade.width * 1.28,
    )
    rng = np.random.default_rng(seed)
    rows = []
    for index in range(episodes):
        varied = replace(
            scenario,
            name=f"{scenario.name}_robust_{index:03d}",
            soil=_varied_soil(scenario.soil, rng),
        )
        machine_variant = _varied_machine(machine, rng)
        row = _evaluate_sequence("single_pass_wide_cut", varied, [plan], machine_variant, targets)
        row["episode"] = index
        row["soil"] = varied.soil.__dict__
        row["machine_variant"] = {
            "blade_speed_mps": machine_variant["blade_speed_mps"],
            "return_speed_mps": machine_variant["return_speed_mps"],
            "turnaround_s": machine_variant["turnaround_s"],
            "dump_settle_s": machine_variant["dump_settle_s"],
        }
        rows.append(row)

    payload = {
        "scenario": scenario_name,
        "candidate": "single_pass_wide_cut",
        "summary": _summary(rows, targets),
        "rows": rows,
        "recommendation": _recommendation(rows, targets),
    }
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "task_plan_robustness.json"
    md_path = output / "task_plan_robustness.md"
    json_path.write_text(json.dumps(payload, indent=2))
    md_path.write_text(render_task_plan_robustness(payload))
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="task_plan_robustness",
        config={"scenario": scenario_name, "seed": seed, "episodes": episodes},
        inputs=[benchmark_config_path, jobsite_config_path],
        outputs=[json_path, md_path],
        metadata=payload["summary"],
    )
    return payload


def render_task_plan_robustness(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Task Plan Robustness Sweep",
        "",
        f"Scenario: `{payload['scenario']}`",
        f"Candidate: `{payload['candidate']}`",
        "",
        "## Summary",
        "",
        f"- Episodes: `{summary['episode_count']}`",
        f"- Pass rate: `{summary['pass_rate']:.2%}`",
        f"- Mean productivity: `{summary['mean_productivity_m3_per_hr']:.2f}` m3/hr",
        f"- P10 productivity: `{summary['p10_productivity_m3_per_hr']:.2f}` m3/hr",
        f"- Worst productivity: `{summary['worst_productivity_m3_per_hr']:.2f}` m3/hr",
        f"- Mean target capture: `{summary['mean_target_capture_ratio']:.3f}`",
        f"- Worst failed check: `{summary['top_failed_check']}`",
        "",
        "## Worst Episodes",
        "",
        "| episode | decision | productivity_m3_hr | target_capture | terrain_rmse | failed_checks |",
        "| ---: | --- | ---: | ---: | ---: | --- |",
    ]
    for row in sorted(payload["rows"], key=lambda item: item["productivity_m3_per_hr"])[:8]:
        lines.append(
            f"| {row['episode']} | {row['decision']} | {row['productivity_m3_per_hr']:.2f} | "
            f"{row['target_capture_ratio']:.3f} | {row['terrain_profile_rmse']:.6f} | "
            f"{', '.join(row['failed_checks']) or 'none'} |"
        )
    lines.extend(["", "## Recommendation", "", payload["recommendation"]])
    return "\n".join(lines)


def _varied_soil(soil: SoilConfig, rng: np.random.Generator) -> SoilConfig:
    def scale(value: float, variation: float) -> float:
        return float(value * rng.uniform(1.0 - variation, 1.0 + variation))

    return SoilConfig(
        cohesion=max(0.0, scale(soil.cohesion, 0.18)),
        friction_angle_deg=float(np.clip(scale(soil.friction_angle_deg, 0.10), 18.0, 46.0)),
        compaction_rate=float(np.clip(scale(soil.compaction_rate, 0.25), 0.0, 0.6)),
        blade_coupling=float(np.clip(scale(soil.blade_coupling, 0.14), 0.1, 1.0)),
        spillover_rate=float(np.clip(scale(soil.spillover_rate, 0.25), 0.0, 0.8)),
    )


def _varied_machine(machine: dict[str, Any], rng: np.random.Generator) -> dict[str, Any]:
    variant = dict(machine)
    variant["blade_speed_mps"] = float(machine["blade_speed_mps"] * rng.uniform(0.88, 1.08))
    variant["return_speed_mps"] = float(machine["return_speed_mps"] * rng.uniform(0.9, 1.12))
    variant["turnaround_s"] = float(machine["turnaround_s"] * rng.uniform(0.9, 1.2))
    variant["dump_settle_s"] = float(machine["dump_settle_s"] * rng.uniform(0.85, 1.25))
    return variant


def _summary(rows: list[dict[str, Any]], targets: dict[str, float]) -> dict[str, Any]:
    productivities = np.asarray([row["productivity_m3_per_hr"] for row in rows], dtype=float)
    captures = np.asarray([row["target_capture_ratio"] for row in rows], dtype=float)
    failed_checks = [check for row in rows for check in row["failed_checks"]]
    top_failed = max(set(failed_checks), key=failed_checks.count) if failed_checks else "none"
    pass_count = sum(row["decision"] == "release_candidate" for row in rows)
    return {
        "episode_count": len(rows),
        "pass_count": pass_count,
        "pass_rate": pass_count / max(len(rows), 1),
        "mean_productivity_m3_per_hr": float(np.mean(productivities)),
        "p10_productivity_m3_per_hr": float(np.percentile(productivities, 10)),
        "worst_productivity_m3_per_hr": float(np.min(productivities)),
        "mean_target_capture_ratio": float(np.mean(captures)),
        "top_failed_check": top_failed,
        "target_productivity_m3_per_hr": targets["min_productivity_m3_per_hr"],
    }


def _recommendation(rows: list[dict[str, Any]], targets: dict[str, float]) -> str:
    summary = _summary(rows, targets)
    if summary["pass_rate"] >= 0.8:
        return (
            f"Promote `single_pass_wide_cut` to broader randomized validation: pass rate is {summary['pass_rate']:.0%} "
            f"and mean productivity clears the {targets['min_productivity_m3_per_hr']:.2f} m3/hr target."
        )
    return (
        f"Keep `single_pass_wide_cut` in tuning: pass rate is {summary['pass_rate']:.0%}, with "
        f"`{summary['top_failed_check']}` as the most common failed check."
    )


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())
