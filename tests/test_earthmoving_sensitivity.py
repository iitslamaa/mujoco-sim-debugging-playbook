from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_sensitivity import run_earthmoving_sensitivity


def test_sensitivity_ranks_soil_parameter_effects(tmp_path: Path) -> None:
    result = run_earthmoving_sensitivity(
        config_path=ROOT / "configs" / "earthmoving_benchmark.json",
        output_dir=tmp_path / "sensitivity",
        episodes_per_scenario=3,
        seed=5,
        variation=0.2,
    )

    assert result["summary"]["episode_count"] == 9
    assert result["summary"]["top_sensitivity"] is not None
    assert result["sensitivities"][0]["abs_correlation"] >= result["sensitivities"][-1]["abs_correlation"]
    assert (Path(result["output_dir"]) / "sensitivity_summary.json").exists()
    assert (Path(result["output_dir"]) / "report.md").exists()
