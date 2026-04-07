import json

from mujoco_sim_debugging_playbook.ops_review import build_ops_review


def test_ops_review_summarizes_key_signals(tmp_path):
    support_ops = tmp_path / "support_ops.json"
    support_gaps = tmp_path / "support_gaps.json"
    sla = tmp_path / "sla.json"
    capacity = tmp_path / "capacity.json"
    release_notes = tmp_path / "release_notes.json"
    anomalies = tmp_path / "anomalies.json"

    support_ops.write_text(json.dumps({"summary": {"queue_count": 6, "incident_coverage": 0.5, "knowledge_base_coverage": 0.4, "incident_count": 3, "knowledge_base_count": 2}}))
    support_gaps.write_text(json.dumps({"summary": {"top_gap_target": "case_a"}}))
    sla.write_text(json.dumps({"summary": {"breach_count": 1, "at_risk_count": 2}}))
    capacity.write_text(
        json.dumps(
            {
                "summary": {"highest_pressure_lane": "incident_backfill"},
                "owners": [{"owner": "controls-and-policy"}],
                "rebalance_items": [
                    {"target": "case_a", "recommended_owner": "simulation-debugging", "recommended_action": "Shift", "handoff_reason": "Breach"},
                    {"target": "case_b", "recommended_owner": "simulation-debugging", "recommended_action": "Pair", "handoff_reason": "Risk"},
                ],
            }
        )
    )
    release_notes.write_text(json.dumps({"commit_count": 4, "regression_gate": {"status": "pass"}}))
    anomalies.write_text(json.dumps({"benchmark_anomalies": {"top_cases": [{"scenario": "noise", "controller": "expert_pd", "risk_score": 0.7}]}}))

    payload = build_ops_review(
        support_ops_path=support_ops,
        support_gaps_path=support_gaps,
        sla_report_path=sla,
        capacity_plan_path=capacity,
        release_notes_path=release_notes,
        anomaly_report_path=anomalies,
        output_dir=tmp_path / "output",
    )

    assert payload["summary"]["queue_count"] == 6
    assert payload["summary"]["overloaded_owner"] == "controls-and-policy"
    assert payload["summary"]["top_gap_target"] == "case_a"
    assert len(payload["wins"]) == 3
    assert len(payload["risks"]) >= 3
    assert len(payload["next_actions"]) == 2
