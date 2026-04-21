from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.field_trial_case_study import build_field_trial_case_study


def test_field_trial_case_study_links_replay_to_deployment_decision(tmp_path: Path) -> None:
    payload = build_field_trial_case_study(
        review_packet_path=ROOT / "outputs" / "earthmoving_review_packet" / "review_packet.json",
        jobsite_eval_path=ROOT / "outputs" / "jobsite_autonomy_eval" / "jobsite_autonomy_eval.json",
        replay_path=ROOT / "outputs" / "earthmoving_replay" / "cohesive_soil_replay.json",
        gap_report_path=ROOT / "outputs" / "earthmoving_gap" / "gap_report.json",
        plan_search_path=ROOT / "outputs" / "earthmoving_plan_search" / "plan_search.json",
        output_dir=tmp_path / "case_study",
    )

    assert payload["scenario"] == "cohesive_soil"
    assert payload["executive_readout"]
    assert payload["root_cause_hypotheses"]
    assert payload["next_experiment"]
    assert (tmp_path / "case_study" / "field_trial_case_study.md").exists()
