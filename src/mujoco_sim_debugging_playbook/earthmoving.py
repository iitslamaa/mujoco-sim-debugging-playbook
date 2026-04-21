from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from importlib import resources
from pathlib import Path
from typing import Any

import mujoco
import numpy as np

from mujoco_sim_debugging_playbook.terrain import (
    BladeState,
    SoilConfig,
    TerrainConfig,
    TerrainGrid,
    apply_blade_pass,
    build_target_berm,
)


@dataclass(frozen=True)
class BladePlan:
    start_x: float
    end_x: float
    y: float
    yaw: float
    width: float
    depth: float
    steps: int


@dataclass(frozen=True)
class EarthmovingScenario:
    name: str
    terrain: TerrainConfig
    soil: SoilConfig
    blade: BladePlan
    target_center_x: float
    target_width: float
    target_height: float


@dataclass(frozen=True)
class EarthmovingMetrics:
    moved_volume: float
    compacted_volume: float
    volume_error: float
    volume_conservation_error: float
    terrain_profile_rmse: float
    target_zone_volume: float
    material_moved_per_second: float
    pass_count: int
    runtime_s: float


@dataclass(frozen=True)
class EarthmovingResult:
    scenario: str
    metrics: EarthmovingMetrics
    initial_terrain: dict[str, object]
    final_terrain: dict[str, object]
    target_terrain: dict[str, object]
    blade_path: list[dict[str, float]]


def _asset_path() -> str:
    return str(resources.files("mujoco_sim_debugging_playbook.assets").joinpath("earthmoving_dozer.xml"))


def load_earthmoving_config(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def scenario_from_dict(payload: dict[str, Any]) -> EarthmovingScenario:
    terrain = payload["terrain"]
    soil = payload["soil"]
    blade = payload["blade"]
    return EarthmovingScenario(
        name=payload["name"],
        terrain=TerrainConfig(
            x_range=tuple(terrain["x_range"]),
            y_range=tuple(terrain["y_range"]),
            resolution=tuple(terrain["resolution"]),
            base_height=terrain["base_height"],
            pile_center=tuple(terrain["pile_center"]),
            pile_radius=terrain["pile_radius"],
            pile_height=terrain["pile_height"],
        ),
        soil=SoilConfig(**soil),
        blade=BladePlan(**blade),
        target_center_x=payload["target"]["center_x"],
        target_width=payload["target"]["width"],
        target_height=payload["target"]["height"],
    )


class EarthmovingSimulation:
    def __init__(self, scenario: EarthmovingScenario) -> None:
        self.scenario = scenario
        self.model = mujoco.MjModel.from_xml_path(_asset_path())
        self.data = mujoco.MjData(self.model)
        self.blade_x_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, "blade_x")
        self.blade_y_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, "blade_y")
        self.blade_yaw_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, "blade_yaw")

    def blade_path(self) -> list[BladeState]:
        blade = self.scenario.blade
        xs = np.linspace(blade.start_x, blade.end_x, blade.steps)
        return [
            BladeState(x=float(x), y=blade.y, yaw=blade.yaw, width=blade.width, depth=blade.depth)
            for x in xs
        ]

    def run(self) -> EarthmovingResult:
        start_time = time.perf_counter()
        terrain = TerrainGrid(self.scenario.terrain)
        initial = terrain.copy()
        target = build_target_berm(
            self.scenario.terrain,
            target_center_x=self.scenario.target_center_x,
            target_width=self.scenario.target_width,
            target_height=self.scenario.target_height,
        )
        path = self.blade_path()
        self._replay_machine_path(path)
        soil_summary = apply_blade_pass(terrain, path, self.scenario.soil)
        runtime_s = max(time.perf_counter() - start_time, 1e-9)
        target_zone_volume = _target_zone_volume(terrain, self.scenario.target_center_x, self.scenario.target_width)
        metrics = EarthmovingMetrics(
            moved_volume=soil_summary["moved_volume"],
            compacted_volume=soil_summary["compacted_volume"],
            volume_error=soil_summary["volume_error"],
            volume_conservation_error=abs(soil_summary["volume_error"]),
            terrain_profile_rmse=terrain.profile_error(target),
            target_zone_volume=target_zone_volume,
            material_moved_per_second=soil_summary["moved_volume"] / runtime_s,
            pass_count=1,
            runtime_s=runtime_s,
        )
        return EarthmovingResult(
            scenario=self.scenario.name,
            metrics=metrics,
            initial_terrain=initial.to_dict(),
            final_terrain=terrain.to_dict(),
            target_terrain=target.to_dict(),
            blade_path=[asdict(state) for state in path],
        )

    def _replay_machine_path(self, path: list[BladeState]) -> None:
        mujoco.mj_resetData(self.model, self.data)
        for state in path:
            self.data.qpos[self.blade_x_id] = state.x
            self.data.qpos[self.blade_y_id] = state.y
            self.data.qpos[self.blade_yaw_id] = state.yaw
            mujoco.mj_forward(self.model, self.data)


def _target_zone_volume(terrain: TerrainGrid, center_x: float, width: float) -> float:
    mask = np.abs(terrain.xs[:, None] - center_x) <= width
    excess = np.clip(terrain.heights - terrain.config.base_height, 0.0, None)
    return float(np.sum(np.where(mask, excess, 0.0)) * terrain.cell_area)


def result_to_dict(result: EarthmovingResult) -> dict[str, Any]:
    return {
        "scenario": result.scenario,
        "metrics": asdict(result.metrics),
        "initial_terrain": result.initial_terrain,
        "final_terrain": result.final_terrain,
        "target_terrain": result.target_terrain,
        "blade_path": result.blade_path,
    }
