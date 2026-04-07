from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.regression import compare_snapshots
from mujoco_sim_debugging_playbook.regression import build_regression_history
from mujoco_sim_debugging_playbook.regression import evaluate_regression_diff


def test_compare_snapshots_generates_outputs(tmp_path: Path) -> None:
    left = tmp_path / "left.json"
    right = tmp_path / "right.json"
    left.write_text(json.dumps({
        "name": "left",
        "metrics": {
            "baseline_success_rate": 0.1,
            "baseline_final_error_mean": 0.2,
            "imitation_success_rate": 0.2,
            "imitation_final_error_mean": 0.15,
            "rl_success_rate": 0.3,
            "rl_final_error_mean": 0.12,
            "benchmark_success_rate_by_controller": {"expert_pd": 0.5},
            "randomization_success_rate_by_controller": {"expert_pd": 0.2},
            "randomization_final_error_by_controller": {"expert_pd": 0.1}
        }
    }))
    right.write_text(json.dumps({
        "name": "right",
        "metrics": {
            "baseline_success_rate": 0.2,
            "baseline_final_error_mean": 0.1,
            "imitation_success_rate": 0.25,
            "imitation_final_error_mean": 0.14,
            "rl_success_rate": 0.4,
            "rl_final_error_mean": 0.1,
            "benchmark_success_rate_by_controller": {"expert_pd": 0.55},
            "randomization_success_rate_by_controller": {"expert_pd": 0.25},
            "randomization_final_error_by_controller": {"expert_pd": 0.08}
        }
    }))
    output_dir = tmp_path / "diff"
    payload = compare_snapshots(left, right, output_dir)
    assert payload["scalar_deltas"]["baseline_success_rate"] == 0.1
    assert (output_dir / "regression_diff.md").exists()
    assert (output_dir / "regression_diff.png").exists()


def test_evaluate_regression_diff_flags_threshold_violation() -> None:
    diff_payload = {
        "left": "baseline",
        "right": "candidate",
        "scalar_deltas": {
            "baseline_success_rate": -0.08,
            "baseline_final_error_mean": 0.01,
        },
        "controller_deltas": {
            "benchmark_success_rate_by_controller": {
                "expert_pd": -0.02,
                "torch_policy": -0.15,
            }
        },
    }
    thresholds = {
        "scalar_thresholds": {
            "baseline_success_rate": {"min_delta": -0.05},
            "baseline_final_error_mean": {"max_delta": 0.02},
        },
        "controller_thresholds": {
            "benchmark_success_rate_by_controller": {
                "*": {"min_delta": -0.10}
            }
        },
    }

    report = evaluate_regression_diff(diff_payload, thresholds)
    assert report["status"] == "fail"
    assert report["violation_count"] == 2
    assert report["scalar_results"]["baseline_success_rate"]["passed"] is False
    assert report["controller_results"]["benchmark_success_rate_by_controller"]["torch_policy"]["passed"] is False


def test_build_regression_history_generates_outputs(tmp_path: Path) -> None:
    left = tmp_path / "baseline_reference.json"
    right = tmp_path / "current.json"
    left.write_text(json.dumps({
        "name": "baseline_reference",
        "created_at": "2026-04-01T12:00:00+00:00",
        "metrics": {
            "baseline_success_rate": 0.1,
            "baseline_final_error_mean": 0.2,
            "imitation_success_rate": 0.2,
            "imitation_final_error_mean": 0.15,
            "rl_success_rate": 0.3,
            "rl_final_error_mean": 0.12,
            "benchmark_success_rate_by_controller": {"expert_pd": 0.5},
            "randomization_success_rate_by_controller": {"expert_pd": 0.2},
            "randomization_final_error_by_controller": {"expert_pd": 0.1}
        }
    }))
    right.write_text(json.dumps({
        "name": "current",
        "created_at": "2026-04-02T12:00:00+00:00",
        "metrics": {
            "baseline_success_rate": 0.2,
            "baseline_final_error_mean": 0.18,
            "imitation_success_rate": 0.25,
            "imitation_final_error_mean": 0.14,
            "rl_success_rate": 0.35,
            "rl_final_error_mean": 0.1,
            "benchmark_success_rate_by_controller": {"expert_pd": 0.55},
            "randomization_success_rate_by_controller": {"expert_pd": 0.25},
            "randomization_final_error_by_controller": {"expert_pd": 0.08}
        }
    }))
    gate_reports = {
        "current": {
            "right": "current",
            "status": "pass",
            "violation_count": 0,
        }
    }

    output_dir = tmp_path / "history"
    payload = build_regression_history([left, right], gate_reports, output_dir)
    assert payload["trend_summary"]["baseline_success_rate"]["direction"] == "up"
    assert payload["trend_summary"]["baseline_final_error_mean"]["direction"] == "down"
    assert (output_dir / "history.json").exists()
    assert (output_dir / "history.md").exists()
    assert (output_dir / "history.png").exists()
