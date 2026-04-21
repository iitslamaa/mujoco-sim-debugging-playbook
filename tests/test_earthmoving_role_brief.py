from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_role_brief import build_earthmoving_role_brief


def test_role_brief_summarizes_fit_signals(tmp_path: Path) -> None:
    payload = build_earthmoving_role_brief(
        review_packet_path=ROOT / "outputs" / "earthmoving_review_packet" / "review_packet.json",
        dataset_summary_path=ROOT / "outputs" / "earthmoving_dataset" / "dataset_summary.json",
        failure_modes_path=ROOT / "outputs" / "earthmoving_failure_modes" / "failure_modes.json",
        output_dir=tmp_path / "brief",
    )

    assert "deformable terrain" in payload["headline"]
    assert payload["metrics"]["dataset_rows"] > 0
    assert payload["fit_signals"]
    assert payload["talking_points"]
    assert (tmp_path / "brief" / "role_brief.md").exists()
