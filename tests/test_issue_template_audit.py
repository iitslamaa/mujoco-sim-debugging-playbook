from mujoco_sim_debugging_playbook.issue_template_audit import build_issue_template_audit


def test_issue_template_audit_counts_templates(tmp_path):
    template_dir = tmp_path / "ISSUE_TEMPLATE"
    template_dir.mkdir()
    (template_dir / "a.yml").write_text("name: A\ndescription: first\n")
    (template_dir / "b.yml").write_text("name: B\n")
    payload = build_issue_template_audit(template_dir=template_dir, output_dir=tmp_path)
    assert payload["summary"]["template_count"] == 2
