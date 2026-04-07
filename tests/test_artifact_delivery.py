import json

from mujoco_sim_debugging_playbook.artifact_delivery import build_artifact_delivery


def test_artifact_delivery_flags_breach_for_slow_failing_phase(tmp_path):
    recovery = tmp_path / "artifact_recovery.json"
    recovery.write_text(
        json.dumps(
            {
                "phases": [
                    {
                        "phase": 1,
                        "name": "Phase A",
                        "expected_status": "fail",
                        "expected_failure_count": 3,
                        "commands": ["a", "b", "c"],
                        "focus_artifacts": ["x"],
                    },
                    {
                        "phase": 2,
                        "name": "Phase B",
                        "expected_status": "pass",
                        "expected_failure_count": 0,
                        "commands": ["d"],
                        "focus_artifacts": ["y"],
                    },
                ]
            }
        )
    )
    maintenance = tmp_path / "maintenance_risk.json"
    maintenance.write_text(
        json.dumps(
            {
                "rows": [
                    {"artifact": "x", "risk_score": 1.6},
                    {"artifact": "y", "risk_score": 0.4},
                ]
            }
        )
    )
    checklist = tmp_path / "refresh_checklist.json"
    checklist.write_text(
        json.dumps(
            {
                "bundles": [
                    {"bundle": "one", "steps": [{"artifact": "x"}]},
                    {"bundle": "two", "steps": [{"artifact": "y"}]},
                ]
            }
        )
    )

    payload = build_artifact_delivery(
        artifact_recovery_path=recovery,
        maintenance_risk_path=maintenance,
        refresh_checklist_path=checklist,
        output_dir=tmp_path / "out",
    )

    assert payload["summary"]["breach_count"] >= 1
    assert payload["phases"][0]["status"] in {"breach", "at_risk"}
