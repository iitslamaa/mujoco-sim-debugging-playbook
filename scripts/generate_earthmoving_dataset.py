from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_dataset import generate_earthmoving_dataset


if __name__ == "__main__":
    result = generate_earthmoving_dataset(
        config_path=ROOT / "configs" / "earthmoving_benchmark.json",
        output_dir=ROOT / "outputs" / "earthmoving_dataset",
        episodes_per_scenario=18,
        seed=909,
        variation=0.3,
    )
    print(f"Wrote earthmoving dataset with {result['summary']['row_count']} rows to {result['output_dir']}")
