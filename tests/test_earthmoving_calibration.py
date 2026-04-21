from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_calibration import calibrate_earthmoving_soil, load_field_logs


def test_load_field_logs_has_observations() -> None:
    logs = load_field_logs(ROOT / "configs" / "earthmoving_field_logs.json")
    assert logs["name"] == "earthmoving_field_logs"
    assert logs["logs"][0]["observed_moved_volume"] > 0.0


def test_calibration_writes_best_fit_rows(tmp_path: Path) -> None:
    result = calibrate_earthmoving_soil(
        benchmark_config_path=ROOT / "configs" / "earthmoving_benchmark.json",
        field_logs_path=ROOT / "configs" / "earthmoving_field_logs.json",
        output_dir=tmp_path / "calibration",
    )

    assert len(result["rows"]) == 2
    assert result["rows"][0]["calibration_error"] >= 0.0
    assert (Path(result["output_dir"]) / "calibration_summary.json").exists()
    assert (Path(result["output_dir"]) / "report.md").exists()
