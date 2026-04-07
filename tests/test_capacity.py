import json

from mujoco_sim_debugging_playbook.capacity import build_capacity_plan


def test_capacity_plan_marks_overloaded_owner(tmp_path):
    sla_path = tmp_path / "sla.json"
    workstream_path = tmp_path / "workstreams.json"
    support_ops_path = tmp_path / "support_ops.json"

    sla_path.write_text(
        json.dumps(
            {
                "summary": {},
                "lanes": [
                    {
                        "lane": "incident_backfill",
                        "breach_count": 1,
                        "at_risk_count": 1,
                    }
                ],
                "items": [
                    {
                        "lane": "incident_backfill",
                        "target": "case_a",
                        "status": "breach",
                        "owner": "controls-and-policy",
                        "effort_points": 5,
                    },
                    {
                        "lane": "incident_backfill",
                        "target": "case_b",
                        "status": "at_risk",
                        "owner": "controls-and-policy",
                        "effort_points": 4,
                    },
                ],
            }
        )
    )
    workstream_path.write_text(
        json.dumps(
            {
                "lanes": [
                    {
                        "lane": "incident_backfill",
                        "items": [
                            {"target": "case_a", "recommended_action": "Shift work"},
                            {"target": "case_b", "recommended_action": "Pre-stage docs"},
                        ],
                    }
                ]
            }
        )
    )
    support_ops_path.write_text(json.dumps({"summary": {"queue_count": 8}}))

    payload = build_capacity_plan(
        sla_report_path=sla_path,
        workstream_plan_path=workstream_path,
        support_ops_path=support_ops_path,
        output_dir=tmp_path / "output",
    )

    assert payload["summary"]["overloaded_owner_count"] == 1
    assert payload["summary"]["rebalance_item_count"] == 2
    assert payload["owners"][0]["owner"] == "controls-and-policy"
    assert payload["owners"][0]["status"] == "overloaded"
    assert payload["rebalance_items"][0]["recommended_owner"] == "simulation-debugging"
