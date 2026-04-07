import json

from mujoco_sim_debugging_playbook.readiness import build_support_readiness_report


def test_support_readiness_fails_on_breaches(tmp_path):
    support_ops = tmp_path / "support_ops.json"
    support_gaps = tmp_path / "support_gaps.json"
    sla = tmp_path / "sla.json"
    capacity = tmp_path / "capacity.json"
    release_notes = tmp_path / "release_notes.json"

    support_ops.write_text(json.dumps({"summary": {"incident_coverage": 0.6, "knowledge_base_coverage": 0.55}}))
    support_gaps.write_text(json.dumps({"summary": {"needs_follow_up_count": 2}}))
    sla.write_text(json.dumps({"summary": {"breach_count": 1, "at_risk_count": 0}}))
    capacity.write_text(json.dumps({"summary": {"overloaded_owner_count": 0}}))
    release_notes.write_text(json.dumps({"regression_gate": {"status": "pass", "violation_count": 0}}))

    payload = build_support_readiness_report(
        support_ops_path=support_ops,
        support_gaps_path=support_gaps,
        sla_report_path=sla,
        capacity_plan_path=capacity,
        release_notes_path=release_notes,
        output_dir=tmp_path / "output",
    )

    assert payload["summary"]["status"] == "fail"
    assert payload["summary"]["failure_count"] == 1
    assert any(check["name"] == "delivery_breaches" and check["status"] == "fail" for check in payload["checks"])
