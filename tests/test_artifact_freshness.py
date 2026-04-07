from pathlib import Path
import time

from mujoco_sim_debugging_playbook.artifact_freshness import build_artifact_freshness


def test_artifact_freshness_marks_stale_and_missing(tmp_path: Path):
    ref = tmp_path / "src.txt"
    fresh = tmp_path / "fresh.json"
    stale = tmp_path / "stale.json"
    ref.write_text("ref")
    time.sleep(0.01)
    fresh.write_text("{}")
    stale.write_text("{}")
    older = ref.stat().st_mtime - 5
    stale.touch()
    import os
    os.utime(stale, (older, older))

    payload = build_artifact_freshness(
        root=tmp_path,
        artifact_paths=["fresh.json", "stale.json", "missing.json"],
        reference_paths=["src.txt"],
    )
    statuses = {row["artifact"]: row["status"] for row in payload["rows"]}
    assert statuses["fresh.json"] == "fresh"
    assert statuses["stale.json"] == "stale"
    assert statuses["missing.json"] == "missing"
