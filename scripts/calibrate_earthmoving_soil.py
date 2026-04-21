from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_calibration import calibrate_earthmoving_soil


if __name__ == "__main__":
    result = calibrate_earthmoving_soil(
        benchmark_config_path=ROOT / "configs" / "earthmoving_benchmark.json",
        field_logs_path=ROOT / "configs" / "earthmoving_field_logs.json",
        output_dir=ROOT / "outputs" / "earthmoving_calibration",
    )
    print(f"Wrote earthmoving calibration artifacts to {result['output_dir']}")
