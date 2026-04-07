import json

from mujoco_sim_debugging_playbook.risk_register import build_risk_register


def test_risk_register_surfaces_top_risk(tmp_path):
    anomalies = tmp_path / "anomalies.json"
    readiness = tmp_path / "readiness.json"
    capacity = tmp_path / "capacity.json"
    anomalies.write_text(json.dumps({"benchmark_anomalies": {"top_cases": [{"scenario": "noise", "controller": "expert", "risk_score": 0.7}]}}))
    readiness.write_text(json.dumps({"checks": [{"name": "delivery_breaches", "status": "fail", "message": "breach"}]}))
    capacity.write_text(json.dumps({"owners": [{"owner": "controls", "status": "overloaded", "effort_points": 12}]}))
    payload = build_risk_register(
        anomaly_report_path=anomalies,
        support_readiness_path=readiness,
        capacity_plan_path=capacity,
    )
    assert payload["summary"]["count"] == 3
    assert payload["summary"]["top_risk"] == "controls"
