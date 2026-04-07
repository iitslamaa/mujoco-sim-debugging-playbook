from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.learning import state_vector


def test_state_vector_shape_and_order() -> None:
    qpos = np.array([1.0, 2.0])
    qvel = np.array([3.0, 4.0])
    target = np.array([5.0, 6.0])
    desired = np.array([7.0, 8.0])
    vector = state_vector(qpos, qvel, target, desired)
    assert vector.shape == (10,)
    assert vector.tolist() == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 6.0, 6.0]
