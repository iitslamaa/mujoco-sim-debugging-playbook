from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.multipass_plan_eval import build_multipass_plan_eval


def test_multipass_plan_eval_compares_candidate_sequences(tmp_path: Path) -> None:
    payload = build_multipass_plan_eval(
        benchmark_config_path=ROOT / "configs" / "earthmoving_benchmark.json",
        jobsite_config_path=ROOT / "configs" / "jobsite_autonomy_eval.json",
        scenario_name="cohesive_soil",
        output_dir=tmp_path / "multipass",
    )

    assert payload["scenario"] == "cohesive_soil"
    assert payload["summary"]["candidate_count"] >= 3
    assert payload["summary"]["best_candidate"]["productivity_m3_per_hr"] > 0
    assert payload["recommendation"]
    assert (tmp_path / "multipass" / "multipass_plan_eval.md").exists()
