from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def test_rust_terrain_kernel_builds_when_rust_is_available(tmp_path: Path) -> None:
    rustc = shutil.which("rustc")
    if rustc is None:
        return
    binary = tmp_path / "terrain_kernel_rs"
    subprocess.run(
        [rustc, "-C", "opt-level=3", str(ROOT / "rust" / "terrain_kernel.rs"), "-o", str(binary)],
        check=True,
    )
    completed = subprocess.run([str(binary), "3"], check=True, capture_output=True, text=True)
    values = {}
    for line in completed.stdout.splitlines():
        key, value = line.split("=")
        values[key] = float(value)
    assert values["repeats"] == 3.0
    assert values["moved_volume"] > 0.0
    assert values["mean_ms"] > 0.0
