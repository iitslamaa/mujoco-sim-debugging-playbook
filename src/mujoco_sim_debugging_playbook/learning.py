from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset, random_split

from mujoco_sim_debugging_playbook.config import ControllerConfig, ExperimentConfig, SimulationConfig, TaskConfig
from mujoco_sim_debugging_playbook.controller import ReacherController
from mujoco_sim_debugging_playbook.environment import capture_environment_report
from mujoco_sim_debugging_playbook.metrics import aggregate_metrics
from mujoco_sim_debugging_playbook.provenance import write_manifest
from mujoco_sim_debugging_playbook.simulation import ReacherSimulation, trace_to_dict
from mujoco_sim_debugging_playbook.trace_plot import plot_trace


def state_vector(
    observed_qpos: np.ndarray,
    observed_qvel: np.ndarray,
    target_xy: np.ndarray,
    desired_joint_angles: np.ndarray,
) -> np.ndarray:
    joint_error = desired_joint_angles - observed_qpos
    return np.concatenate([observed_qpos, observed_qvel, target_xy, desired_joint_angles, joint_error], axis=0).astype(np.float32)


def collect_imitation_dataset(config: ExperimentConfig, episodes: int, output_dir: str | Path) -> dict[str, Any]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    simulation = ReacherSimulation(
        task_config=config.task,
        sim_config=config.sim,
        controller_config=config.controller,
        seed=config.seed,
    )
    controller = ReacherController(
        link_lengths=config.task.link_lengths,
        controller_config=config.controller,
        control_delay_steps=config.sim.control_delay_steps,
    )

    states: list[np.ndarray] = []
    actions: list[np.ndarray] = []
    targets: list[np.ndarray] = []
    trace_manifest: list[dict[str, Any]] = []

    for episode_index in range(episodes):
        target_xy = simulation.sample_target()
        simulation.reset(target_xy)
        controller.reset()
        num_control_steps = max(1, int(config.episode_horizon_s / config.sim.control_dt))

        episode_trace = {
            "target_xy": [],
            "ee_xy": [],
            "joint_angles": [],
            "target_joint_angles": [],
            "torques": [],
            "errors": [],
            "observed_joint_angles": [],
            "observed_joint_velocities": [],
            "error_deltas": [],
        }

        previous_error: float | None = None
        for _ in range(num_control_steps):
            observed_qpos, observed_qvel = simulation._observe()
            control_state = controller.compute(observed_qpos, observed_qvel, target_xy)
            states.append(state_vector(observed_qpos, observed_qvel, target_xy, control_state.delayed_joint_angles))
            actions.append(control_state.torque.astype(np.float32))
            targets.append(target_xy.astype(np.float32))

            simulation.data.ctrl[:] = control_state.torque
            for _ in range(simulation.physics_steps_per_control):
                simulation._step()

            ee_xy = simulation._ee_xy()
            error = float(np.linalg.norm(target_xy - ee_xy))
            episode_trace["target_xy"].append(target_xy.tolist())
            episode_trace["ee_xy"].append(ee_xy.tolist())
            episode_trace["joint_angles"].append(simulation.data.qpos.copy().tolist())
            episode_trace["target_joint_angles"].append(control_state.delayed_joint_angles.tolist())
            episode_trace["torques"].append(control_state.torque.tolist())
            episode_trace["errors"].append(error)
            episode_trace["observed_joint_angles"].append(observed_qpos.tolist())
            episode_trace["observed_joint_velocities"].append(observed_qvel.tolist())
            episode_trace["error_deltas"].append(0.0 if previous_error is None else error - previous_error)
            previous_error = error

        trace_path = output_path / "expert_traces" / f"episode_{episode_index:03d}.json"
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        trace_path.write_text(json.dumps(episode_trace, indent=2))
        plot_trace(trace_path, output_path / "expert_trace_plots" / f"episode_{episode_index:03d}.png", title=f"expert episode {episode_index:03d}")
        trace_manifest.append({"episode": episode_index, "trace_path": str(trace_path)})

    states_array = np.stack(states)
    actions_array = np.stack(actions)
    targets_array = np.stack(targets)
    dataset_path = output_path / "imitation_dataset.npz"
    np.savez_compressed(dataset_path, states=states_array, actions=actions_array, targets=targets_array)

    summary = {
        "episodes": episodes,
        "num_samples": int(states_array.shape[0]),
        "state_dim": int(states_array.shape[1]),
        "action_dim": int(actions_array.shape[1]),
        "dataset_path": str(dataset_path),
        "trace_manifest": trace_manifest,
    }
    summary_path = output_path / "dataset_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output_path,
        run_type="imitation_dataset",
        config={"episodes": episodes, "experiment_config": experiment_config_to_dict(config)},
        outputs=[summary_path, dataset_path, *[entry["trace_path"] for entry in trace_manifest], *[str(path) for path in (output_path / "expert_trace_plots").glob("*.png")]],
        metadata={"num_samples": int(states_array.shape[0])},
    )
    return summary


class PolicyNetwork(nn.Module):
    def __init__(self, input_dim: int, output_dim: int, hidden_sizes: tuple[int, ...] = (128, 128, 64)) -> None:
        super().__init__()
        layers: list[nn.Module] = []
        prev_dim = input_dim
        for hidden in hidden_sizes:
            layers.extend([nn.Linear(prev_dim, hidden), nn.LayerNorm(hidden), nn.ReLU()])
            prev_dim = hidden
        layers.append(nn.Linear(prev_dim, output_dim))
        self.net = nn.Sequential(*layers)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        return self.net(inputs)


def _make_loader(states: np.ndarray, actions: np.ndarray, batch_size: int, seed: int) -> tuple[DataLoader, DataLoader]:
    state_tensor = torch.from_numpy(states)
    action_tensor = torch.from_numpy(actions)
    dataset = TensorDataset(state_tensor, action_tensor)
    val_size = max(1, int(len(dataset) * 0.2))
    train_size = len(dataset) - val_size
    generator = torch.Generator().manual_seed(seed)
    train_set, val_set = random_split(dataset, [train_size, val_size], generator=generator)
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False)
    return train_loader, val_loader


def train_imitation_policy(
    dataset_path: str | Path,
    output_dir: str | Path,
    epochs: int = 80,
    batch_size: int = 128,
    learning_rate: float = 1e-3,
    seed: int = 7,
) -> dict[str, Any]:
    torch.manual_seed(seed)
    np.random.seed(seed)

    payload = np.load(dataset_path)
    states = payload["states"].astype(np.float32)
    actions = payload["actions"].astype(np.float32)

    state_mean = states.mean(axis=0)
    state_std = states.std(axis=0) + 1e-6
    action_mean = actions.mean(axis=0)
    action_std = actions.std(axis=0) + 1e-6

    normalized_states = (states - state_mean) / state_std
    normalized_actions = (actions - action_mean) / action_std
    train_loader, val_loader = _make_loader(normalized_states, normalized_actions, batch_size=batch_size, seed=seed)

    model = PolicyNetwork(input_dim=states.shape[1], output_dim=actions.shape[1])
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=max(epochs, 1))
    loss_fn = nn.MSELoss()

    history: list[dict[str, float]] = []
    best_val_loss = float("inf")
    best_state: dict[str, torch.Tensor] | None = None

    for epoch in range(1, epochs + 1):
        model.train()
        train_losses = []
        for batch_states, batch_actions in train_loader:
            optimizer.zero_grad(set_to_none=True)
            predictions = model(batch_states)
            loss = loss_fn(predictions, batch_actions)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            train_losses.append(float(loss.item()))

        model.eval()
        val_losses = []
        with torch.no_grad():
            for batch_states, batch_actions in val_loader:
                predictions = model(batch_states)
                val_losses.append(float(loss_fn(predictions, batch_actions).item()))

        scheduler.step()
        record = {
            "epoch": epoch,
            "train_loss": float(np.mean(train_losses)),
            "val_loss": float(np.mean(val_losses)),
            "lr": float(scheduler.get_last_lr()[0]),
        }
        history.append(record)
        if record["val_loss"] < best_val_loss:
            best_val_loss = record["val_loss"]
            best_state = {key: value.detach().clone() for key, value in model.state_dict().items()}

    if best_state is None:
        raise RuntimeError("Training did not produce a valid model state.")

    model.load_state_dict(best_state)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    checkpoint_path = output_path / "policy.pt"
    torch.save(
        {
            "state_dict": model.state_dict(),
            "state_mean": state_mean.tolist(),
            "state_std": state_std.tolist(),
            "action_mean": action_mean.tolist(),
            "action_std": action_std.tolist(),
            "history": history,
            "seed": seed,
        },
        checkpoint_path,
    )
    training_summary = {
        "epochs": epochs,
        "batch_size": batch_size,
        "learning_rate": learning_rate,
        "best_val_loss": best_val_loss,
        "checkpoint_path": str(checkpoint_path),
        "history": history,
    }
    summary_path = output_path / "training_summary.json"
    summary_path.write_text(json.dumps(training_summary, indent=2))
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output_path,
        run_type="imitation_training",
        config={
            "dataset_path": str(dataset_path),
            "epochs": epochs,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "seed": seed,
        },
        inputs=[dataset_path],
        outputs=[summary_path, checkpoint_path],
        metadata={"best_val_loss": best_val_loss},
    )
    return training_summary


def load_policy(checkpoint_path: str | Path) -> tuple[PolicyNetwork, dict[str, np.ndarray]]:
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    state_mean = np.asarray(checkpoint["state_mean"], dtype=np.float32)
    state_std = np.asarray(checkpoint["state_std"], dtype=np.float32)
    action_mean = np.asarray(checkpoint["action_mean"], dtype=np.float32)
    action_std = np.asarray(checkpoint["action_std"], dtype=np.float32)
    model = PolicyNetwork(input_dim=state_mean.shape[0], output_dim=action_mean.shape[0])
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()
    return model, {
        "state_mean": state_mean,
        "state_std": state_std,
        "action_mean": action_mean,
        "action_std": action_std,
    }


def evaluate_policy(
    checkpoint_path: str | Path,
    experiment_config: ExperimentConfig,
    episodes: int,
    output_dir: str | Path,
) -> dict[str, Any]:
    model, normalization = load_policy(checkpoint_path)
    simulation = ReacherSimulation(
        task_config=experiment_config.task,
        sim_config=experiment_config.sim,
        controller_config=experiment_config.controller,
        seed=experiment_config.seed + 101,
    )

    metric_rows = []
    episode_rows = []
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    def torque_policy(observed_qpos: np.ndarray, observed_qvel: np.ndarray, target_xy: np.ndarray) -> np.ndarray:
        desired_joint_angles = simulation.controller.inverse_kinematics(target_xy)
        raw_state = state_vector(observed_qpos, observed_qvel, target_xy, desired_joint_angles)
        normalized_state = (raw_state - normalization["state_mean"]) / normalization["state_std"]
        with torch.no_grad():
            prediction = model(torch.from_numpy(normalized_state).unsqueeze(0)).squeeze(0).numpy()
        torque = prediction * normalization["action_std"] + normalization["action_mean"]
        return np.clip(torque, -experiment_config.controller.max_torque, experiment_config.controller.max_torque)

    for episode_index in range(episodes):
        target_xy = simulation.sample_target()
        result = simulation.run_episode_with_policy(target_xy, experiment_config.episode_horizon_s, torque_policy)
        trace_path = output_path / "traces" / f"episode_{episode_index:03d}.json"
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        trace_path.write_text(json.dumps(trace_to_dict(result.trace), indent=2))
        plot_trace(trace_path, output_path / "trace_plots" / f"episode_{episode_index:03d}.png", title=f"policy episode {episode_index:03d}")
        metric_rows.append(result.metrics)
        episode_rows.append(
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

    summary = aggregate_metrics(metric_rows)
    payload = {
        "summary": summary,
        "episodes": episode_rows,
        "checkpoint_path": str(checkpoint_path),
        "environment": capture_environment_report(Path.cwd()),
    }
    summary_path = output_path / "summary.json"
    summary_path.write_text(json.dumps(payload, indent=2))
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output_path,
        run_type="imitation_evaluation",
        config={"episodes": episodes, "experiment_config": experiment_config_to_dict(experiment_config)},
        inputs=[checkpoint_path],
        outputs=[summary_path, *[str(path) for path in (output_path / "traces").glob("*.json")], *[str(path) for path in (output_path / "trace_plots").glob("*.png")]],
        metadata={"summary": summary},
    )
    return payload


def experiment_config_to_dict(config: ExperimentConfig) -> dict[str, Any]:
    return {
        "name": config.name,
        "episodes": config.episodes,
        "episode_horizon_s": config.episode_horizon_s,
        "seed": config.seed,
        "output_dir": config.output_dir,
        "task": {
            "target_radius": config.task.target_radius,
            "target_range": {
                "x": list(config.task.target_range.x),
                "y": list(config.task.target_range.y),
            },
            "link_lengths": list(config.task.link_lengths),
        },
        "sim": {
            "physics_timestep": config.sim.physics_timestep,
            "control_dt": config.sim.control_dt,
            "joint_damping": config.sim.joint_damping,
            "actuator_gain": config.sim.actuator_gain,
            "friction_loss": config.sim.friction_loss,
            "sensor_noise_std": config.sim.sensor_noise_std,
            "control_delay_steps": config.sim.control_delay_steps,
        },
        "controller": {
            "kp": config.controller.kp,
            "kd": config.controller.kd,
            "max_torque": config.controller.max_torque,
        },
    }
