import json

from mujoco_sim_debugging_playbook.release_evidence_packet import build_release_evidence_packet


def test_release_evidence_packet_collects_release_state(tmp_path):
    dry_run = tmp_path / "dry_run.json"
    blockers = tmp_path / "blockers.json"
    matrix = tmp_path / "matrix.json"
    dry_run.write_text(json.dumps({"summary": {"status": "warn"}, "recommendation": "Wait"}))
    blockers.write_text(json.dumps({"summary": {"blocker_count": 2}, "blockers": ["a", "b"]}))
    matrix.write_text(json.dumps({"summary": {"row_count": 2}, "rows": [{"dimension": "compatibility", "status": "warn"}]}))
    payload = build_release_evidence_packet(
        release_dry_run_path=dry_run,
        release_blockers_path=blockers,
        release_matrix_path=matrix,
        output_dir=tmp_path,
    )
    assert payload["summary"]["blocker_count"] == 2
