from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.task_plan_robustness import build_task_plan_robustness


if __name__ == "__main__":
    payload = build_task_plan_robustness(
        benchmark_config_path=ROOT / "configs" / "earthmoving_benchmark.json",
        jobsite_config_path=ROOT / "configs" / "jobsite_autonomy_eval.json",
        scenario_name="cohesive_soil",
        output_dir=ROOT / "outputs" / "task_plan_robustness",
    )
    print(
        "Wrote task-plan robustness sweep "
        f"with pass rate {payload['summary']['pass_rate']:.0%}"
    )
