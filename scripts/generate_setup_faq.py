from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.setup_faq import build_setup_faq


def main() -> None:
    build_setup_faq(
        doctor_path=ROOT / "outputs" / "environment_doctor" / "doctor.json",
        compatibility_path=ROOT / "outputs" / "compatibility" / "compatibility.json",
        output_dir=ROOT / "outputs" / "setup_faq",
    )


if __name__ == "__main__":
    main()
