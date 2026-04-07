from pathlib import Path
import json
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.diagnostics import compare_summaries, summarize_experiment


def test_summarize_experiment_and_compare() -> None:
    payload_a = {
        "summary": {
            "success_rate": 0.5,
            "final_error_mean": 0.12,
            "max_overshoot_mean": 0.01,
            "oscillation_index_mean": 0.8,
        },
        "episodes": [
            {"episode": 0, "final_error": 0.1, "oscillation_index": 0.6},
            {"episode": 1, "final_error": 0.2, "oscillation_index": 0.9},
        ],
    }
    payload_b = {
        "summary": {
            "success_rate": 0.8,
            "final_error_mean": 0.08,
            "max_overshoot_mean": 0.02,
            "oscillation_index_mean": 0.7,
        },
        "episodes": [
            {"episode": 0, "final_error": 0.08, "oscillation_index": 0.7},
            {"episode": 1, "final_error": 0.1, "oscillation_index": 0.75},
        ],
    }
    left = summarize_experiment(payload_a, "baseline")
    right = summarize_experiment(payload_b, "candidate")
    deltas = compare_summaries(left, right)

    assert left.worst_episode == 1
    assert right.most_oscillatory_episode == 1
    assert deltas["success_rate_delta"] == pytest.approx(0.3)
