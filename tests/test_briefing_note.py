import json

from mujoco_sim_debugging_playbook.briefing_note import build_briefing_note


def test_briefing_note_surfaces_best_scenario(tmp_path):
    scorecard = tmp_path / "scorecard.json"
    ops_review = tmp_path / "ops_review.json"
    scenario_plan = tmp_path / "scenario_plan.json"
    scorecard.write_text(json.dumps({"cards": [{"label": "A", "value": 1}]}))
    ops_review.write_text(json.dumps({"summary": {"breach_count": 2}, "wins": ["w"], "risks": ["r"]}))
    scenario_plan.write_text(json.dumps({"scenarios": [{"name": "Baseline", "status": "fail"}, {"name": "Full stabilization", "status": "pass"}]}))
    payload = build_briefing_note(
        scorecard_path=scorecard,
        ops_review_path=ops_review,
        scenario_plan_path=scenario_plan,
    )
    assert payload["summary"]["best_scenario"] == "Full stabilization"
