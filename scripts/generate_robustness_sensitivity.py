from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.robustness_sensitivity import build_robustness_sensitivity


if __name__ == "__main__":
    payload = build_robustness_sensitivity(
        robustness_path=ROOT / "outputs" / "task_plan_robustness" / "task_plan_robustness.json",
        output_dir=ROOT / "outputs" / "robustness_sensitivity",
    )
    top = payload["summary"]["top_driver"]
    print(f"Wrote robustness sensitivity; top driver={top['input'] if top else 'none'}")
