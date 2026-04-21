from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.field_trial_case_study import build_field_trial_case_study


if __name__ == "__main__":
    payload = build_field_trial_case_study(
        review_packet_path=ROOT / "outputs" / "earthmoving_review_packet" / "review_packet.json",
        jobsite_eval_path=ROOT / "outputs" / "jobsite_autonomy_eval" / "jobsite_autonomy_eval.json",
        replay_path=ROOT / "outputs" / "earthmoving_replay" / "cohesive_soil_replay.json",
        gap_report_path=ROOT / "outputs" / "earthmoving_gap" / "gap_report.json",
        plan_search_path=ROOT / "outputs" / "earthmoving_plan_search" / "plan_search.json",
        multipass_eval_path=ROOT / "outputs" / "multipass_plan_eval" / "multipass_plan_eval.json",
        visuals_path=ROOT / "outputs" / "field_trial_visuals" / "field_trial_visuals.json",
        output_dir=ROOT / "outputs" / "field_trial_case_study",
    )
    print(f"Wrote field trial case study for {payload['scenario']}")
