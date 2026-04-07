import json

from mujoco_sim_debugging_playbook.artifact_readiness import build_artifact_readiness


def test_artifact_readiness_fails_on_high_risk_and_backlog(tmp_path):
    freshness = tmp_path / "artifact_freshness.json"
    freshness.write_text(
        json.dumps(
            {
                "summary": {
                    "artifact_count": 3,
                    "fresh_count": 0,
                    "stale_count": 3,
                    "missing_count": 0,
                }
            }
        )
    )
    maintenance_risk = tmp_path / "maintenance_risk.json"
    maintenance_risk.write_text(
        json.dumps(
            {
                "summary": {
                    "artifact_count": 3,
                    "high_risk_count": 2,
                    "medium_risk_count": 1,
                    "top_risk_artifact": "dashboard/data.json",
                    "top_risk_score": 1.8,
                }
            }
        )
    )
    refresh_checklist = tmp_path / "refresh_checklist.json"
    refresh_checklist.write_text(
        json.dumps({"summary": {"bundle_count": 2, "total_steps": 6}})
    )
    regeneration_plan = tmp_path / "regeneration_plan.json"
    regeneration_plan.write_text(
        json.dumps({"summary": {"count": 3, "high_priority_count": 1}})
    )

    payload = build_artifact_readiness(
        artifact_freshness_path=freshness,
        maintenance_risk_path=maintenance_risk,
        refresh_checklist_path=refresh_checklist,
        regeneration_plan_path=regeneration_plan,
    )

    assert payload["summary"]["status"] == "fail"
    assert payload["summary"]["failure_count"] >= 2
