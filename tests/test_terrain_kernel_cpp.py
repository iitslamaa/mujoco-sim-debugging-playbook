from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def test_cpp_terrain_kernel_builds_and_moves_material(tmp_path: Path) -> None:
    compiler = shutil.which("c++")
    if compiler is None:
        return
    binary = tmp_path / "terrain_kernel"
    subprocess.run(
        [compiler, "-std=c++17", "-O2", str(ROOT / "cpp" / "terrain_kernel.cpp"), "-o", str(binary)],
        check=True,
    )
    completed = subprocess.run([str(binary)], check=True, capture_output=True, text=True)
    values = {}
    for line in completed.stdout.splitlines():
        key, value = line.split("=")
        values[key] = float(value)
    assert values["moved_volume"] > 0.0
    assert values["end_volume"] > 0.0
