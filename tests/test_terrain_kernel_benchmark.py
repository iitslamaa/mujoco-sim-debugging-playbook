from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.terrain_kernel_benchmark import benchmark_terrain_kernels


def test_terrain_kernel_benchmark_compares_python_and_cpp(tmp_path: Path) -> None:
    if shutil.which("c++") is None:
        return
    payload = benchmark_terrain_kernels(
        repo_root=ROOT,
        output_dir=tmp_path / "kernel_benchmark",
        repeats=5,
    )

    assert payload["summary"]["repeats"] == 5
    assert payload["summary"]["cxx_speedup"] > 0.0
    assert payload["summary"]["moved_volume_delta"] >= 0.0
    assert (tmp_path / "kernel_benchmark" / "terrain_kernel_benchmark.json").exists()
    assert (tmp_path / "kernel_benchmark" / "report.md").exists()
