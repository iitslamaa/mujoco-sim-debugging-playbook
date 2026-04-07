from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.benchmark import load_benchmark_config


def test_load_benchmark_config_has_scenarios() -> None:
    payload = load_benchmark_config(ROOT / "configs" / "controller_benchmark.json")
    assert payload["name"] == "controller_benchmark"
    assert len(payload["scenarios"]) >= 3
