from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.repro_readiness import build_repro_readiness


if __name__ == "__main__":
    build_repro_readiness(
        repro_bundle_index_path=ROOT / "outputs" / "repro_bundle_index" / "repro_bundle_index.json",
        support_intake_checklist_path=ROOT / "outputs" / "support_intake_checklist" / "support_intake_checklist.json",
        output_dir=ROOT / "outputs" / "repro_readiness",
    )
