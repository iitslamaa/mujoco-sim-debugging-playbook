from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.machine_profile import build_machine_profile


if __name__ == "__main__":
    build_machine_profile(environment_report_path=ROOT / "outputs" / "diagnostics" / "environment.json", output_dir=ROOT / "outputs" / "machine_profile")
