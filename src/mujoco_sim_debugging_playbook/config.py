from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Range2D:
    x: tuple[float, float]
    y: tuple[float, float]


@dataclass(frozen=True)
class TaskConfig:
    target_radius: float
    target_range: Range2D
    link_lengths: tuple[float, float]


@dataclass(frozen=True)
class SimulationConfig:
    physics_timestep: float
    control_dt: float
    joint_damping: float
    friction_loss: float
    actuator_gain: float
    sensor_noise_std: float
    control_delay_steps: int


@dataclass(frozen=True)
class ControllerConfig:
    kp: float
    kd: float
    max_torque: float


@dataclass(frozen=True)
class ExperimentConfig:
    name: str
    episodes: int
    episode_horizon_s: float
    seed: int
    output_dir: str
    task: TaskConfig
    sim: SimulationConfig
    controller: ControllerConfig


def _range2d_from_dict(payload: dict[str, Any]) -> Range2D:
    return Range2D(
        x=tuple(payload["x"]),
        y=tuple(payload["y"]),
    )


def load_experiment_config(path: str | Path) -> ExperimentConfig:
    payload = json.loads(Path(path).read_text())
    return ExperimentConfig(
        name=payload["name"],
        episodes=payload["episodes"],
        episode_horizon_s=payload["episode_horizon_s"],
        seed=payload["seed"],
        output_dir=payload["output_dir"],
        task=TaskConfig(
            target_radius=payload["task"]["target_radius"],
            target_range=_range2d_from_dict(payload["task"]["target_range"]),
            link_lengths=tuple(payload["task"]["link_lengths"]),
        ),
        sim=SimulationConfig(**payload["sim"]),
        controller=ControllerConfig(**payload["controller"]),
    )


def save_json(data: dict[str, Any] | list[Any], path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(data, indent=2))


def dataclass_to_dict(value: Any) -> dict[str, Any]:
    return asdict(value)

