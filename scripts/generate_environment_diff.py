from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.environment_diff import build_environment_diff


def main() -> None:
    build_environment_diff(
        doctor_path=ROOT / "outputs" / "environment_doctor" / "doctor.json",
        compatibility_path=ROOT / "outputs" / "compatibility" / "compatibility.json",
        output_dir=ROOT / "outputs" / "environment_diff",
    )


if __name__ == "__main__":
    main()
