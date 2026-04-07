import json

from mujoco_sim_debugging_playbook.scorecard import build_scorecard


def test_scorecard_builds_compact_cards(tmp_path):
    support_ops = tmp_path / "support_ops.json"
    support_readiness = tmp_path / "support_readiness.json"
    scenario_plan = tmp_path / "scenario_plan.json"
    support_ops.write_text(json.dumps({"summary": {"queue_count": 11, "knowledge_base_coverage": 0.5}}))
    support_readiness.write_text(json.dumps({"summary": {"status": "warn"}}))
    scenario_plan.write_text(json.dumps({"scenarios": [{"name": "A", "status": "warn"}, {"name": "B", "status": "pass"}]}))
    payload = build_scorecard(
        support_ops_path=support_ops,
        support_readiness_path=support_readiness,
        scenario_plan_path=scenario_plan,
    )
    assert len(payload["cards"]) == 4
    assert payload["cards"][-1]["value"] == "B"
