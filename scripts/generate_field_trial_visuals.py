from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.field_trial_visuals import build_field_trial_visuals


if __name__ == "__main__":
    payload = build_field_trial_visuals(
        benchmark_summary_path=ROOT / "outputs" / "earthmoving_benchmark" / "earthmoving_summary.json",
        jobsite_eval_path=ROOT / "outputs" / "jobsite_autonomy_eval" / "jobsite_autonomy_eval.json",
        replay_path=ROOT / "outputs" / "earthmoving_replay" / "cohesive_soil_replay.json",
        output_dir=ROOT / "outputs" / "field_trial_visuals",
    )
    print(f"Wrote field trial visuals for {payload['scenario']}")
