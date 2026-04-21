from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.task_plan_robustness import build_task_plan_robustness


def test_task_plan_robustness_sweeps_uncertainty(tmp_path: Path) -> None:
    payload = build_task_plan_robustness(
        benchmark_config_path=ROOT / "configs" / "earthmoving_benchmark.json",
        jobsite_config_path=ROOT / "configs" / "jobsite_autonomy_eval.json",
        scenario_name="cohesive_soil",
        output_dir=tmp_path / "robustness",
        episodes=8,
    )

    assert payload["summary"]["episode_count"] == 8
    assert 0.0 <= payload["summary"]["pass_rate"] <= 1.0
    assert payload["summary"]["mean_productivity_m3_per_hr"] > 0
    assert payload["recommendation"]
    assert (tmp_path / "robustness" / "task_plan_robustness.md").exists()
    assert (tmp_path / "robustness" / "productivity_distribution.png").exists()
