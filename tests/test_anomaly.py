from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.anomaly import build_anomaly_report


def test_build_anomaly_report_outputs_files(tmp_path: Path) -> None:
    benchmark = tmp_path / "benchmark_summary.json"
    benchmark.write_text(json.dumps({
        "benchmark_rows": [
            {"scenario": "baseline", "controller": "expert_pd", "success_rate": 0.8, "final_error_mean": 0.04, "control_energy_mean": 100.0},
            {"scenario": "baseline", "controller": "torch_policy", "success_rate": 0.4, "final_error_mean": 0.09, "control_energy_mean": 120.0},
            {"scenario": "stress", "controller": "expert_pd", "success_rate": 0.6, "final_error_mean": 0.06, "control_energy_mean": 110.0},
            {"scenario": "stress", "controller": "torch_policy", "success_rate": 0.2, "final_error_mean": 0.11, "control_energy_mean": 140.0}
        ]
    }))
    randomization = tmp_path / "evaluation_rows.json"
    randomization.write_text(json.dumps({
        "rows": [
            {"episode": 0, "controller": "expert_pd", "success": 1, "final_error": 0.04, "control_energy": 100.0, "joint_damping": 1.0, "friction_loss": 0.01, "actuator_gain": 30.0, "sensor_noise_std": 0.0, "control_delay_steps": 0},
            {"episode": 0, "controller": "torch_policy", "success": 0, "final_error": 0.12, "control_energy": 130.0, "joint_damping": 1.0, "friction_loss": 0.01, "actuator_gain": 30.0, "sensor_noise_std": 0.0, "control_delay_steps": 0},
            {"episode": 1, "controller": "expert_pd", "success": 0, "final_error": 0.18, "control_energy": 140.0, "joint_damping": 0.8, "friction_loss": 0.03, "actuator_gain": 50.0, "sensor_noise_std": 0.02, "control_delay_steps": 4},
            {"episode": 1, "controller": "torch_policy", "success": 0, "final_error": 0.16, "control_energy": 120.0, "joint_damping": 0.8, "friction_loss": 0.03, "actuator_gain": 50.0, "sensor_noise_std": 0.02, "control_delay_steps": 4}
        ]
    }))
    output_dir = tmp_path / "anomalies"
    payload = build_anomaly_report(
        benchmark_summary_path=benchmark,
        randomization_rows_path=randomization,
        output_dir=output_dir,
    )
    assert payload["benchmark_anomalies"]["top_cases"][0]["controller"] == "torch_policy"
    assert (output_dir / "anomaly_report.md").exists()
    assert (output_dir / "benchmark_risk_heatmap.png").exists()
