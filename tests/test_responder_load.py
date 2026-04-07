import json

from mujoco_sim_debugging_playbook.responder_load import build_responder_load


def test_responder_load_ranks_owner_pressure(tmp_path):
    capacity = tmp_path / "capacity.json"
    sla = tmp_path / "sla.json"
    capacity.write_text(
        json.dumps(
            {
                "owners": [
                    {"owner": "controls", "status": "overloaded"},
                    {"owner": "sim", "status": "healthy"},
                ]
            }
        )
    )
    sla.write_text(
        json.dumps(
            {
                "items": [
                    {"owner": "controls", "effort_points": 5, "status": "breach", "target": "a"},
                    {"owner": "controls", "effort_points": 3, "status": "at_risk", "target": "b"},
                    {"owner": "sim", "effort_points": 2, "status": "on_track", "target": "c"},
                ]
            }
        )
    )

    payload = build_responder_load(capacity_plan_path=capacity, sla_report_path=sla)
    assert payload["summary"]["owner_count"] == 2
    assert payload["summary"]["top_owner"] == "controls"
    assert payload["rows"][0]["pressure_index"] > payload["rows"][1]["pressure_index"]
