from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from mujoco_sim_debugging_playbook.config import ControllerConfig, ExperimentConfig, Range2D, SimulationConfig, TaskConfig
from mujoco_sim_debugging_playbook.controller import ReacherController
from mujoco_sim_debugging_playbook.environment import capture_environment_report
from mujoco_sim_debugging_playbook.learning import load_policy, state_vector
from mujoco_sim_debugging_playbook.metrics import aggregate_metrics
from mujoco_sim_debugging_playbook.simulation import ReacherSimulation


def load_benchmark_config(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _experiment_from_scenario(payload: dict[str, Any], scenario: dict[str, Any]) -> ExperimentConfig:
    return ExperimentConfig(
        name=scenario["name"],
        episodes=payload["episodes"],
        episode_horizon_s=payload["episode_horizon_s"],
        seed=payload["seed"],
        output_dir=str(Path(payload["output_dir"]) / scenario["name"]),
        task=TaskConfig(
            target_radius=payload["task"]["target_radius"],
            target_range=Range2D(
                x=tuple(payload["task"]["target_range"]["x"]),
                y=tuple(payload["task"]["target_range"]["y"]),
            ),
            link_lengths=tuple(payload["task"]["link_lengths"]),
        ),
        sim=SimulationConfig(**scenario["sim"]),
        controller=ControllerConfig(**payload["controller"]),
    )


def _torch_policy_fn(checkpoint_path: str | Path, simulation: ReacherSimulation) -> Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray]:
    model, normalization = load_policy(checkpoint_path)

    def fn(observed_qpos: np.ndarray, observed_qvel: np.ndarray, target_xy: np.ndarray) -> np.ndarray:
        desired_joint_angles = simulation.controller.inverse_kinematics(target_xy)
        raw_state = state_vector(observed_qpos, observed_qvel, target_xy, desired_joint_angles)
        normalized_state = (raw_state - normalization["state_mean"]) / normalization["state_std"]
        import torch
        with torch.no_grad():
            prediction = model(torch.from_numpy(normalized_state).unsqueeze(0)).squeeze(0).numpy()
        torque = prediction * normalization["action_std"] + normalization["action_mean"]
        return np.clip(torque, -simulation.controller_config.max_torque, simulation.controller_config.max_torque)

    return fn


def _expert_policy_fn(simulation: ReacherSimulation) -> Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray]:
    controller = ReacherController(
        link_lengths=simulation.task_config.link_lengths,
        controller_config=simulation.controller_config,
        control_delay_steps=simulation.sim_config.control_delay_steps,
    )

    def fn(observed_qpos: np.ndarray, observed_qvel: np.ndarray, target_xy: np.ndarray) -> np.ndarray:
        state = controller.compute(observed_qpos, observed_qvel, target_xy)
        return state.torque

    setattr(fn, "reset", controller.reset)

    return fn


def _hybrid_policy_fn(checkpoint_path: str | Path, simulation: ReacherSimulation) -> Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray]:
    learned = _torch_policy_fn(checkpoint_path, simulation)
    expert = _expert_policy_fn(simulation)

    def fn(observed_qpos: np.ndarray, observed_qvel: np.ndarray, target_xy: np.ndarray) -> np.ndarray:
        desired_joint_angles = simulation.controller.inverse_kinematics(target_xy)
        tracking_error = np.linalg.norm(desired_joint_angles - observed_qpos)
        if tracking_error > 0.7 or np.linalg.norm(observed_qvel) > 4.5:
            return expert(observed_qpos, observed_qvel, target_xy)
        learned_torque = learned(observed_qpos, observed_qvel, target_xy)
        expert_torque = expert(observed_qpos, observed_qvel, target_xy)
        expert_weight = 0.15 + 0.35 * np.clip(tracking_error / 0.7, 0.0, 1.0)
        return (1.0 - expert_weight) * learned_torque + expert_weight * expert_torque

    def reset() -> None:
        reset_fn = getattr(expert, "reset", None)
        if callable(reset_fn):
            reset_fn()

    setattr(fn, "reset", reset)

    return fn


def _evaluate_controller(
    controller_name: str,
    policy_fn: Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray],
    simulation: ReacherSimulation,
    config: ExperimentConfig,
) -> dict[str, Any]:
    rows = []
    metric_rows = []
    for episode_index in range(config.episodes):
        reset_fn = getattr(policy_fn, "reset", None)
        if callable(reset_fn):
            reset_fn()
        target_xy = simulation.sample_target()
        result = simulation.run_episode_with_policy(target_xy, config.episode_horizon_s, policy_fn)
        metric_rows.append(result.metrics)
        rows.append(
            {
                "episode": episode_index,
                "target_x": float(target_xy[0]),
                "target_y": float(target_xy[1]),
                "success": int(result.metrics.success),
                "final_error": result.metrics.final_error,
                "mean_error": result.metrics.mean_error,
                "max_overshoot": result.metrics.max_overshoot,
                "oscillation_index": result.metrics.oscillation_index,
                "control_energy": result.metrics.control_energy,
            }
        )
    return {
        "controller": controller_name,
        "summary": aggregate_metrics(metric_rows),
        "episodes": rows,
    }


def _plot_benchmark(rows: list[dict[str, Any]], output_dir: str | Path) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    controllers = sorted({row["controller"] for row in rows})
    scenarios = sorted({row["scenario"] for row in rows})
    metrics = [
        ("success_rate", "Success rate"),
        ("final_error_mean", "Final error"),
        ("control_energy_mean", "Control energy"),
    ]

    for metric_key, title in metrics:
        fig, axis = plt.subplots(figsize=(10, 4.8))
        x = np.arange(len(scenarios))
        width = 0.22
        for idx, controller in enumerate(controllers):
            controller_rows = [row for row in rows if row["controller"] == controller]
            values = []
            for scenario in scenarios:
                row = next(item for item in controller_rows if item["scenario"] == scenario)
                values.append(row[metric_key])
            axis.bar(x + (idx - (len(controllers) - 1) / 2) * width, values, width=width, label=controller)

        axis.set_xticks(x)
        axis.set_xticklabels(scenarios, rotation=20)
        axis.set_ylabel(title)
        axis.set_title(f"Controller benchmark: {title}")
        axis.legend()
        axis.grid(True, axis="y", alpha=0.3)
        fig.tight_layout()
        fig.savefig(output / f"{metric_key}.png", dpi=180)
        plt.close(fig)


def _write_markdown_report(rows: list[dict[str, Any]], output_path: str | Path) -> None:
    scenarios = sorted({row["scenario"] for row in rows})
    controllers = sorted({row["controller"] for row in rows})
    lines = [
        "# Controller Benchmark",
        "",
        "Expert, learned, and guarded hybrid controllers compared across scenario stressors.",
        "",
    ]
    for scenario in scenarios:
        lines.extend(
            [
                f"## {scenario}",
                "",
                "| controller | success_rate | final_error_mean | overshoot_mean | oscillation_mean | control_energy_mean |",
                "| --- | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        scenario_rows = [row for row in rows if row["scenario"] == scenario]
        ordered = sorted(scenario_rows, key=lambda item: (-item["success_rate"], item["final_error_mean"]))
        for row in ordered:
            lines.append(
                f"| {row['controller']} | {row['success_rate']:.3f} | {row['final_error_mean']:.4f} | "
                f"{row['max_overshoot_mean']:.4f} | {row['oscillation_index_mean']:.4f} | {row['control_energy_mean']:.4f} |"
            )
        winner = ordered[0]
        lines.extend(
            [
                "",
                f"Best success in this scenario: `{winner['controller']}` at `{winner['success_rate']:.3f}` success rate.",
                "",
            ]
        )
    Path(output_path).write_text("\n".join(lines))


def run_controller_benchmark(
    config_path: str | Path,
    checkpoint_path: str | Path,
) -> dict[str, Any]:
    payload = load_benchmark_config(config_path)
    output_dir = Path(payload["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    benchmark_rows: list[dict[str, Any]] = []
    for scenario in payload["scenarios"]:
        config = _experiment_from_scenario(payload, scenario)
        for controller_name in ["expert_pd", "torch_policy", "hybrid_guardrail"]:
            simulation = ReacherSimulation(
                task_config=config.task,
                sim_config=config.sim,
                controller_config=config.controller,
                seed=config.seed,
            )
            if controller_name == "expert_pd":
                policy = _expert_policy_fn(simulation)
            elif controller_name == "torch_policy":
                policy = _torch_policy_fn(checkpoint_path, simulation)
            else:
                policy = _hybrid_policy_fn(checkpoint_path, simulation)

            result = _evaluate_controller(controller_name, policy, simulation, config)
            row = {
                "scenario": scenario["name"],
                "controller": controller_name,
                **result["summary"],
            }
            benchmark_rows.append(row)

    (output_dir / "benchmark_summary.json").write_text(json.dumps({
        "benchmark_rows": benchmark_rows,
        "environment": capture_environment_report(Path.cwd()),
        "checkpoint_path": str(checkpoint_path),
    }, indent=2))
    _plot_benchmark(benchmark_rows, output_dir)
    _write_markdown_report(benchmark_rows, output_dir / "report.md")
    return {"rows": benchmark_rows, "output_dir": str(output_dir)}
