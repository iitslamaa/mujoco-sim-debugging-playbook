import json

from mujoco_sim_debugging_playbook.support_gaps import build_support_gap_report


def test_support_gap_report_flags_missing_assets(tmp_path):
    triage_path = tmp_path / "triage.json"
    incidents_path = tmp_path / "incidents.json"
    knowledge_base_path = tmp_path / "knowledge_base.json"
    escalation_path = tmp_path / "escalation.json"
    recommendations_path = tmp_path / "recommendations.json"

    triage_path.write_text(
        json.dumps(
            {
                "items": [
                    {"target": "episode 1", "kind": "randomized_episode", "priority_score": 210.0},
                    {"target": "noise_heavy / expert_pd", "kind": "benchmark_case", "priority_score": 54.0},
                    {"target": "base -> head", "kind": "release_review", "priority_score": 25.0},
                ]
            }
        )
    )
    incidents_path.write_text(json.dumps({"bundles": [{"target": "episode 1"}]}))
    knowledge_base_path.write_text(json.dumps({"entries": [{"target": "episode 1"}]}))
    escalation_path.write_text(
        json.dumps(
            {
                "items": [
                    {"target": "episode 1", "severity": "critical", "owner": "simulation-debugging"},
                    {"target": "noise_heavy / expert_pd", "severity": "medium", "owner": "controls-and-policy"},
                    {"target": "base -> head", "severity": "low", "owner": "maintainer-review"},
                ]
            }
        )
    )
    recommendations_path.write_text(
        json.dumps(
            {
                "recommendations": [
                    {"target": "episode 1"},
                    {"target": "noise_heavy / expert_pd"},
                ]
            }
        )
    )

    payload = build_support_gap_report(
        triage_queue_path=triage_path,
        incidents_index_path=incidents_path,
        knowledge_base_index_path=knowledge_base_path,
        escalation_matrix_path=escalation_path,
        recommendations_path=recommendations_path,
        output_dir=tmp_path / "output",
    )

    assert payload["summary"]["count"] == 3
    assert payload["summary"]["fully_covered_count"] == 2
    assert payload["summary"]["needs_follow_up_count"] == 1
    assert payload["summary"]["uncovered_critical_count"] == 0

    benchmark_case = next(item for item in payload["items"] if item["target"] == "noise_heavy / expert_pd")
    assert benchmark_case["missing_artifacts"] == ["incident_bundle", "knowledge_base_entry"]
    assert benchmark_case["next_best_asset"].startswith("Capture a reproducible incident bundle")
