from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_failure_modes import build_earthmoving_failure_modes


if __name__ == "__main__":
    payload = build_earthmoving_failure_modes(
        benchmark_summary_path=ROOT / "outputs" / "earthmoving_benchmark" / "earthmoving_summary.json",
        scale_summary_path=ROOT / "outputs" / "earthmoving_scale" / "scale_summary.json",
        replay_dir=ROOT / "outputs" / "earthmoving_replay",
        output_dir=ROOT / "outputs" / "earthmoving_failure_modes",
    )
    print(f"Wrote {payload['summary']['item_count']} earthmoving failure-mode items")
