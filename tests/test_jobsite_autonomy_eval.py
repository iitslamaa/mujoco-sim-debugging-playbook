from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.jobsite_autonomy_eval import build_jobsite_autonomy_eval


def test_jobsite_autonomy_eval_scores_deployment_readiness(tmp_path: Path) -> None:
    payload = build_jobsite_autonomy_eval(
        benchmark_summary_path=ROOT / "outputs" / "earthmoving_benchmark" / "earthmoving_summary.json",
        eval_config_path=ROOT / "configs" / "jobsite_autonomy_eval.json",
        output_dir=tmp_path / "jobsite",
    )

    assert payload["summary"]["scenario_count"] == 3
    assert payload["summary"]["overall_decision"]
    assert payload["rows"][0]["cycle_time_s"] > 0
    assert payload["rows"][0]["productivity_m3_per_hr"] > 0
    assert payload["operator_notes"]
    assert (tmp_path / "jobsite" / "jobsite_autonomy_eval.json").exists()
    assert (tmp_path / "jobsite" / "report.md").exists()
