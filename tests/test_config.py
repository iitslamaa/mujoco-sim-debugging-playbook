from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.config import load_experiment_config


def test_load_experiment_config_reads_expected_fields() -> None:
    config = load_experiment_config(ROOT / "configs" / "baseline.json")
    assert config.name == "baseline"
    assert config.sim.control_dt == 0.02
    assert config.task.link_lengths == (0.18, 0.16)

