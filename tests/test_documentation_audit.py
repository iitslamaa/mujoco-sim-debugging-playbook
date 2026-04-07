import json

from mujoco_sim_debugging_playbook.documentation_audit import build_documentation_audit


def test_documentation_audit_lists_uncovered_targets(tmp_path):
    support_ops = tmp_path / "support_ops.json"
    support_gaps = tmp_path / "support_gaps.json"
    knowledge_base = tmp_path / "knowledge_base.json"
    support_ops.write_text(json.dumps({"summary": {"knowledge_base_coverage": 0.5}}))
    support_gaps.write_text(
        json.dumps({"items": [{"target": "case_a", "missing_artifacts": ["knowledge_base_entry"]}, {"target": "case_b", "missing_artifacts": []}]})
    )
    knowledge_base.write_text(json.dumps({"entries": [{"target": "case_b"}]}))
    payload = build_documentation_audit(
        support_ops_path=support_ops,
        support_gaps_path=support_gaps,
        knowledge_base_path=knowledge_base,
    )
    assert payload["summary"]["entry_count"] == 1
    assert payload["uncovered_targets"] == ["case_a"]
