import json

from mujoco_sim_debugging_playbook.regeneration_plan import build_regeneration_plan


def test_regeneration_plan_orders_high_priority_dashboard_first(tmp_path):
    freshness = tmp_path / "freshness.json"
    freshness.write_text(
        json.dumps(
            {
                "rows": [
                    {"artifact": "outputs/scorecard/scorecard.json", "status": "stale", "age_delta_seconds": 10},
                    {"artifact": "dashboard/data.json", "status": "stale", "age_delta_seconds": 5},
                    {"artifact": "outputs/support_readiness/support_readiness.json", "status": "fresh", "age_delta_seconds": 0},
                ]
            }
        )
    )
    payload = build_regeneration_plan(artifact_freshness_path=freshness)
    assert payload["summary"]["count"] == 2
    assert payload["actions"][0]["artifact"] == "dashboard/data.json"
