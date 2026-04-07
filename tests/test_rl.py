from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.rl import discounted_returns


def test_discounted_returns_monotonic_example() -> None:
    returns = discounted_returns([1.0, 1.0, 1.0], gamma=0.5)
    assert np.allclose(returns, np.array([1.75, 1.5, 1.0], dtype=np.float32))
