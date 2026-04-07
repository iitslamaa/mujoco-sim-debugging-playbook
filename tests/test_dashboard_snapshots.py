import json

from mujoco_sim_debugging_playbook.dashboard_snapshots import build_dashboard_snapshot


def test_dashboard_snapshot_records_artifact_summary(tmp_path):
    dashboard = tmp_path / "data.json"
    dashboard.write_text(json.dumps({"repo": "demo", "baseline_summary": {"success_rate": 0.5}}))
    packet = tmp_path / "packet.json"
    packet.write_text(
        json.dumps(
            {
                "summary": {
                    "current_status": "fail",
                    "closeout_status": "not_ready_to_close",
                    "projected_terminal_status": "pass",
                    "handoff_owner": "owner-a",
                }
            }
        )
    )

    payload = build_dashboard_snapshot(
        dashboard_data_path=dashboard,
        artifact_packet_path=packet,
        output_dir=tmp_path / "out",
    )

    assert payload["artifact_summary"]["handoff_owner"] == "owner-a"
    assert payload["repo"] == "demo"
