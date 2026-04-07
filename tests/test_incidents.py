from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.incidents import build_incident_bundles


def test_build_incident_bundles(tmp_path: Path) -> None:
    triage = tmp_path / "triage_queue.json"
    triage.write_text(json.dumps({
        "items": [
            {
                "target": "episode 1",
                "kind": "randomized_episode",
                "priority_score": 200.0,
                "summary": "Hard randomized episode.",
                "evidence": "delay 5",
                "next_action": "Reduce delay.",
            }
        ]
    }))
    anomalies = tmp_path / "anomaly_report.json"
    anomalies.write_text(json.dumps({
        "benchmark_anomalies": {"top_cases": []},
        "randomization_anomalies": {"episodes": [{"episode": 1, "difficulty_score": 1.2}]}
    }))
    recommendations = tmp_path / "recommendations.json"
    recommendations.write_text(json.dumps({
        "recommendations": [{"target": "episode 1", "recommendation": "Reduce delay.", "tradeoff": "More compute.", "evidence": "delay evidence"}]
    }))

    output_dir = tmp_path / "incidents"
    payload = build_incident_bundles(
        triage_queue_path=triage,
        anomaly_report_path=anomalies,
        recommendation_report_path=recommendations,
        output_dir=output_dir,
        limit=3,
    )
    assert payload["summary"]["count"] == 1
    assert (output_dir / "index.md").exists()
