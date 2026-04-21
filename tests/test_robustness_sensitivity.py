from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.robustness_sensitivity import build_robustness_sensitivity


def test_robustness_sensitivity_ranks_productivity_drivers(tmp_path: Path) -> None:
    payload = build_robustness_sensitivity(
        robustness_path=ROOT / "outputs" / "task_plan_robustness" / "task_plan_robustness.json",
        output_dir=tmp_path / "sensitivity",
    )

    assert payload["summary"]["episode_count"] > 0
    assert payload["summary"]["top_driver"]
    assert payload["sensitivities"]
    assert payload["recommendations"]
    assert (tmp_path / "sensitivity" / "robustness_sensitivity.md").exists()
    assert (tmp_path / "sensitivity" / "productivity_driver_correlations.png").exists()
