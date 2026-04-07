import json

from mujoco_sim_debugging_playbook.refresh_bundle import build_refresh_bundle


def test_refresh_bundle_groups_actions(tmp_path):
    regeneration = tmp_path / "regeneration.json"
    impact = tmp_path / "impact.json"
    regeneration.write_text(
        json.dumps(
            {
                "actions": [
                    {"artifact": "dashboard/data.json", "priority": "high", "command": "python scripts/generate_dashboard.py"},
                    {"artifact": "outputs/ops_review/ops_review.json", "priority": "medium", "command": "python scripts/generate_ops_review.py"},
                ]
            }
        )
    )
    impact.write_text(
        json.dumps(
            {
                "rows": [
                    {"dependency": "dashboard/data.json", "impact_count": 0, "impacted_artifacts": []},
                    {"dependency": "outputs/ops_review/ops_review.json", "impact_count": 2, "impacted_artifacts": ["a", "b"]},
                ]
            }
        )
    )
    payload = build_refresh_bundle(regeneration_plan_path=regeneration, impact_analysis_path=impact)
    assert payload["summary"]["bundle_count"] == 2
    assert payload["bundles"][0]["bundle"] == "dashboard_refresh"
