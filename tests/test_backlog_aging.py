import json

from mujoco_sim_debugging_playbook.backlog_aging import build_backlog_aging


def test_backlog_aging_marks_stale_items(tmp_path):
    workstreams = tmp_path / "workstreams.json"
    sla = tmp_path / "sla.json"
    workstreams.write_text(
        json.dumps(
            {
                "lanes": [
                    {
                        "lane": "incident_backfill",
                        "items": [
                            {"target": "case_a", "effort": {"points": 5}},
                            {"target": "case_b", "effort": {"points": 2}},
                        ],
                    }
                ]
            }
        )
    )
    sla.write_text(
        json.dumps(
            {
                "items": [
                    {"target": "case_a", "lane": "incident_backfill", "status": "breach", "due_in_days": 7, "effort_points": 5},
                    {"target": "case_b", "lane": "incident_backfill", "status": "on_track", "due_in_days": 2, "effort_points": 2},
                ]
            }
        )
    )
    payload = build_backlog_aging(workstream_plan_path=workstreams, sla_report_path=sla)
    assert payload["summary"]["stale_count"] == 1
    assert payload["summary"]["oldest_target"] == "case_a"
