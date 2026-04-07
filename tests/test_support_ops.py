from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.support_ops import build_support_ops_report


def test_build_support_ops_report(tmp_path: Path) -> None:
    triage = tmp_path / "triage.json"
    triage.write_text(json.dumps({"items": [{"target": "a"}, {"target": "b"}]}))
    incidents = tmp_path / "incidents.json"
    incidents.write_text(json.dumps({"bundles": [{"target": "a"}]}))
    kb = tmp_path / "kb.json"
    kb.write_text(json.dumps({"entries": [{"target": "a"}]}))
    escalation = tmp_path / "escalation.json"
    escalation.write_text(json.dumps({"items": [{"severity": "critical", "owner": "simulation-debugging", "escalation_path": "Escalate now"}, {"severity": "medium", "owner": "maintainer-review", "escalation_path": "Handle in support"}]}))

    output_dir = tmp_path / "ops"
    payload = build_support_ops_report(
        triage_queue_path=triage,
        incidents_index_path=incidents,
        knowledge_base_index_path=kb,
        escalation_matrix_path=escalation,
        output_dir=output_dir,
    )
    assert payload["summary"]["queue_count"] == 2
    assert (output_dir / "support_ops.md").exists()
