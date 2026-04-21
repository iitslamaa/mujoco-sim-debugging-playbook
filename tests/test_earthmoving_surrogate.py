from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_surrogate import train_earthmoving_surrogate


def test_surrogate_trains_on_generated_dataset(tmp_path: Path) -> None:
    payload = train_earthmoving_surrogate(
        dataset_path=ROOT / "outputs" / "earthmoving_dataset" / "earthmoving_dataset.npz",
        output_dir=tmp_path / "surrogate",
        seed=3,
        test_fraction=0.25,
        ridge_alpha=1e-3,
    )

    assert payload["summary"]["train_rows"] > payload["summary"]["test_rows"]
    assert payload["summary"]["mean_mae"] >= 0.0
    assert len(payload["metrics"]) == payload["summary"]["label_count"]
    assert (tmp_path / "surrogate" / "surrogate_model.json").exists()
    assert (tmp_path / "surrogate" / "report.md").exists()
