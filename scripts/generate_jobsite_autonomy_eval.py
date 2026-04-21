from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.jobsite_autonomy_eval import build_jobsite_autonomy_eval


if __name__ == "__main__":
    payload = build_jobsite_autonomy_eval(
        benchmark_summary_path=ROOT / "outputs" / "earthmoving_benchmark" / "earthmoving_summary.json",
        eval_config_path=ROOT / "configs" / "jobsite_autonomy_eval.json",
        output_dir=ROOT / "outputs" / "jobsite_autonomy_eval",
    )
    print(
        "Wrote jobsite autonomy evaluation "
        f"with decision {payload['summary']['overall_decision']} "
        f"and {payload['summary']['release_candidate_count']} release candidates"
    )
