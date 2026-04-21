from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.terrain_kernel_benchmark import benchmark_terrain_kernels


if __name__ == "__main__":
    payload = benchmark_terrain_kernels(
        repo_root=ROOT,
        output_dir=ROOT / "outputs" / "terrain_kernel_benchmark",
        repeats=200,
    )
    print(f"C++ terrain kernel speedup: {payload['summary']['cxx_speedup']:.2f}x")
