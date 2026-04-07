import json

from mujoco_sim_debugging_playbook.dashboard_snapshot_readiness_gate import (
    build_dashboard_snapshot_readiness_gate,
)


def test_dashboard_snapshot_readiness_gate_fails_when_not_closeable(tmp_path):
    owner_load = tmp_path / "owner_load.json"
    closeout = tmp_path / "closeout.json"

    owner_load.write_text(
        json.dumps(
            {
                "summary": {
                    "owner": "dashboard-stabilization",
                    "current_status": "fail",
                    "critical_alert_count": 1,
                    "planned_item_count": 2,
                }
            }
        )
    )
    closeout.write_text(
        json.dumps(
            {
                "summary": {
                    "closeout_status": "not_ready_to_close",
                }
            }
        )
    )

    payload = build_dashboard_snapshot_readiness_gate(
        dashboard_snapshot_owner_load_path=owner_load,
        dashboard_snapshot_closeout_path=closeout,
        output_dir=tmp_path,
    )

    assert payload["summary"]["status"] == "fail"
    assert payload["summary"]["failure_count"] == 2
