from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.native_kernel_matrix import build_native_kernel_matrix


def test_native_kernel_matrix_reports_available_and_skipped_kernels(tmp_path: Path) -> None:
    payload = build_native_kernel_matrix(
        repo_root=ROOT,
        output_dir=tmp_path / "native_kernel_matrix",
        repeats=5,
    )

    assert "python" in payload["summary"]["available_kernels"]
    assert payload["summary"]["fastest_kernel"]
    assert payload["entries"][0]["kernel"] == "python"
    assert (tmp_path / "native_kernel_matrix" / "native_kernel_matrix.json").exists()
    assert (tmp_path / "native_kernel_matrix" / "report.md").exists()
