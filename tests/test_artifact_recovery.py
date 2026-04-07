import json

from mujoco_sim_debugging_playbook.artifact_recovery import build_artifact_recovery


def test_artifact_recovery_builds_three_phase_plan(tmp_path):
    readiness = tmp_path / "artifact_readiness.json"
    readiness.write_text(
        json.dumps({"summary": {"status": "fail", "failure_count": 5}})
    )
    scenarios = tmp_path / "artifact_scenarios.json"
    scenarios.write_text(
        json.dumps(
            {
                "scenarios": [
                    {"name": "Top-risk stabilization", "status": "fail", "failure_count": 3},
                    {"name": "Support report sprint", "status": "fail", "failure_count": 1},
                    {"name": "Full artifact refresh", "status": "pass", "failure_count": 0},
                ]
            }
        )
    )
    maintenance = tmp_path / "maintenance_risk.json"
    maintenance.write_text(
        json.dumps(
            {
                "summary": {"top_risk_artifact": "a"},
                "rows": [
                    {"artifact": "a", "command": "cmd_a"},
                    {"artifact": "b", "command": "cmd_b"},
                ],
            }
        )
    )
    checklist = tmp_path / "refresh_checklist.json"
    checklist.write_text(
        json.dumps(
            {
                "bundles": [
                    {
                        "bundle": "support_report_refresh",
                        "steps": [
                            {"artifact": "c", "command": "cmd_c"},
                            {"artifact": "d", "command": "cmd_d"},
                        ],
                    },
                    {
                        "bundle": "dashboard_refresh",
                        "steps": [{"artifact": "e", "command": "cmd_e"}],
                    },
                ]
            }
        )
    )

    payload = build_artifact_recovery(
        artifact_readiness_path=readiness,
        artifact_scenarios_path=scenarios,
        maintenance_risk_path=maintenance,
        refresh_checklist_path=checklist,
    )

    assert payload["summary"]["phase_count"] == 3
    assert payload["phases"][0]["focus_artifacts"] == ["a", "b"]
    assert payload["phases"][-1]["expected_status"] == "pass"
