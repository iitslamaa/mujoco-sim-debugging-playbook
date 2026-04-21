from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving import EarthmovingSimulation, load_earthmoving_config, scenario_from_dict


def test_load_earthmoving_config_has_construction_scenarios() -> None:
    payload = load_earthmoving_config(ROOT / "configs" / "earthmoving_benchmark.json")
    assert payload["name"] == "earthmoving_benchmark"
    assert {scenario["name"] for scenario in payload["scenarios"]} >= {
        "baseline_push",
        "cohesive_soil",
        "shallow_blade_slip",
    }


def test_earthmoving_simulation_runs_blade_push() -> None:
    payload = load_earthmoving_config(ROOT / "configs" / "earthmoving_benchmark.json")
    scenario = scenario_from_dict(payload["scenarios"][0])
    result = EarthmovingSimulation(scenario).run()

    assert result.metrics.moved_volume > 0.0
    assert result.metrics.target_zone_volume > 0.0
    assert result.metrics.terrain_profile_rmse >= 0.0
    assert len(result.blade_path) == scenario.blade.steps
