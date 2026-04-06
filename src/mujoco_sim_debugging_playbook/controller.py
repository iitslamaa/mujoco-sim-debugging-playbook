from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import math

import numpy as np

from mujoco_sim_debugging_playbook.config import ControllerConfig


@dataclass
class ControlState:
    target_joint_angles: np.ndarray
    delayed_joint_angles: np.ndarray
    torque: np.ndarray


class ReacherController:
    def __init__(
        self,
        link_lengths: tuple[float, float],
        controller_config: ControllerConfig,
        control_delay_steps: int,
    ) -> None:
        self.link_lengths = link_lengths
        self.cfg = controller_config
        self.delay_buffer = deque(maxlen=max(control_delay_steps, 0) + 1)
        for _ in range(self.delay_buffer.maxlen):
            self.delay_buffer.append(np.zeros(2, dtype=float))

    def reset(self) -> None:
        for index in range(self.delay_buffer.maxlen):
            self.delay_buffer[index] = np.zeros(2, dtype=float)

    def inverse_kinematics(self, target_xy: np.ndarray) -> np.ndarray:
        l1, l2 = self.link_lengths
        x = float(target_xy[0])
        y = float(target_xy[1])
        r2 = x * x + y * y
        cos_q2 = (r2 - l1 * l1 - l2 * l2) / (2.0 * l1 * l2)
        cos_q2 = max(-1.0, min(1.0, cos_q2))
        q2 = math.acos(cos_q2)
        k1 = l1 + l2 * math.cos(q2)
        k2 = l2 * math.sin(q2)
        q1 = math.atan2(y, x) - math.atan2(k2, k1)
        return np.array([q1, q2], dtype=float)

    def compute(
        self,
        observed_qpos: np.ndarray,
        observed_qvel: np.ndarray,
        target_xy: np.ndarray,
    ) -> ControlState:
        desired_joint_angles = self.inverse_kinematics(target_xy)
        self.delay_buffer.append(desired_joint_angles.copy())
        delayed_joint_angles = self.delay_buffer[0]

        position_error = delayed_joint_angles - observed_qpos
        damping_term = -self.cfg.kd * observed_qvel
        torque = self.cfg.kp * position_error + damping_term
        torque = np.clip(torque, -self.cfg.max_torque, self.cfg.max_torque)

        return ControlState(
            target_joint_angles=desired_joint_angles,
            delayed_joint_angles=delayed_joint_angles.copy(),
            torque=torque,
        )

