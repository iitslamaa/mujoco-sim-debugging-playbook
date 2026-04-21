from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_replay import build_earthmoving_replay_bundle


def test_replay_bundle_captures_scenario_debug_context(tmp_path: Path) -> None:
    bundle = build_earthmoving_replay_bundle(
        config_path=ROOT / "configs" / "earthmoving_benchmark.json",
        scenario_name="cohesive_soil",
        output_dir=tmp_path / "replay",
    )

    assert bundle["scenario"] == "cohesive_soil"
    assert bundle["metrics"]["moved_volume"] > 0.0
    assert bundle["terrain_stats"]["final"]["volume"] > 0.0
    assert bundle["debug_hypotheses"]
    assert (tmp_path / "replay" / "cohesive_soil_replay.json").exists()
    assert (tmp_path / "replay" / "cohesive_soil_replay.md").exists()
