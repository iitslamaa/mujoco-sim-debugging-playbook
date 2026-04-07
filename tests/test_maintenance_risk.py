import json

from mujoco_sim_debugging_playbook.maintenance_risk import build_maintenance_risk


def test_maintenance_risk_prioritizes_stale_high_impact_artifact(tmp_path):
    freshness = tmp_path / "artifact_freshness.json"
    freshness.write_text(
        json.dumps(
            {
                "rows": [
                    {
                        "artifact": "dashboard/data.json",
                        "status": "stale",
                        "age_delta_seconds": 7200,
                    },
                    {
                        "artifact": "outputs/scorecard/scorecard.json",
                        "status": "fresh",
                        "age_delta_seconds": 0,
                    },
                ]
            }
        )
    )
    regeneration = tmp_path / "regeneration_plan.json"
    regeneration.write_text(
        json.dumps(
            {
                "actions": [
                    {
                        "artifact": "dashboard/data.json",
                        "priority": "high",
                        "command": "python scripts/generate_dashboard.py",
                        "age_delta_seconds": 7200,
                    }
                ]
            }
        )
    )
    impact = tmp_path / "impact_analysis.json"
    impact.write_text(
        json.dumps(
            {
                "rows": [
                    {
                        "dependency": "dashboard/data.json",
                        "impact_count": 4,
                        "impacted_artifacts": ["a", "b", "c", "d"],
                    }
                ]
            }
        )
    )
    refresh_bundle = tmp_path / "refresh_bundle.json"
    refresh_bundle.write_text(
        json.dumps(
            {
                "actions": [
                    {
                        "bundle": "dashboard_refresh",
                        "artifact": "dashboard/data.json",
                    }
                ]
            }
        )
    )

    payload = build_maintenance_risk(
        artifact_freshness_path=freshness,
        regeneration_plan_path=regeneration,
        impact_analysis_path=impact,
        refresh_bundle_path=refresh_bundle,
    )

    assert payload["summary"]["top_risk_artifact"] == "dashboard/data.json"
    assert payload["summary"]["high_risk_count"] == 1
    assert payload["rows"][0]["risk_score"] > payload["rows"][1]["risk_score"]
