from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_sensitivity import run_earthmoving_sensitivity


if __name__ == "__main__":
    result = run_earthmoving_sensitivity(
        config_path=ROOT / "configs" / "earthmoving_benchmark.json",
        output_dir=ROOT / "outputs" / "earthmoving_sensitivity",
        episodes_per_scenario=24,
        seed=404,
        variation=0.3,
    )
    top = result["summary"]["top_sensitivity"]
    print(f"Wrote earthmoving sensitivity artifacts to {result['output_dir']}")
    print(f"Top sensitivity: {top['soil_parameter']} -> {top['metric']} ({top['pearson_correlation']:.3f})")
