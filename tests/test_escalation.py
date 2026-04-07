from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.escalation import build_escalation_matrix


def test_build_escalation_matrix(tmp_path: Path) -> None:
    triage = tmp_path / "triage_queue.json"
    triage.write_text(json.dumps({
        "items": [
            {"target": "episode 1", "kind": "randomized_episode", "priority_score": 220.0},
            {"target": "delay_heavy / expert_pd", "kind": "benchmark_case", "priority_score": 90.0}
        ]
    }))
    incidents = tmp_path / "incidents.json"
    incidents.write_text(json.dumps({
        "bundles": [
            {"target": "episode 1", "bundle_path": "outputs/incidents/episode_1.md"}
        ]
    }))
    gate = tmp_path / "gate.json"
    gate.write_text(json.dumps({"status": "pass"}))

    output_dir = tmp_path / "escalation"
    payload = build_escalation_matrix(
        triage_queue_path=triage,
        incidents_index_path=incidents,
        regression_gate_path=gate,
        output_dir=output_dir,
    )
    assert payload["summary"]["critical_count"] == 1
    assert (output_dir / "escalation_matrix.md").exists()
