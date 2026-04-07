import json

from mujoco_sim_debugging_playbook.release_blockers import build_release_blockers


def test_release_blockers_collects_warn_entries(tmp_path):
    checklist = tmp_path / "checklist.json"
    matrix = tmp_path / "matrix.json"
    checklist.write_text(json.dumps({"items": [{"name": "compatibility", "status": "warn"}]}))
    matrix.write_text(json.dumps({"rows": [{"dimension": "release_checklist", "status": "warn"}]}))
    payload = build_release_blockers(
        release_checklist_path=checklist,
        release_matrix_path=matrix,
        output_dir=tmp_path,
    )
    assert payload["summary"]["blocker_count"] == 2
