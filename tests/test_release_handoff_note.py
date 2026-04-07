import json

from mujoco_sim_debugging_playbook.release_handoff_note import build_release_handoff_note


def test_release_handoff_note_uses_packet_and_dry_run(tmp_path):
    packet = tmp_path / "packet.json"
    dry_run = tmp_path / "dry.json"
    packet.write_text(json.dumps({"summary": {"blocker_count": 2, "matrix_row_count": 2}}))
    dry_run.write_text(json.dumps({"summary": {"status": "warn"}, "recommendation": "Wait"}))
    payload = build_release_handoff_note(
        release_evidence_packet_path=packet,
        release_dry_run_path=dry_run,
        output_dir=tmp_path,
    )
    assert payload["next_owner"] == "release-review"
