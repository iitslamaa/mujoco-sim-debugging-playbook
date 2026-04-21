from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_failure_modes import build_earthmoving_failure_modes


def test_failure_modes_rank_debug_items(tmp_path: Path) -> None:
    payload = build_earthmoving_failure_modes(
        benchmark_summary_path=ROOT / "outputs" / "earthmoving_benchmark" / "earthmoving_summary.json",
        scale_summary_path=ROOT / "outputs" / "earthmoving_scale" / "scale_summary.json",
        replay_dir=ROOT / "outputs" / "earthmoving_replay",
        output_dir=tmp_path / "failure_modes",
    )

    assert payload["summary"]["item_count"] > 0
    assert payload["items"][0]["score"] >= payload["items"][-1]["score"]
    assert payload["items"][0]["next_action"]
    assert (tmp_path / "failure_modes" / "failure_modes.json").exists()
    assert (tmp_path / "failure_modes" / "report.md").exists()
