from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.rust_kernel_benchmark import benchmark_rust_terrain_kernel


if __name__ == "__main__":
    if shutil.which("rustc") is None:
        print("rustc not found; install Rust to run the Rust terrain-kernel benchmark")
        raise SystemExit(0)
    payload = benchmark_rust_terrain_kernel(
        repo_root=ROOT,
        output_dir=ROOT / "outputs" / "rust_kernel_benchmark",
        repeats=200,
    )
    print(f"Rust terrain kernel speedup: {payload['summary']['rust_speedup']:.2f}x")
