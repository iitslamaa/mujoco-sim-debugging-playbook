from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_review_packet import build_earthmoving_review_packet


def test_review_packet_rolls_up_earthmoving_outputs(tmp_path: Path) -> None:
    payload = build_earthmoving_review_packet(
        benchmark_summary_path=ROOT / "outputs" / "earthmoving_benchmark" / "earthmoving_summary.json",
        calibration_summary_path=ROOT / "outputs" / "earthmoving_calibration" / "calibration_summary.json",
        scale_summary_path=ROOT / "outputs" / "earthmoving_scale" / "scale_summary.json",
        sensitivity_summary_path=ROOT / "outputs" / "earthmoving_sensitivity" / "sensitivity_summary.json",
        gate_path=ROOT / "outputs" / "earthmoving_gate" / "earthmoving_gate.json",
        gap_report_path=ROOT / "outputs" / "earthmoving_gap" / "gap_report.json",
        output_dir=tmp_path / "review",
    )

    assert payload["summary"]["gate_status"] == "pass"
    assert payload["summary"]["scenario_count"] == 3
    assert payload["readiness_signals"]
    assert payload["top_sensitivities"]
    assert (tmp_path / "review" / "review_packet.json").exists()
    assert (tmp_path / "review" / "review_packet.md").exists()
