from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_gate import evaluate_earthmoving_gate, write_earthmoving_gate_report


def test_earthmoving_gate_passes_current_artifacts(tmp_path: Path) -> None:
    report = evaluate_earthmoving_gate(
        benchmark_summary_path=ROOT / "outputs" / "earthmoving_benchmark" / "earthmoving_summary.json",
        thresholds_path=ROOT / "configs" / "earthmoving_thresholds.json",
        scale_summary_path=ROOT / "outputs" / "earthmoving_scale" / "scale_summary.json",
    )
    write_earthmoving_gate_report(report, tmp_path)

    assert report["status"] == "pass"
    assert report["violation_count"] == 0
    assert (tmp_path / "earthmoving_gate.json").exists()
    assert (tmp_path / "earthmoving_gate.md").exists()
