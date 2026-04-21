from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_gap import build_earthmoving_gap_report


if __name__ == "__main__":
    payload = build_earthmoving_gap_report(
        calibration_summary_path=ROOT / "outputs" / "earthmoving_calibration" / "calibration_summary.json",
        sensitivity_summary_path=ROOT / "outputs" / "earthmoving_sensitivity" / "sensitivity_summary.json",
        output_dir=ROOT / "outputs" / "earthmoving_gap",
    )
    print(
        "Wrote earthmoving gap report with "
        f"{payload['summary']['scenario_count']} scenarios and "
        f"{payload['summary']['mean_calibration_error']:.3f} mean calibration error"
    )
