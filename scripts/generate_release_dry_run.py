from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.release_dry_run import build_release_dry_run


if __name__ == "__main__":
    build_release_dry_run(
        release_blockers_path=ROOT / "outputs" / "release_blockers" / "release_blockers.json",
        machine_readiness_path=ROOT / "outputs" / "machine_readiness" / "machine_readiness.json",
        environment_alignment_path=ROOT / "outputs" / "environment_alignment" / "environment_alignment.json",
        output_dir=ROOT / "outputs" / "release_dry_run",
    )
