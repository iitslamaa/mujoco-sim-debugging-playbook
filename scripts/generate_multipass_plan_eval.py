from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.multipass_plan_eval import build_multipass_plan_eval


if __name__ == "__main__":
    payload = build_multipass_plan_eval(
        benchmark_config_path=ROOT / "configs" / "earthmoving_benchmark.json",
        jobsite_config_path=ROOT / "configs" / "jobsite_autonomy_eval.json",
        scenario_name="cohesive_soil",
        output_dir=ROOT / "outputs" / "multipass_plan_eval",
    )
    best = payload["summary"]["best_candidate"]
    print(f"Wrote multi-pass plan evaluation; best={best['candidate']} productivity={best['productivity_m3_per_hr']:.2f}")
