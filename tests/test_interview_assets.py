from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.interview_assets import build_interview_assets


def test_interview_assets_create_resume_and_screen_material(tmp_path: Path) -> None:
    payload = build_interview_assets(
        repo_root=ROOT,
        output_dir=tmp_path / "interview",
    )

    assert len(payload["resume_bullets"]) >= 3
    assert payload["phone_screen_story"]
    assert payload["questions_to_invite"]
    assert (tmp_path / "interview" / "interview_assets.md").exists()
