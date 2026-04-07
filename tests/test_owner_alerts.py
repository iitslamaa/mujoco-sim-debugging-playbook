import json

from mujoco_sim_debugging_playbook.owner_alerts import build_owner_alerts


def test_owner_alerts_only_emit_for_overloaded_owners(tmp_path):
    capacity = tmp_path / "capacity.json"
    sla = tmp_path / "sla.json"
    capacity.write_text(json.dumps({"owners": [{"owner": "controls", "status": "overloaded", "breach_count": 1, "at_risk_count": 2}, {"owner": "sim", "status": "healthy", "breach_count": 0, "at_risk_count": 0}]}))
    sla.write_text(json.dumps({"items": [{"owner": "controls", "target": "a", "status": "breach", "effort_points": 5}, {"owner": "sim", "target": "b", "status": "on_track", "effort_points": 2}]}))
    payload = build_owner_alerts(capacity_plan_path=capacity, sla_report_path=sla)
    assert payload["summary"]["count"] == 1
    assert payload["alerts"][0]["owner"] == "controls"
