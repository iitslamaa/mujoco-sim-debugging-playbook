from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.application_readiness import build_application_readiness


if __name__ == "__main__":
    payload = build_application_readiness(
        repo_root=ROOT,
        bundle_path=ROOT / "outputs" / "application_bundle" / "application_bundle.json",
        output_dir=ROOT / "outputs" / "application_readiness",
    )
    print(f"Wrote application readiness gate: {payload['summary']['status']}")
