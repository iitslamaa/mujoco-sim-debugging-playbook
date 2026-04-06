from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.metrics import compute_episode_metrics


def test_compute_episode_metrics_detects_settling() -> None:
    errors = np.array([0.2, 0.12, 0.06, 0.03, 0.02])
    torques = np.ones((5, 2))
    metrics = compute_episode_metrics(errors, torques, control_dt=0.02, target_radius=0.04)

    assert metrics.success is True
    assert metrics.settling_time_s == 0.06
    assert metrics.final_error == 0.02
