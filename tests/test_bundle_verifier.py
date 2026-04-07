import json
from mujoco_sim_debugging_playbook.bundle_verifier import build_bundle_verifier


def test_bundle_verifier_marks_pass_for_large_bundle(tmp_path):
    p = tmp_path / "m.json"
    p.write_text(json.dumps({"summary": {"file_count": 8}}))
    payload = build_bundle_verifier(bundle_manifest_path=p, output_dir=tmp_path)
    assert payload["summary"]["status"] == "pass"
