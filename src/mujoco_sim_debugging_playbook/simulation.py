from __future__ import annotations

from dataclasses import asdict, dataclass
from importlib import resources
from pathlib import Path

import mujoco
import numpy as np

from mujoco_sim_debugging_playbook.config import ControllerConfig, ExperimentConfig, SimulationConfig, TaskConfig
from mujoco_sim_debugging_playbook.controller import ReacherController
from mujoco_sim_debugging_playbook.metrics import EpisodeMetrics, compute_episode_metrics


@dataclass
class EpisodeTrace:
    target_xy: list[list[float]]
    ee_xy: list[list[float]]
    joint_angles: list[list[float]]
    target_joint_angles: list[list[float]]
    torques: list[list[float]]
    errors: list[float]
    observed_joint_angles: list[list[float]]
    observed_joint_velocities: list[list[float]]
    error_deltas: list[float]


@dataclass
class EpisodeResult:
    metrics: EpisodeMetrics
    trace: EpisodeTrace


def _asset_path() -> str:
    return str(resources.files("mujoco_sim_debugging_playbook.assets").joinpath("planar_reacher.xml"))


class ReacherSimulation:
    def __init__(
        self,
        task_config: TaskConfig,
        sim_config: SimulationConfig,
        controller_config: ControllerConfig,
        seed: int,
    ) -> None:
        self.task_config = task_config
        self.sim_config = sim_config
        self.controller_config = controller_config
        self.rng = np.random.default_rng(seed)

        self.model = mujoco.MjModel.from_xml_path(_asset_path())
        self.data = mujoco.MjData(self.model)
        self.model.opt.timestep = sim_config.physics_timestep
        self._apply_model_parameters(sim_config)

        self.ee_site_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_SITE, "ee_site")
        self.target_body_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, "target")
        self.shoulder_joint_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, "shoulder")
        self.elbow_joint_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, "elbow")

        self.controller = ReacherController(
            link_lengths=task_config.link_lengths,
            controller_config=controller_config,
            control_delay_steps=sim_config.control_delay_steps,
        )

        self.physics_steps_per_control = max(1, round(sim_config.control_dt / sim_config.physics_timestep))

    def _apply_model_parameters(self, sim_config: SimulationConfig) -> None:
        for joint_index in range(self.model.njnt):
            self.model.dof_damping[joint_index] = sim_config.joint_damping
            self.model.dof_frictionloss[joint_index] = sim_config.friction_loss

        for actuator_index in range(self.model.nu):
            self.model.actuator_gear[actuator_index, 0] = sim_config.actuator_gain

    def sample_target(self) -> np.ndarray:
        x = self.rng.uniform(*self.task_config.target_range.x)
        y = self.rng.uniform(*self.task_config.target_range.y)
        return np.array([x, y], dtype=float)

    def reset(self, target_xy: np.ndarray) -> None:
        mujoco.mj_resetData(self.model, self.data)
        self.data.qpos[:] = np.array([0.25, 0.15], dtype=float)
        self.data.qvel[:] = 0.0
        self.data.ctrl[:] = 0.0
        self.data.mocap_pos[0, :3] = np.array([target_xy[0], target_xy[1], 0.0], dtype=float)
        self.controller.reset()
        mujoco.mj_forward(self.model, self.data)

    def _observe(self) -> tuple[np.ndarray, np.ndarray]:
        qpos = self.data.qpos.copy()
        qvel = self.data.qvel.copy()
        if self.sim_config.sensor_noise_std > 0.0:
            qpos += self.rng.normal(0.0, self.sim_config.sensor_noise_std, size=qpos.shape)
            qvel += self.rng.normal(0.0, self.sim_config.sensor_noise_std, size=qvel.shape)
        return qpos, qvel

    def _ee_xy(self) -> np.ndarray:
        return self.data.site_xpos[self.ee_site_id, :2].copy()

    def run_episode(self, target_xy: np.ndarray, horizon_s: float) -> EpisodeResult:
        self.reset(target_xy)

        num_control_steps = max(1, int(horizon_s / self.sim_config.control_dt))
        trace = EpisodeTrace(
            target_xy=[],
            ee_xy=[],
            joint_angles=[],
            target_joint_angles=[],
            torques=[],
            errors=[],
            observed_joint_angles=[],
            observed_joint_velocities=[],
            error_deltas=[],
        )

        previous_error: float | None = None
        for _ in range(num_control_steps):
            observed_qpos, observed_qvel = self._observe()
            control_state = self.controller.compute(
                observed_qpos=observed_qpos,
                observed_qvel=observed_qvel,
                target_xy=target_xy,
            )
            self.data.ctrl[:] = control_state.torque

            for _ in range(self.physics_steps_per_control):
                mujoco.mj_step(self.model, self.data)

            ee_xy = self._ee_xy()
            error = float(np.linalg.norm(target_xy - ee_xy))
            trace.target_xy.append(target_xy.tolist())
            trace.ee_xy.append(ee_xy.tolist())
            trace.joint_angles.append(self.data.qpos.copy().tolist())
            trace.observed_joint_angles.append(observed_qpos.tolist())
            trace.observed_joint_velocities.append(observed_qvel.tolist())
            trace.target_joint_angles.append(control_state.delayed_joint_angles.tolist())
            trace.torques.append(control_state.torque.tolist())
            trace.errors.append(error)
            trace.error_deltas.append(0.0 if previous_error is None else error - previous_error)
            previous_error = error

        metrics = compute_episode_metrics(
            errors=np.asarray(trace.errors),
            torques=np.asarray(trace.torques),
            control_dt=self.sim_config.control_dt,
            target_radius=self.task_config.target_radius,
        )
        return EpisodeResult(metrics=metrics, trace=trace)


def trace_to_dict(trace: EpisodeTrace) -> dict[str, list[list[float]] | list[float]]:
    return asdict(trace)
