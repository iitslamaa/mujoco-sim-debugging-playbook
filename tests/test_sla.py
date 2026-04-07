from datetime import date
import json

from mujoco_sim_debugging_playbook.sla import build_sla_report


def test_sla_report_flags_high_severity_breach(tmp_path):
    workstream_path = tmp_path / "workstream.json"
    support_ops_path = tmp_path / "support_ops.json"

    workstream_path.write_text(
        json.dumps(
            {
                "lanes": [
                    {
                        "lane": "incident_backfill",
                        "blocking_count": 1,
                        "items": [
                            {
                                "target": "high_case",
                                "severity": "high",
                                "blocking": True,
                                "effort": {"points": 5},
                                "owner": "controls",
                                "deliverable": "Create incident bundle",
                            },
                            {
                                "target": "medium_case",
                                "severity": "medium",
                                "blocking": False,
                                "effort": {"points": 2},
                                "owner": "controls",
                                "deliverable": "Create incident bundle",
                            },
                        ],
                    }
                ]
            }
        )
    )
    support_ops_path.write_text(json.dumps({"summary": {"queue_count": 10}}))

    payload = build_sla_report(
        workstream_plan_path=workstream_path,
        support_ops_path=support_ops_path,
        output_dir=tmp_path / "output",
        today=date(2026, 4, 6),
    )

    assert payload["summary"]["item_count"] == 2
    assert payload["summary"]["breach_count"] == 1
    assert payload["summary"]["next_due_target"] == "high_case"
    assert payload["items"][0]["status"] == "breach"
