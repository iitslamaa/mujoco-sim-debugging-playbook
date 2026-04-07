import json

from mujoco_sim_debugging_playbook.workstream import build_workstream_plan


def test_workstream_plan_groups_missing_assets(tmp_path):
    support_gaps_path = tmp_path / "support_gaps.json"
    triage_path = tmp_path / "triage.json"
    recommendations_path = tmp_path / "recommendations.json"

    support_gaps_path.write_text(
        json.dumps(
            {
                "items": [
                    {
                        "target": "benchmark / expert",
                        "kind": "benchmark_case",
                        "severity": "high",
                        "owner": "controls-and-policy",
                        "priority_score": 80.0,
                        "gap_score": 40.0,
                        "missing_artifacts": ["incident_bundle", "knowledge_base_entry"],
                        "next_best_asset": "Create incident bundle",
                    },
                    {
                        "target": "episode 2",
                        "kind": "randomized_episode",
                        "severity": "critical",
                        "owner": "simulation-debugging",
                        "priority_score": 210.0,
                        "gap_score": 35.0,
                        "missing_artifacts": [],
                        "next_best_asset": "No follow-up",
                    },
                ]
            }
        )
    )
    triage_path.write_text(
        json.dumps(
            {
                "items": [
                    {
                        "target": "benchmark / expert",
                        "summary": "Benchmark case remains brittle.",
                    }
                ]
            }
        )
    )
    recommendations_path.write_text(
        json.dumps(
            {
                "recommendations": [
                    {
                        "target": "benchmark / expert",
                        "recommendation": "Raise damping.",
                        "evidence": "Damping sweep improved stability.",
                    }
                ]
            }
        )
    )

    payload = build_workstream_plan(
        support_gaps_path=support_gaps_path,
        triage_queue_path=triage_path,
        recommendations_path=recommendations_path,
        output_dir=tmp_path / "output",
    )

    assert payload["summary"]["lane_count"] == 1
    assert payload["summary"]["item_count"] == 1
    assert payload["summary"]["blocking_count"] == 1
    lane = payload["lanes"][0]
    assert lane["lane"] == "incident_backfill"
    assert lane["estimated_points"] >= 4
    assert lane["items"][0]["recommended_action"] == "Raise damping."
