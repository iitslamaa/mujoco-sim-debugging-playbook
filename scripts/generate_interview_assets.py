from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.interview_assets import build_interview_assets


if __name__ == "__main__":
    payload = build_interview_assets(
        repo_root=ROOT,
        output_dir=ROOT / "outputs" / "interview_assets",
    )
    print(f"Wrote interview assets with {len(payload['resume_bullets'])} resume bullets")
