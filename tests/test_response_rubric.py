import json

from mujoco_sim_debugging_playbook.response_rubric import build_response_rubric


def test_response_rubric_uses_catalog_count(tmp_path):
    catalog = tmp_path / "catalog.json"
    catalog.write_text(json.dumps({"summary": {"case_count": 2}}))
    payload = build_response_rubric(support_case_catalog_path=catalog, output_dir=tmp_path)
    assert payload["summary"]["catalog_case_count"] == 2
