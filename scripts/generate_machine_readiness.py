from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.machine_readiness import build_machine_readiness


if __name__ == "__main__":
    build_machine_readiness(
        machine_profile_path=ROOT / "outputs" / "machine_profile" / "machine_profile.json",
        doctor_path=ROOT / "outputs" / "environment_doctor" / "doctor.json",
        compatibility_path=ROOT / "outputs" / "compatibility" / "compatibility.json",
        output_dir=ROOT / "outputs" / "machine_readiness",
    )
