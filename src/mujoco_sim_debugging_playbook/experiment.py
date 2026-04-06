from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.config import (
    ControllerConfig,
    ExperimentConfig,
    Range2D,
    SimulationConfig,
    TaskConfig,
    dataclass_to_dict,
    save_json,
)
from mujoco_sim_debugging_playbook.metrics import EpisodeMetrics, aggregate_metrics
from mujoco_sim_debugging_playbook.simulation import ReacherSimulation, trace_to_dict


def _metrics_row(index: int, metrics: EpisodeMetrics, target_xy: list[float]) -> dict[str, Any]:
    return {
        "episode": index,
        "target_x": target_xy[0],
        "target_y": target_xy[1],
        "success": int(metrics.success),
        "final_error": metrics.final_error,
        "min_error": metrics.min_error,
        "mean_error": metrics.mean_error,
        "max_overshoot": metrics.max_overshoot,
        "settling_time_s": metrics.settling_time_s,
        "oscillation_index": metrics.oscillation_index,
        "control_energy": metrics.control_energy,
    }


def run_experiment(config: ExperimentConfig) -> dict[str, Any]:
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    simulation = ReacherSimulation(
        task_config=config.task,
        sim_config=config.sim,
        controller_config=config.controller,
        seed=config.seed,
    )

    metric_rows: list[EpisodeMetrics] = []
    trace_manifest: list[dict[str, Any]] = []
    table_rows: list[dict[str, Any]] = []

    for episode_index in range(config.episodes):
        target_xy = simulation.sample_target()
        episode = simulation.run_episode(target_xy=target_xy, horizon_s=config.episode_horizon_s)
        trace_path = output_dir / "traces" / f"episode_{episode_index:03d}.json"
        save_json(trace_to_dict(episode.trace), trace_path)
        trace_manifest.append(
            {
                "episode": episode_index,
                "target_xy": target_xy.tolist(),
                "trace_path": str(trace_path),
            }
        )

        metric_rows.append(episode.metrics)
        table_rows.append(_metrics_row(episode_index, episode.metrics, target_xy.tolist()))

    summary = aggregate_metrics(metric_rows)
    save_json(
        {
            "config": dataclass_to_dict(config),
            "summary": summary,
            "episodes": table_rows,
            "trace_manifest": trace_manifest,
        },
        output_dir / "summary.json",
    )
    write_episode_csv(table_rows, output_dir / "episodes.csv")
    return {
        "config": dataclass_to_dict(config),
        "summary": summary,
        "episodes": table_rows,
        "output_dir": str(output_dir),
    }


def write_episode_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_sweep_config(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _build_experiment_config(
    sweep_payload: dict[str, Any],
    scenario_name: str,
    output_dir: Path,
    sim_values: dict[str, Any],
) -> ExperimentConfig:
    return ExperimentConfig(
        name=scenario_name,
        episodes=sweep_payload["episodes"],
        episode_horizon_s=sweep_payload["episode_horizon_s"],
        seed=sweep_payload["seed"],
        output_dir=str(output_dir),
        task=TaskConfig(
            target_radius=sweep_payload["task"]["target_radius"],
            target_range=Range2D(
                x=tuple(sweep_payload["task"]["target_range"]["x"]),
                y=tuple(sweep_payload["task"]["target_range"]["y"]),
            ),
            link_lengths=tuple(sweep_payload["task"]["link_lengths"]),
        ),
        sim=SimulationConfig(**sim_values),
        controller=ControllerConfig(**sweep_payload["controller"]),
    )


def run_sweep_suite(config_path: str | Path) -> dict[str, Any]:
    from mujoco_sim_debugging_playbook.plot import plot_sweep_results
    from mujoco_sim_debugging_playbook.report import write_markdown_report

    sweep_payload = load_sweep_config(config_path)
    suite_output_dir = Path(sweep_payload["output_dir"])
    suite_output_dir.mkdir(parents=True, exist_ok=True)

    combined_rows: list[dict[str, Any]] = []
    scenario_summaries: list[dict[str, Any]] = []

    for sweep in sweep_payload["sweeps"]:
        parameter = sweep["parameter"]
        for value in sweep["values"]:
            sim_values = dict(sweep_payload["baseline_sim"])
            sim_values[parameter] = value
            scenario_name = f"{parameter}_{value}".replace(".", "p")
            scenario_output_dir = suite_output_dir / scenario_name
            config = _build_experiment_config(
                sweep_payload=sweep_payload,
                scenario_name=scenario_name,
                output_dir=scenario_output_dir,
                sim_values=sim_values,
            )
            result = run_experiment(config)
            summary_row = {
                "parameter": parameter,
                "value": value,
                **result["summary"],
            }
            scenario_summaries.append(summary_row)
            combined_rows.append(summary_row)

    write_episode_csv(combined_rows, suite_output_dir / "combined_summary.csv")
    save_json(scenario_summaries, suite_output_dir / "combined_summary.json")
    plot_sweep_results(scenario_summaries, suite_output_dir)
    write_markdown_report(scenario_summaries, suite_output_dir / "report.md", title=sweep_payload["name"])
    return {
        "suite": sweep_payload["name"],
        "output_dir": str(suite_output_dir),
        "rows": scenario_summaries,
    }
