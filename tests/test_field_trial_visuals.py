from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.field_trial_visuals import build_field_trial_visuals


def test_field_trial_visuals_write_review_plots(tmp_path: Path) -> None:
    payload = build_field_trial_visuals(
        benchmark_summary_path=ROOT / "outputs" / "earthmoving_benchmark" / "earthmoving_summary.json",
        jobsite_eval_path=ROOT / "outputs" / "jobsite_autonomy_eval" / "jobsite_autonomy_eval.json",
        replay_path=ROOT / "outputs" / "earthmoving_replay" / "cohesive_soil_replay.json",
        output_dir=tmp_path / "visuals",
    )

    assert payload["scenario"] == "cohesive_soil"
    assert (tmp_path / "visuals" / "field_trial_visuals.md").exists()
    assert (tmp_path / "visuals" / "cohesive_soil_terrain_delta.png").exists()
    assert (tmp_path / "visuals" / "jobsite_productivity_bottleneck.png").exists()
