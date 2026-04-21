from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_plan_search import search_earthmoving_blade_plan


def test_plan_search_ranks_candidates(tmp_path: Path) -> None:
    payload = search_earthmoving_blade_plan(
        config_path=ROOT / "configs" / "earthmoving_benchmark.json",
        scenario_name="baseline_push",
        output_dir=tmp_path / "plan_search",
        depth_values=[0.01, 0.02],
        width_values=[0.16, 0.2],
        y_offsets=[0.0],
    )

    assert payload["summary"]["candidate_count"] == 4
    assert payload["rows"][0]["score"] <= payload["rows"][-1]["score"]
    assert payload["summary"]["best_candidate"]["candidate"]
    assert (tmp_path / "plan_search" / "plan_search.json").exists()
    assert (tmp_path / "plan_search" / "report.md").exists()
