from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.native_kernel_matrix import build_native_kernel_matrix


if __name__ == "__main__":
    payload = build_native_kernel_matrix(
        repo_root=ROOT,
        output_dir=ROOT / "outputs" / "native_kernel_matrix",
        repeats=200,
    )
    print(f"Fastest terrain kernel: {payload['summary']['fastest_kernel']}")
