from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.release_notes import _categorize_files


def test_categorize_files_groups_paths() -> None:
    payload = _categorize_files(
        [
            "README.md",
            "dashboard/app.js",
            "scripts/run_baseline.py",
            "src/mujoco_sim_debugging_playbook/simulation.py",
            "tests/test_release_notes.py",
            "outputs/provenance/index.json",
            ".github/workflows/ci.yml",
            "Makefile",
        ]
    )
    assert payload["docs"] == 1
    assert payload["dashboard"] == 1
    assert payload["scripts"] == 1
    assert payload["core_python"] == 1
    assert payload["tests"] == 1
    assert payload["outputs"] == 1
    assert payload["ci"] == 2
