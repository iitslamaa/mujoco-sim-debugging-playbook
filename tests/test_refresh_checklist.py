import json

from mujoco_sim_debugging_playbook.refresh_checklist import build_refresh_checklist


def test_refresh_checklist_orders_high_priority_first(tmp_path):
    refresh_bundle = tmp_path / "refresh_bundle.json"
    refresh_bundle.write_text(
        json.dumps(
            {
                "actions": [
                    {"bundle": "bundle_a", "artifact": "b", "priority": "medium", "command": "cmd_b", "impact_count": 1, "impacted_artifacts": ["x"]},
                    {"bundle": "bundle_a", "artifact": "a", "priority": "high", "command": "cmd_a", "impact_count": 0, "impacted_artifacts": []},
                ]
            }
        )
    )
    payload = build_refresh_checklist(refresh_bundle_path=refresh_bundle)
    assert payload["summary"]["bundle_count"] == 1
    assert payload["bundles"][0]["steps"][0]["artifact"] == "a"
