from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.generalization import load_generalization_config


def test_load_generalization_config_reads_ranges() -> None:
    payload = load_generalization_config(ROOT / "configs" / "domain_randomization.json")
    assert payload["name"] == "domain_randomization"
    assert "joint_damping" in payload["ranges"]
