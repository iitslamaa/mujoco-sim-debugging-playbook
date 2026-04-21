from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_dataset import FEATURE_NAMES, LABEL_NAMES, generate_earthmoving_dataset


def test_dataset_generator_writes_ml_ready_arrays(tmp_path: Path) -> None:
    result = generate_earthmoving_dataset(
        config_path=ROOT / "configs" / "earthmoving_benchmark.json",
        output_dir=tmp_path / "dataset",
        episodes_per_scenario=2,
        seed=13,
        variation=0.15,
    )

    dataset_path = Path(result["output_dir"]) / "earthmoving_dataset.npz"
    payload = np.load(dataset_path)
    assert payload["features"].shape == (6, len(FEATURE_NAMES))
    assert payload["labels"].shape == (6, len(LABEL_NAMES))
    assert result["summary"]["row_count"] == 6
    assert (Path(result["output_dir"]) / "dataset_summary.json").exists()
    assert (Path(result["output_dir"]) / "report.md").exists()
