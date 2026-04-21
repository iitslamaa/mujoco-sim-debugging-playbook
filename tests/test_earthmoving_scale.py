from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_scale import run_earthmoving_scale_study


def test_scale_study_runs_seeded_batch(tmp_path: Path) -> None:
    result = run_earthmoving_scale_study(
        config_path=ROOT / "configs" / "earthmoving_benchmark.json",
        output_dir=tmp_path / "scale",
        episodes_per_scenario=2,
        seed=11,
        workers=1,
        variation=0.1,
    )

    assert result["summary"]["episode_count"] == 6
    assert result["summary"]["episodes_per_second"] > 0.0
    assert (Path(result["output_dir"]) / "scale_summary.json").exists()
    assert (Path(result["output_dir"]) / "report.md").exists()
