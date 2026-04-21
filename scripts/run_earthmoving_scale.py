from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_scale import run_earthmoving_scale_study


if __name__ == "__main__":
    result = run_earthmoving_scale_study(
        config_path=ROOT / "configs" / "earthmoving_benchmark.json",
        output_dir=ROOT / "outputs" / "earthmoving_scale",
        episodes_per_scenario=20,
        seed=2026,
        workers=1,
        variation=0.25,
    )
    print(
        "Wrote earthmoving scale artifacts to "
        f"{result['output_dir']} at {result['summary']['episodes_per_second']:.2f} episodes/s"
    )
