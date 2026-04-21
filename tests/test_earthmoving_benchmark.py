from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving import load_earthmoving_config, scenario_from_dict
from mujoco_sim_debugging_playbook.earthmoving_benchmark import randomized_soil_variants, run_earthmoving_benchmark


def test_randomized_soil_variants_are_seeded() -> None:
    payload = load_earthmoving_config(ROOT / "configs" / "earthmoving_benchmark.json")
    scenario = scenario_from_dict(payload["scenarios"][0])

    first = randomized_soil_variants(scenario, seed=7, episodes=3, variation=0.2)
    second = randomized_soil_variants(scenario, seed=7, episodes=3, variation=0.2)

    assert [item.soil for item in first] == [item.soil for item in second]
    assert first[0].soil != scenario.soil


def test_run_earthmoving_benchmark_writes_outputs(tmp_path: Path) -> None:
    config_path = tmp_path / "earthmoving.json"
    payload = load_earthmoving_config(ROOT / "configs" / "earthmoving_benchmark.json")
    payload["output_dir"] = str(tmp_path / "outputs")
    payload["scenarios"] = [payload["scenarios"][0]]
    import json
    config_path.write_text(json.dumps(payload))

    result = run_earthmoving_benchmark(config_path)

    output = Path(result["output_dir"])
    assert (output / "earthmoving_summary.json").exists()
    assert (output / "report.md").exists()
    assert (output / "baseline_push_terrain.png").exists()
    assert result["rows"][0]["moved_volume"] > 0.0
    assert result["rows"][0]["deposit_forward_progress"] > 0.0
