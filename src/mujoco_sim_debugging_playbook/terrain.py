from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class SoilConfig:
    cohesion: float
    friction_angle_deg: float
    compaction_rate: float
    blade_coupling: float
    spillover_rate: float


@dataclass(frozen=True)
class TerrainConfig:
    x_range: tuple[float, float]
    y_range: tuple[float, float]
    resolution: tuple[int, int]
    base_height: float
    pile_center: tuple[float, float]
    pile_radius: float
    pile_height: float


@dataclass(frozen=True)
class BladeState:
    x: float
    y: float
    yaw: float
    width: float
    depth: float


class TerrainGrid:
    def __init__(self, config: TerrainConfig, heights: np.ndarray | None = None) -> None:
        self.config = config
        nx, ny = config.resolution
        if nx < 2 or ny < 2:
            raise ValueError("terrain resolution must have at least two cells per axis")
        self.xs = np.linspace(config.x_range[0], config.x_range[1], nx)
        self.ys = np.linspace(config.y_range[0], config.y_range[1], ny)
        if heights is None:
            self.heights = self._initial_heights()
        else:
            expected = (nx, ny)
            if heights.shape != expected:
                raise ValueError(f"heights shape {heights.shape} does not match terrain resolution {expected}")
            self.heights = heights.astype(float, copy=True)

    def copy(self) -> TerrainGrid:
        return TerrainGrid(self.config, self.heights.copy())

    @property
    def cell_area(self) -> float:
        return float((self.xs[1] - self.xs[0]) * (self.ys[1] - self.ys[0]))

    def volume(self) -> float:
        return float(np.sum(self.heights - self.config.base_height) * self.cell_area)

    def profile_error(self, target: TerrainGrid) -> float:
        return float(np.sqrt(np.mean((self.heights - target.heights) ** 2)))

    def to_dict(self) -> dict[str, object]:
        return {
            "config": asdict(self.config),
            "xs": self.xs.tolist(),
            "ys": self.ys.tolist(),
            "heights": self.heights.tolist(),
            "volume": self.volume(),
        }

    def _initial_heights(self) -> np.ndarray:
        xx, yy = np.meshgrid(self.xs, self.ys, indexing="ij")
        cx, cy = self.config.pile_center
        radius = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        pile = np.clip(1.0 - radius / self.config.pile_radius, 0.0, 1.0)
        return self.config.base_height + self.config.pile_height * pile**2


def build_target_berm(config: TerrainConfig, target_center_x: float, target_width: float, target_height: float) -> TerrainGrid:
    grid = TerrainGrid(config)
    xx, yy = np.meshgrid(grid.xs, grid.ys, indexing="ij")
    longitudinal = np.clip(1.0 - np.abs(xx - target_center_x) / target_width, 0.0, 1.0)
    lateral = np.clip(1.0 - np.abs(yy - config.pile_center[1]) / (config.pile_radius * 1.4), 0.0, 1.0)
    heights = config.base_height + target_height * longitudinal * lateral
    return TerrainGrid(config, heights)


def apply_blade_pass(
    terrain: TerrainGrid,
    blade_path: Iterable[BladeState],
    soil: SoilConfig,
) -> dict[str, float]:
    start_volume = terrain.volume()
    moved_volume = 0.0
    compacted_volume = 0.0
    carried_volume = 0.0
    states = list(blade_path)
    for index in range(1, len(states)):
        previous = states[index - 1]
        state = states[index]
        moved, compacted, carried_volume = _apply_blade_segment(
            terrain,
            previous,
            state,
            soil,
            carried_volume=carried_volume,
            is_final_segment=index == len(states) - 1,
        )
        moved_volume += moved
        compacted_volume += compacted
    end_volume = terrain.volume()
    return {
        "start_volume": start_volume,
        "end_volume": end_volume,
        "moved_volume": float(moved_volume),
        "compacted_volume": float(compacted_volume),
        "volume_error": float(end_volume - start_volume + compacted_volume),
    }


def _apply_blade_segment(
    terrain: TerrainGrid,
    start: BladeState,
    end: BladeState,
    soil: SoilConfig,
    *,
    carried_volume: float,
    is_final_segment: bool,
) -> tuple[float, float, float]:
    dx = end.x - start.x
    dy = end.y - start.y
    distance = float(np.hypot(dx, dy))
    if distance <= 1e-9:
        return 0.0, 0.0, carried_volume

    forward = np.array([dx / distance, dy / distance])
    lateral = np.array([-forward[1], forward[0]])
    xx, yy = np.meshgrid(terrain.xs, terrain.ys, indexing="ij")
    rel_x = xx - end.x
    rel_y = yy - end.y
    along = rel_x * forward[0] + rel_y * forward[1]
    cross = rel_x * lateral[0] + rel_y * lateral[1]

    blade_mask = (np.abs(cross) <= end.width * 0.5) & (along >= -distance) & (along <= distance * 0.35)
    if not np.any(blade_mask):
        return 0.0, 0.0, carried_volume

    cut_height = terrain.config.base_height + max(0.0, end.depth)
    available = np.clip(terrain.heights - cut_height, 0.0, None)
    resistance = 1.0 + soil.cohesion + np.tan(np.deg2rad(soil.friction_angle_deg)) * 0.25
    removed = np.where(blade_mask, available * np.clip(soil.blade_coupling / resistance, 0.0, 1.0), 0.0)
    removed_volume = float(np.sum(removed) * terrain.cell_area)
    if removed_volume <= 0.0:
        if is_final_segment and carried_volume > 0.0:
            _deposit_material(terrain, end, forward, lateral, distance, carried_volume, final_dump=True)
            return 0.0, 0.0, 0.0
        return 0.0, 0.0, carried_volume

    terrain.heights -= removed

    compacted = removed * np.clip(soil.compaction_rate, 0.0, 0.9)
    transport = removed - compacted
    compacted_volume = float(np.sum(compacted) * terrain.cell_area)
    transport_volume = float(np.sum(transport) * terrain.cell_area)
    blade_load = carried_volume + transport_volume
    deposit_fraction = 1.0 if is_final_segment else float(np.clip(0.03 + soil.spillover_rate * 0.08, 0.03, 0.14))
    deposit_volume = blade_load * deposit_fraction
    next_carried_volume = blade_load - deposit_volume
    if deposit_volume > 0.0:
        _deposit_material(
            terrain,
            end,
            forward,
            lateral,
            distance,
            deposit_volume,
            final_dump=is_final_segment,
        )

    return removed_volume, compacted_volume, next_carried_volume


def _deposit_material(
    terrain: TerrainGrid,
    blade: BladeState,
    forward: np.ndarray,
    lateral: np.ndarray,
    segment_distance: float,
    volume: float,
    *,
    final_dump: bool,
) -> None:
    xx, yy = np.meshgrid(terrain.xs, terrain.ys, indexing="ij")
    rel_x = xx - blade.x
    rel_y = yy - blade.y
    deposit_center_along = 0.0 if final_dump else segment_distance * 0.65
    deposit_along = rel_x * forward[0] + rel_y * forward[1] - deposit_center_along
    deposit_cross = rel_x * lateral[0] + rel_y * lateral[1]
    spread_x = max(blade.width * (0.38 if final_dump else 0.75), terrain.xs[1] - terrain.xs[0])
    spread_y = max(blade.width * (0.38 if final_dump else 0.55), terrain.ys[1] - terrain.ys[0])
    weights = np.exp(-0.5 * ((deposit_along / spread_x) ** 2 + (deposit_cross / spread_y) ** 2))
    if not final_dump:
        weights *= deposit_along >= -spread_x * 0.5
    weight_sum = float(np.sum(weights) * terrain.cell_area)
    if weight_sum > 0.0:
        terrain.heights += weights * (volume / weight_sum)
