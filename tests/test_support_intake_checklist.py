import json
from mujoco_sim_debugging_playbook.support_intake_checklist import build_support_intake_checklist

def test_support_intake_checklist_builds_three_items(tmp_path):
    a = tmp_path / "a.json"
    r = tmp_path / "r.json"
    a.write_text(json.dumps({"summary": {"template_count": 2, "described_count": 1}}))
    r.write_text(json.dumps({"summary": {"criterion_count": 4}}))
    payload = build_support_intake_checklist(issue_template_audit_path=a, response_rubric_path=r, output_dir=tmp_path)
    assert payload["summary"]["item_count"] == 3
