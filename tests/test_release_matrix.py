import json
from mujoco_sim_debugging_playbook.release_matrix import build_release_matrix


def test_release_matrix_builds_two_rows(tmp_path):
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    a.write_text(json.dumps({"summary": {"warn_count": 0}}))
    b.write_text(json.dumps({"summary": {"status": "warn"}}))
    payload = build_release_matrix(release_checklist_path=a, compatibility_path=b, output_dir=tmp_path)
    assert payload["summary"]["row_count"] == 2
