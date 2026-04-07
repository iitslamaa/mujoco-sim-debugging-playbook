import json

from mujoco_sim_debugging_playbook.scenario_planner import build_scenario_plan


def test_scenario_planner_improves_status_when_breaches_removed(tmp_path):
    support_ops = tmp_path / "support_ops.json"
    support_gaps = tmp_path / "support_gaps.json"
    sla = tmp_path / "sla.json"
    capacity = tmp_path / "capacity.json"
    release_notes = tmp_path / "release_notes.json"

    support_ops.write_text(json.dumps({"summary": {"incident_coverage": 0.45, "knowledge_base_coverage": 0.45}}))
    support_gaps.write_text(json.dumps({"summary": {"needs_follow_up_count": 5}}))
    sla.write_text(json.dumps({"summary": {"breach_count": 2, "at_risk_count": 3}}))
    capacity.write_text(json.dumps({"summary": {"overloaded_owner_count": 1}}))
    release_notes.write_text(json.dumps({"regression_gate": {"status": "pass", "violation_count": 0}}))

    payload = build_scenario_plan(
        support_ops_path=support_ops,
        support_gaps_path=support_gaps,
        sla_report_path=sla,
        capacity_plan_path=capacity,
        release_notes_path=release_notes,
        output_dir=tmp_path / "output",
    )

    assert payload["baseline"]["status"] == "fail"
    clear_breaches = next(item for item in payload["scenarios"] if item["name"] == "Clear breaches")
    assert clear_breaches["status"] in {"warn", "pass"}
    assert clear_breaches["failure_count"] == 0
