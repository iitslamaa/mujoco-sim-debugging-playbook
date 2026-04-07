import json

from mujoco_sim_debugging_playbook.action_register import build_action_register


def test_action_register_carries_priority_from_rebalance_status(tmp_path):
    ops_review = tmp_path / "ops_review.json"
    capacity = tmp_path / "capacity.json"
    ops_review.write_text(json.dumps({"next_actions": [{"target": "a", "owner": "sim", "action": "fix", "reason": "urgent"}]}))
    capacity.write_text(json.dumps({"rebalance_items": [{"target": "a", "status": "breach"}]}))
    payload = build_action_register(ops_review_path=ops_review, capacity_plan_path=capacity)
    assert payload["summary"]["count"] == 1
    assert payload["actions"][0]["priority"] == "high"
