from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_gap import build_earthmoving_gap_report


def test_gap_report_combines_calibration_and_sensitivity(tmp_path: Path) -> None:
    payload = build_earthmoving_gap_report(
        calibration_summary_path=ROOT / "outputs" / "earthmoving_calibration" / "calibration_summary.json",
        sensitivity_summary_path=ROOT / "outputs" / "earthmoving_sensitivity" / "sensitivity_summary.json",
        output_dir=tmp_path / "gap",
    )

    assert payload["summary"]["scenario_count"] == 2
    assert payload["items"][0]["recommended_action"]
    assert payload["top_sensitivities"]
    assert (tmp_path / "gap" / "gap_report.json").exists()
    assert (tmp_path / "gap" / "report.md").exists()
