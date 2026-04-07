import json

from mujoco_sim_debugging_playbook.artifact_capacity import build_artifact_capacity


def test_artifact_capacity_marks_breach_phase_as_high_pressure(tmp_path):
    delivery = tmp_path / "artifact_delivery.json"
    delivery.write_text(
        json.dumps(
            {
                "phases": [
                    {
                        "phase": 1,
                        "name": "Clear support report bundle",
                        "status": "breach",
                        "estimated_days": 6,
                    },
                    {
                        "phase": 2,
                        "name": "Clear dashboard lag",
                        "status": "on_track",
                        "estimated_days": 1,
                    },
                ]
            }
        )
    )
    recovery = tmp_path / "artifact_recovery.json"
    recovery.write_text(
        json.dumps(
            {
                "phases": [
                    {
                        "phase": 1,
                        "name": "Clear support report bundle",
                        "commands": ["a", "b", "c"],
                        "focus_artifacts": ["outputs/support_readiness/support_readiness.json"],
                    },
                    {
                        "phase": 2,
                        "name": "Clear dashboard lag",
                        "commands": ["d"],
                        "focus_artifacts": ["dashboard/data.json"],
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
                    {"artifact": "outputs/support_readiness/support_readiness.json", "risk_score": 1.6},
                    {"artifact": "dashboard/data.json", "risk_score": 1.0},
                ]
            }
        )
    )

    payload = build_artifact_capacity(
        artifact_delivery_path=delivery,
        artifact_recovery_path=recovery,
        maintenance_risk_path=maintenance,
        output_dir=tmp_path / "out",
    )

    assert payload["summary"]["highest_pressure_phase"] == "Clear support report bundle"
    assert payload["summary"]["overloaded_owner_count"] >= 1
