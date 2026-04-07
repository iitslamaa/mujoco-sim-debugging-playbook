from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.recommendations import build_recommendation_report


def test_build_recommendation_report(tmp_path: Path) -> None:
    anomaly_path = tmp_path / "anomaly_report.json"
    anomaly_path.write_text(json.dumps({
        "benchmark_anomalies": {
            "top_cases": [
                {"scenario": "delay_heavy", "controller": "expert_pd", "risk_score": 0.4}
            ]
        },
        "randomization_anomalies": {
            "episodes": [
                {
                    "episode": 3,
                    "difficulty_score": 1.2,
                    "success_rate": 0.0,
                    "worst_controller": "expert_pd",
                    "control_delay_steps": 5,
                    "sensor_noise_std": 0.02,
                    "actuator_gain": 50.0,
                    "joint_damping": 0.9
                }
            ]
        }
    }))
    sweep_path = tmp_path / "combined_summary.json"
    sweep_path.write_text(json.dumps([
        {"parameter": "control_dt", "value": 0.01, "success_rate": 0.8, "final_error_mean": 0.03, "control_energy_mean": 100.0},
        {"parameter": "control_dt", "value": 0.02, "success_rate": 0.2, "final_error_mean": 0.08, "control_energy_mean": 130.0},
        {"parameter": "joint_damping", "value": 5.5, "success_rate": 0.7, "final_error_mean": 0.04, "control_energy_mean": 110.0},
        {"parameter": "actuator_gain", "value": 18.0, "success_rate": 0.9, "final_error_mean": 0.02, "control_energy_mean": 90.0},
        {"parameter": "sensor_noise_std", "value": 0.002, "success_rate": 0.6, "final_error_mean": 0.05, "control_energy_mean": 115.0}
    ]))
    output_dir = tmp_path / "recommendations"
    payload = build_recommendation_report(
        anomaly_report_path=anomaly_path,
        sweep_summary_path=sweep_path,
        output_dir=output_dir,
    )
    assert len(payload["recommendations"]) == 2
    assert (output_dir / "recommendations.md").exists()
