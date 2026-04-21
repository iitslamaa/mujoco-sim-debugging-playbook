from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_surrogate import train_earthmoving_surrogate


if __name__ == "__main__":
    payload = train_earthmoving_surrogate(
        dataset_path=ROOT / "outputs" / "earthmoving_dataset" / "earthmoving_dataset.npz",
        output_dir=ROOT / "outputs" / "earthmoving_surrogate",
        seed=17,
        test_fraction=0.25,
        ridge_alpha=1e-3,
    )
    print(f"Wrote earthmoving surrogate with mean MAE {payload['summary']['mean_mae']:.6f}")
