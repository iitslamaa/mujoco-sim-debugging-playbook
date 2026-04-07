from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch import nn

from mujoco_sim_debugging_playbook.config import ExperimentConfig
from mujoco_sim_debugging_playbook.environment import capture_environment_report
from mujoco_sim_debugging_playbook.learning import PolicyNetwork, load_policy, state_vector
from mujoco_sim_debugging_playbook.metrics import aggregate_metrics
from mujoco_sim_debugging_playbook.simulation import ReacherSimulation, trace_to_dict
from mujoco_sim_debugging_playbook.trace_plot import plot_trace


def discounted_returns(rewards: list[float], gamma: float) -> np.ndarray:
    returns = np.zeros(len(rewards), dtype=np.float32)
    running = 0.0
    for index in range(len(rewards) - 1, -1, -1):
        running = rewards[index] + gamma * running
        returns[index] = running
    return returns


class GaussianPolicy(nn.Module):
    def __init__(self, base_model: PolicyNetwork, action_dim: int) -> None:
        super().__init__()
        self.model = base_model
        self.log_std = nn.Parameter(torch.full((action_dim,), -1.75))

    def forward(self, inputs: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        mean = self.model(inputs)
        std = torch.exp(self.log_std).expand_as(mean)
        return mean, std


def _policy_state(
    simulation: ReacherSimulation,
    normalization: dict[str, np.ndarray],
    observed_qpos: np.ndarray,
    observed_qvel: np.ndarray,
    target_xy: np.ndarray,
) -> tuple[np.ndarray, torch.Tensor]:
    desired_joint_angles = simulation.controller.inverse_kinematics(target_xy)
    raw_state = state_vector(observed_qpos, observed_qvel, target_xy, desired_joint_angles)
    normalized_state = (raw_state - normalization["state_mean"]) / normalization["state_std"]
    tensor = torch.from_numpy(normalized_state).unsqueeze(0)
    return raw_state, tensor


def train_policy_gradient(
    imitation_checkpoint: str | Path,
    experiment_config: ExperimentConfig,
    iterations: int,
    episodes_per_iteration: int,
    output_dir: str | Path,
    gamma: float = 0.98,
    learning_rate: float = 3e-4,
    entropy_coef: float = 1e-3,
) -> dict[str, Any]:
    base_model, normalization = load_policy(imitation_checkpoint)
    policy = GaussianPolicy(base_model, action_dim=normalization["action_mean"].shape[0])
    optimizer = torch.optim.AdamW(policy.parameters(), lr=learning_rate, weight_decay=1e-4)

    history: list[dict[str, float]] = []
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for iteration in range(1, iterations + 1):
        log_probs: list[torch.Tensor] = []
        entropies: list[torch.Tensor] = []
        returns_all: list[float] = []
        episode_returns: list[float] = []
        final_errors: list[float] = []
        successes: list[float] = []

        for episode_idx in range(episodes_per_iteration):
            simulation = ReacherSimulation(
                task_config=experiment_config.task,
                sim_config=experiment_config.sim,
                controller_config=experiment_config.controller,
                seed=experiment_config.seed + iteration * 100 + episode_idx,
            )
            target_xy = simulation.sample_target()
            simulation.reset(target_xy)
            rewards: list[float] = []
            episode_log_probs: list[torch.Tensor] = []
            episode_entropies: list[torch.Tensor] = []

            num_control_steps = max(1, int(experiment_config.episode_horizon_s / experiment_config.sim.control_dt))
            final_error = 0.0
            for _ in range(num_control_steps):
                observed_qpos, observed_qvel = simulation._observe()
                _, state_tensor = _policy_state(simulation, normalization, observed_qpos, observed_qvel, target_xy)
                mean, std = policy(state_tensor.float())
                dist = torch.distributions.Normal(mean, std)
                sample = dist.rsample()
                denormalized = sample.squeeze(0).detach().numpy() * normalization["action_std"] + normalization["action_mean"]
                torque = np.clip(denormalized, -experiment_config.controller.max_torque, experiment_config.controller.max_torque)

                simulation.data.ctrl[:] = torque
                for _ in range(simulation.physics_steps_per_control):
                    simulation._step()
                ee_xy = simulation._ee_xy()
                final_error = float(np.linalg.norm(target_xy - ee_xy))
                reward = -final_error - 0.001 * float(np.sum(torque * torque))
                rewards.append(reward)
                episode_log_probs.append(dist.log_prob(sample).sum())
                episode_entropies.append(dist.entropy().sum())

            success = 1.0 if final_error <= experiment_config.task.target_radius else 0.0
            rewards[-1] += 3.0 * success
            returns = discounted_returns(rewards, gamma)
            returns_all.extend(returns.tolist())
            episode_returns.append(float(np.sum(rewards)))
            final_errors.append(final_error)
            successes.append(success)
            log_probs.extend(episode_log_probs)
            entropies.extend(episode_entropies)

        returns_tensor = torch.tensor(returns_all, dtype=torch.float32)
        returns_tensor = (returns_tensor - returns_tensor.mean()) / (returns_tensor.std() + 1e-6)
        log_prob_tensor = torch.stack(log_probs)
        entropy_tensor = torch.stack(entropies)
        loss = -(log_prob_tensor * returns_tensor).mean() - entropy_coef * entropy_tensor.mean()

        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(policy.parameters(), max_norm=1.0)
        optimizer.step()

        record = {
            "iteration": iteration,
            "loss": float(loss.item()),
            "mean_episode_return": float(np.mean(episode_returns)),
            "mean_final_error": float(np.mean(final_errors)),
            "success_rate": float(np.mean(successes)),
            "policy_std": float(torch.exp(policy.log_std).mean().item()),
        }
        history.append(record)

    checkpoint_path = output_path / "reinforce_policy.pt"
    torch.save(
        {
            "state_dict": policy.model.state_dict(),
            "log_std": policy.log_std.detach().cpu().tolist(),
            "state_mean": normalization["state_mean"].tolist(),
            "state_std": normalization["state_std"].tolist(),
            "action_mean": normalization["action_mean"].tolist(),
            "action_std": normalization["action_std"].tolist(),
            "history": history,
        },
        checkpoint_path,
    )
    summary = {
        "iterations": iterations,
        "episodes_per_iteration": episodes_per_iteration,
        "learning_rate": learning_rate,
        "gamma": gamma,
        "entropy_coef": entropy_coef,
        "checkpoint_path": str(checkpoint_path),
        "history": history,
    }
    (output_path / "training_summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def load_reinforce_policy(checkpoint_path: str | Path) -> tuple[GaussianPolicy, dict[str, np.ndarray]]:
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    state_mean = np.asarray(checkpoint["state_mean"], dtype=np.float32)
    state_std = np.asarray(checkpoint["state_std"], dtype=np.float32)
    action_mean = np.asarray(checkpoint["action_mean"], dtype=np.float32)
    action_std = np.asarray(checkpoint["action_std"], dtype=np.float32)
    model = PolicyNetwork(input_dim=state_mean.shape[0], output_dim=action_mean.shape[0])
    model.load_state_dict(checkpoint["state_dict"])
    policy = GaussianPolicy(model, action_dim=action_mean.shape[0])
    policy.log_std.data = torch.tensor(checkpoint["log_std"], dtype=torch.float32)
    policy.eval()
    return policy, {
        "state_mean": state_mean,
        "state_std": state_std,
        "action_mean": action_mean,
        "action_std": action_std,
    }


def evaluate_reinforce_policy(
    checkpoint_path: str | Path,
    experiment_config: ExperimentConfig,
    episodes: int,
    output_dir: str | Path,
) -> dict[str, Any]:
    policy, normalization = load_reinforce_policy(checkpoint_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    simulation = ReacherSimulation(
        task_config=experiment_config.task,
        sim_config=experiment_config.sim,
        controller_config=experiment_config.controller,
        seed=experiment_config.seed + 707,
    )

    metric_rows = []
    episode_rows = []
    for episode_index in range(episodes):
        target_xy = simulation.sample_target()

        def policy_fn(observed_qpos: np.ndarray, observed_qvel: np.ndarray, current_target: np.ndarray) -> np.ndarray:
            _, state_tensor = _policy_state(simulation, normalization, observed_qpos, observed_qvel, current_target)
            with torch.no_grad():
                mean, _ = policy(state_tensor.float())
            denormalized = mean.squeeze(0).numpy() * normalization["action_std"] + normalization["action_mean"]
            return np.clip(denormalized, -experiment_config.controller.max_torque, experiment_config.controller.max_torque)

        result = simulation.run_episode_with_policy(target_xy, experiment_config.episode_horizon_s, policy_fn)
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
        trace_path = output_path / "traces" / f"episode_{episode_index:03d}.json"
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        trace_path.write_text(json.dumps(trace_to_dict(result.trace), indent=2))
        plot_trace(trace_path, output_path / "trace_plots" / f"episode_{episode_index:03d}.png", title=f"rl episode {episode_index:03d}")

    payload = {
        "summary": aggregate_metrics(metric_rows),
        "episodes": episode_rows,
        "checkpoint_path": str(checkpoint_path),
        "environment": capture_environment_report(Path.cwd()),
    }
    (output_path / "summary.json").write_text(json.dumps(payload, indent=2))
    return payload

