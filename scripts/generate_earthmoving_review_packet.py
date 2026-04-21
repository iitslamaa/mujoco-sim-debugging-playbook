from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_review_packet import build_earthmoving_review_packet


if __name__ == "__main__":
    payload = build_earthmoving_review_packet(
        benchmark_summary_path=ROOT / "outputs" / "earthmoving_benchmark" / "earthmoving_summary.json",
        calibration_summary_path=ROOT / "outputs" / "earthmoving_calibration" / "calibration_summary.json",
        scale_summary_path=ROOT / "outputs" / "earthmoving_scale" / "scale_summary.json",
        sensitivity_summary_path=ROOT / "outputs" / "earthmoving_sensitivity" / "sensitivity_summary.json",
        gate_path=ROOT / "outputs" / "earthmoving_gate" / "earthmoving_gate.json",
        gap_report_path=ROOT / "outputs" / "earthmoving_gap" / "gap_report.json",
        output_dir=ROOT / "outputs" / "earthmoving_review_packet",
    )
    print(
        "Wrote earthmoving review packet "
        f"with gate status {payload['summary']['gate_status']} "
        f"and {payload['summary']['episodes_per_second']:.2f} episodes/s"
    )
