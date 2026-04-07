import json

from mujoco_sim_debugging_playbook.artifact_scenarios import build_artifact_scenarios


def test_artifact_scenarios_improve_under_full_refresh(tmp_path):
    freshness = tmp_path / "artifact_freshness.json"
    freshness.write_text(
        json.dumps(
            {
                "summary": {"artifact_count": 2, "fresh_count": 0, "stale_count": 2, "missing_count": 0},
                "rows": [
                    {"artifact": "dashboard/data.json", "status": "stale", "age_delta_seconds": 10.0},
                    {"artifact": "outputs/support_readiness/support_readiness.json", "status": "stale", "age_delta_seconds": 12.0},
                ],
            }
        )
    )
    maintenance = tmp_path / "maintenance_risk.json"
    maintenance.write_text(
        json.dumps(
            {
                "summary": {
                    "artifact_count": 2,
                    "high_risk_count": 1,
                    "medium_risk_count": 1,
                    "top_risk_artifact": "outputs/support_readiness/support_readiness.json",
                    "top_risk_score": 1.7,
                },
                "rows": [
                    {
                        "artifact": "outputs/support_readiness/support_readiness.json",
                        "status": "stale",
                        "priority": "medium",
                        "risk_score": 1.7,
                        "impact_count": 2,
                        "bundle_count": 1,
                        "bundles": ["support_report_refresh"],
                    },
                    {
                        "artifact": "dashboard/data.json",
                        "status": "stale",
                        "priority": "high",
                        "risk_score": 1.2,
                        "impact_count": 0,
                        "bundle_count": 1,
                        "bundles": ["dashboard_refresh"],
                    },
                ],
            }
        )
    )
    checklist = tmp_path / "refresh_checklist.json"
    checklist.write_text(
        json.dumps(
            {
                "summary": {"bundle_count": 2, "total_steps": 2},
                "bundles": [
                    {
                        "bundle": "dashboard_refresh",
                        "step_count": 1,
                        "validation_target": "dashboard/data.json",
                        "steps": [{"artifact": "dashboard/data.json"}],
                    },
                    {
                        "bundle": "support_report_refresh",
                        "step_count": 1,
                        "validation_target": "outputs/support_readiness/support_readiness.json",
                        "steps": [{"artifact": "outputs/support_readiness/support_readiness.json"}],
                    },
                ],
            }
        )
    )
    regen = tmp_path / "regeneration_plan.json"
    regen.write_text(
        json.dumps(
            {
                "summary": {"count": 2, "high_priority_count": 1},
                "actions": [
                    {"artifact": "dashboard/data.json", "priority": "high"},
                    {"artifact": "outputs/support_readiness/support_readiness.json", "priority": "medium"},
                ],
            }
        )
    )

    payload = build_artifact_scenarios(
        artifact_freshness_path=freshness,
        maintenance_risk_path=maintenance,
        refresh_checklist_path=checklist,
        regeneration_plan_path=regen,
    )

    full = next(item for item in payload["scenarios"] if item["name"] == "Full artifact refresh")
    assert full["status"] == "pass"
