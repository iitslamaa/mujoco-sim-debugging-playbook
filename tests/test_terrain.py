from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.terrain import BladeState, SoilConfig, TerrainConfig, TerrainGrid, apply_blade_pass


def _terrain() -> TerrainGrid:
    return TerrainGrid(
        TerrainConfig(
            x_range=(-0.5, 0.8),
            y_range=(-0.35, 0.35),
            resolution=(64, 36),
            base_height=0.0,
            pile_center=(-0.12, 0.0),
            pile_radius=0.22,
            pile_height=0.12,
        )
    )


def test_blade_pass_moves_material_forward_and_tracks_volume() -> None:
    terrain = _terrain()
    start = terrain.volume()
    path = [
        BladeState(x=-0.34, y=0.0, yaw=0.0, width=0.18, depth=0.015),
        BladeState(x=-0.14, y=0.0, yaw=0.0, width=0.18, depth=0.015),
        BladeState(x=0.12, y=0.0, yaw=0.0, width=0.18, depth=0.015),
        BladeState(x=0.34, y=0.0, yaw=0.0, width=0.18, depth=0.015),
    ]
    soil = SoilConfig(cohesion=0.1, friction_angle_deg=28.0, compaction_rate=0.08, blade_coupling=0.8, spillover_rate=0.25)

    summary = apply_blade_pass(terrain, path, soil)

    assert summary["moved_volume"] > 0.0
    assert abs(summary["volume_error"]) < start * 0.08
    rear = terrain.heights[terrain.xs < -0.2].mean()
    front = terrain.heights[terrain.xs > 0.15].mean()
    assert front > rear


def test_blade_pass_is_deterministic_for_same_inputs() -> None:
    first = _terrain()
    second = _terrain()
    path = [
        BladeState(x=-0.3, y=-0.02, yaw=0.0, width=0.16, depth=0.01),
        BladeState(x=0.2, y=0.02, yaw=0.0, width=0.16, depth=0.01),
    ]
    soil = SoilConfig(cohesion=0.2, friction_angle_deg=35.0, compaction_rate=0.04, blade_coupling=0.65, spillover_rate=0.15)

    first_summary = apply_blade_pass(first, path, soil)
    second_summary = apply_blade_pass(second, path, soil)

    assert first_summary == second_summary
    np.testing.assert_allclose(first.heights, second.heights)
