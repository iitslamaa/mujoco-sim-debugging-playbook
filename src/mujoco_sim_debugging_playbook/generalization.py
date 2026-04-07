from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

from mujoco_sim_debugging_playbook.benchmark import _expert_policy_fn, _hybrid_policy_fn, _torch_policy_fn
from mujoco_sim_debugging_playbook.config import ControllerConfig, ExperimentConfig, Range2D, SimulationConfig, TaskConfig
from mujoco_sim_debugging_playbook.environment import capture_environment_report
from mujoco_sim_debugging_playbook.learning import load_policy, state_vector
from mujoco_sim_debugging_playbook.metrics import aggregate_metrics
from mujoco_sim_debugging_playbook.rl import load_reinforce_policy
from mujoco_sim_debugging_playbook.simulation import ReacherSimulation


def load_generalization_config(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _base_experiment(payload: dict[str, Any], sim_values: dict[str, Any]) -> ExperimentConfig:
    return ExperimentConfig(
        name=payload["name"],
        episodes=payload["episodes"],
        episode_horizon_s=payload["episode_horizon_s"],
        seed=payload["seed"],
        output_dir=str(Path(payload["output_dir"])),
        task=TaskConfig(
            target_radius=payload["task"]["target_radius"],
            target_range=Range2D(
                x=tuple(payload["task"]["target_range"]["x"]),
                y=tuple(payload["task"]["target_range"]["y"]),
            ),
            link_lengths=tuple(payload["task"]["link_lengths"]),
        ),
        sim=SimulationConfig(**sim_values),
        controller=ControllerConfig(**payload["controller"]),
    )


def _rl_policy_fn(checkpoint_path: str | Path, simulation: ReacherSimulation) -> Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray]:
    policy, normalization = load_reinforce_policy(checkpoint_path)

    def fn(observed_qpos: np.ndarray, observed_qvel: np.ndarray, target_xy: np.ndarray) -> np.ndarray:
        desired_joint_angles = simulation.controller.inverse_kinematics(target_xy)
        raw_state = state_vector(observed_qpos, observed_qvel, target_xy, desired_joint_angles)
        normalized_state = (raw_state - normalization["state_mean"]) / normalization["state_std"]
        with torch.no_grad():
            mean, _ = policy(torch.from_numpy(normalized_state).unsqueeze(0).float())
        torque = mean.squeeze(0).numpy() * normalization["action_std"] + normalization["action_mean"]
        return np.clip(torque, -simulation.controller_config.max_torque, simulation.controller_config.max_torque)

    return fn


def _randomized_sim_values(payload: dict[str, Any], rng: np.random.Generator) -> dict[str, Any]:
    values = dict(payload["base_sim"])
    values["joint_damping"] = float(rng.uniform(*payload["ranges"]["joint_damping"]))
    values["friction_loss"] = float(rng.uniform(*payload["ranges"]["friction_loss"]))
    values["actuator_gain"] = float(rng.uniform(*payload["ranges"]["actuator_gain"]))
    values["sensor_noise_std"] = float(rng.uniform(*payload["ranges"]["sensor_noise_std"]))
    delay_low, delay_high = payload["ranges"]["control_delay_steps"]
    values["control_delay_steps"] = int(rng.integers(delay_low, delay_high + 1))
    return values


def _build_controllers(
    simulation: ReacherSimulation,
    torch_checkpoint: str | Path,
    rl_checkpoint: str | Path,
) -> dict[str, Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray]]:
    return {
        "expert_pd": _expert_policy_fn(simulation),
        "torch_policy": _torch_policy_fn(torch_checkpoint, simulation),
        "hybrid_guardrail": _hybrid_policy_fn(torch_checkpoint, simulation),
        "rl_policy": _rl_policy_fn(rl_checkpoint, simulation),
    }


def _plot_randomization(rows: list[dict[str, Any]], output_dir: str | Path) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    for parameter in ["joint_damping", "actuator_gain", "sensor_noise_std", "control_delay_steps"]:
        fig, axis = plt.subplots(figsize=(8, 4.8))
        for controller in sorted({row["controller"] for row in rows}):
            controller_rows = [row for row in rows if row["controller"] == controller]
            axis.scatter(
                [row[parameter] for row in controller_rows],
                [row["final_error"] for row in controller_rows],
                label=controller,
                alpha=0.7,
            )
        axis.set_xlabel(parameter)
        axis.set_ylabel("Final error")
        axis.set_title(f"Domain randomization: final error vs {parameter}")
        axis.grid(True, alpha=0.3)
        axis.legend()
        fig.tight_layout()
        fig.savefig(output / f"{parameter}_scatter.png", dpi=180)
        plt.close(fig)


def _write_markdown(rows: list[dict[str, Any]], output_path: str | Path) -> None:
    summary_rows = []
    controllers = sorted({row["controller"] for row in rows})
    for controller in controllers:
        controller_rows = [row for row in rows if row["controller"] == controller]
        metrics = aggregate_metrics(
            [
                type("MetricsProxy", (), {
                    "success": row["success"],
                    "final_error": row["final_error"],
                    "min_error": row["final_error"],
                    "mean_error": row["mean_error"],
                    "max_overshoot": row["max_overshoot"],
                    "settling_time_s": None,
                    "oscillation_index": row["oscillation_index"],
                    "control_energy": row["control_energy"],
                })()
                for row in controller_rows
            ]
        )
        summary_rows.append({"controller": controller, **metrics})

    ordered = sorted(summary_rows, key=lambda item: (-item["success_rate"], item["final_error_mean"]))
    lines = [
        "# Domain Randomization Report",
        "",
        "Controllers evaluated under episode-to-episode randomized simulator parameters.",
        "",
        "| controller | success_rate | final_error_mean | overshoot_mean | oscillation_mean | control_energy_mean |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in ordered:
        lines.append(
            f"| {row['controller']} | {row['success_rate']:.3f} | {row['final_error_mean']:.4f} | "
            f"{row['max_overshoot_mean']:.4f} | {row['oscillation_index_mean']:.4f} | {row['control_energy_mean']:.4f} |"
        )
    lines.extend(["", f"Most robust by success rate: `{ordered[0]['controller']}`.", ""])
    Path(output_path).write_text("\n".join(lines))


def run_domain_randomization(
    config_path: str | Path,
    torch_checkpoint: str | Path,
    rl_checkpoint: str | Path,
) -> dict[str, Any]:
    payload = load_generalization_config(config_path)
    output_dir = Path(payload["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(payload["seed"])

    evaluation_rows: list[dict[str, Any]] = []
    for episode_index in range(payload["episodes"]):
        sim_values = _randomized_sim_values(payload, rng)
        config = _base_experiment(payload, sim_values)
        target_seed = payload["seed"] + episode_index * 17
        for controller_name in ["expert_pd", "torch_policy", "hybrid_guardrail", "rl_policy"]:
            simulation = ReacherSimulation(
                task_config=config.task,
                sim_config=config.sim,
                controller_config=config.controller,
                seed=target_seed,
            )
            controllers = _build_controllers(simulation, torch_checkpoint, rl_checkpoint)
            policy = controllers[controller_name]
            reset_fn = getattr(policy, "reset", None)
            if callable(reset_fn):
                reset_fn()
            target_xy = simulation.sample_target()
            result = simulation.run_episode_with_policy(target_xy, config.episode_horizon_s, policy)
            evaluation_rows.append(
                {
                    "episode": episode_index,
                    "controller": controller_name,
                    "target_x": float(target_xy[0]),
                    "target_y": float(target_xy[1]),
                    "success": int(result.metrics.success),
                    "final_error": result.metrics.final_error,
                    "mean_error": result.metrics.mean_error,
                    "max_overshoot": result.metrics.max_overshoot,
                    "oscillation_index": result.metrics.oscillation_index,
                    "control_energy": result.metrics.control_energy,
                    **sim_values,
                }
            )

    payload_out = {
        "rows": evaluation_rows,
        "environment": capture_environment_report(Path.cwd()),
        "torch_checkpoint": str(torch_checkpoint),
        "rl_checkpoint": str(rl_checkpoint),
    }
    (output_dir / "evaluation_rows.json").write_text(json.dumps(payload_out, indent=2))
    _plot_randomization(evaluation_rows, output_dir)
    _write_markdown(evaluation_rows, output_dir / "report.md")
    return {"rows": evaluation_rows, "output_dir": str(output_dir)}

