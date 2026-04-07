from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.triage import build_triage_queue


def test_build_triage_queue(tmp_path: Path) -> None:
    anomalies = tmp_path / "anomaly_report.json"
    anomalies.write_text(json.dumps({
        "benchmark_anomalies": {"top_cases": [{"scenario": "delay_heavy", "controller": "expert_pd", "risk_score": 0.4, "final_error_mean": 0.05}]},
        "randomization_anomalies": {"episodes": [{"episode": 7, "difficulty_score": 1.2, "worst_controller": "expert_pd", "success_rate": 0.0, "control_delay_steps": 5, "sensor_noise_std": 0.01}]}
    }))
    recommendations = tmp_path / "recommendations.json"
    recommendations.write_text(json.dumps({
        "recommendations": [
            {"target": "delay_heavy / expert_pd", "recommendation": "Increase control frequency."},
            {"target": "episode 7", "recommendation": "Reduce control delay."}
        ]
    }))
    gate = tmp_path / "regression_gate.json"
    gate.write_text(json.dumps({"status": "pass", "violation_count": 0}))
    notes = tmp_path / "release_notes.json"
    notes.write_text(json.dumps({"base_ref": "a", "head_ref": "b", "commit_count": 2, "diffstat": "2 files changed"}))

    output_dir = tmp_path / "triage"
    payload = build_triage_queue(
        anomaly_report_path=anomalies,
        recommendation_report_path=recommendations,
        regression_gate_path=gate,
        release_notes_path=notes,
        output_dir=output_dir,
    )
    assert payload["summary"]["count"] == 3
    assert (output_dir / "triage_queue.md").exists()
