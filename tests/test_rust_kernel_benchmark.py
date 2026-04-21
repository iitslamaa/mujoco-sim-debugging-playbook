from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.rust_kernel_benchmark import benchmark_rust_terrain_kernel


def test_rust_kernel_benchmark_runs_when_rust_is_available(tmp_path: Path) -> None:
    if shutil.which("rustc") is None:
        return
    payload = benchmark_rust_terrain_kernel(
        repo_root=ROOT,
        output_dir=tmp_path / "rust_benchmark",
        repeats=5,
    )

    assert payload["summary"]["repeats"] == 5
    assert payload["summary"]["rust_speedup"] > 0.0
    assert payload["summary"]["moved_volume_delta"] >= 0.0
    assert (tmp_path / "rust_benchmark" / "rust_kernel_benchmark.json").exists()
    assert (tmp_path / "rust_benchmark" / "report.md").exists()
