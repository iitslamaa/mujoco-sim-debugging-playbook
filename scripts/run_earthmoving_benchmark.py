from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_benchmark import run_earthmoving_benchmark


if __name__ == "__main__":
    result = run_earthmoving_benchmark(ROOT / "configs" / "earthmoving_benchmark.json")
    print(f"Wrote earthmoving benchmark artifacts to {result['output_dir']}")
