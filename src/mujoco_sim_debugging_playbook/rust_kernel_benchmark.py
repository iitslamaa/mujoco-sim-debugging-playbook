from __future__ import annotations

import ctypes
import json
import subprocess
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.provenance import write_manifest
from mujoco_sim_debugging_playbook.terrain_kernel_benchmark import _run_python_kernel


class KernelStats(ctypes.Structure):
    _fields_ = [
        ("repeats", ctypes.c_uint64),
        ("elapsed_ms", ctypes.c_double),
        ("mean_ms", ctypes.c_double),
        ("start_volume", ctypes.c_double),
        ("end_volume", ctypes.c_double),
        ("moved_volume", ctypes.c_double),
    ]


def benchmark_rust_terrain_kernel(
    *,
    repo_root: str | Path,
    output_dir: str | Path,
    repeats: int,
) -> dict[str, Any]:
    root = Path(repo_root)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    rust = _run_rust_ffi_kernel(root, repeats)
    python = _run_python_kernel(repeats)
    payload = {
        "summary": {
            "repeats": repeats,
            "python_mean_ms": python["mean_ms"],
            "rust_mean_ms": rust["mean_ms"],
            "rust_speedup": python["mean_ms"] / max(rust["mean_ms"], 1e-12),
            "moved_volume_delta": abs(python["moved_volume"] - rust["moved_volume"]),
            "end_volume_delta": abs(python["end_volume"] - rust["end_volume"]),
        },
        "python": python,
        "rust": rust,
    }
    summary_path = output / "rust_kernel_benchmark.json"
    report_path = output / "report.md"
    summary_path.write_text(json.dumps(payload, indent=2))
    _write_report(payload, report_path)
    write_manifest(
        repo_root=root,
        output_dir=output,
        run_type="rust_kernel_benchmark",
        config={"repeats": repeats},
        inputs=[root / "rust" / "terrain_kernel_ffi.rs"],
        outputs=[summary_path, report_path],
        metadata=payload["summary"],
    )
    return payload


def _run_rust_ffi_kernel(root: Path, repeats: int) -> dict[str, float]:
    rustc = find_rustc()
    if rustc is None:
        raise RuntimeError("rustc not found")
    dylib = _dylib_path()
    subprocess.run(
        [
            str(rustc),
            "--crate-type",
            "cdylib",
            "-C",
            "opt-level=3",
            str(root / "rust" / "terrain_kernel_ffi.rs"),
            "-o",
            str(dylib),
        ],
        check=True,
    )
    library = ctypes.CDLL(str(dylib))
    fn = library.run_terrain_kernel
    fn.argtypes = [ctypes.c_uint64, ctypes.POINTER(KernelStats)]
    fn.restype = ctypes.c_int
    stats = KernelStats()
    status = fn(repeats, ctypes.byref(stats))
    if status != 0:
        raise RuntimeError(f"Rust terrain kernel returned status {status}")
    return {
        "repeats": float(stats.repeats),
        "elapsed_ms": stats.elapsed_ms,
        "mean_ms": stats.mean_ms,
        "start_volume": stats.start_volume,
        "end_volume": stats.end_volume,
        "moved_volume": stats.moved_volume,
    }


def _dylib_path() -> Path:
    if ctypes.sizeof(ctypes.c_void_p) <= 0:
        raise RuntimeError("invalid pointer size")
    if __import__("sys").platform == "darwin":
        return Path("/tmp") / "libmujoco_rust_terrain_kernel.dylib"
    if __import__("sys").platform.startswith("win"):
        return Path("/tmp") / "mujoco_rust_terrain_kernel.dll"
    return Path("/tmp") / "libmujoco_rust_terrain_kernel.so"


def find_rustc() -> Path | None:
    import os
    import shutil

    path = shutil.which("rustc")
    if path:
        return Path(path)
    cargo_rustc = Path(os.environ.get("HOME", "")) / ".cargo" / "bin" / "rustc"
    if cargo_rustc.exists() and cargo_rustc.is_file():
        return cargo_rustc
    return None


def _write_report(payload: dict[str, Any], output_path: Path) -> None:
    summary = payload["summary"]
    lines = [
        "# Rust Terrain Kernel Benchmark",
        "",
        f"Repeats: `{summary['repeats']}`",
        f"Python mean: `{summary['python_mean_ms']:.6f}` ms",
        f"Rust mean: `{summary['rust_mean_ms']:.6f}` ms",
        f"Rust speedup: `{summary['rust_speedup']:.2f}x`",
        f"Moved-volume delta: `{summary['moved_volume_delta']:.8f}`",
        f"End-volume delta: `{summary['end_volume_delta']:.8f}`",
        "",
        "| kernel | elapsed_ms | mean_ms | moved_volume | end_volume |",
        "| --- | ---: | ---: | ---: | ---: |",
        f"| Python | {payload['python']['elapsed_ms']:.6f} | {payload['python']['mean_ms']:.6f} | {payload['python']['moved_volume']:.8f} | {payload['python']['end_volume']:.8f} |",
        f"| Rust FFI | {payload['rust']['elapsed_ms']:.6f} | {payload['rust']['mean_ms']:.6f} | {payload['rust']['moved_volume']:.8f} | {payload['rust']['end_volume']:.8f} |",
    ]
    output_path.write_text("\n".join(lines))
