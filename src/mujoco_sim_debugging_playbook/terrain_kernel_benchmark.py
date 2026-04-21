from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

import numpy as np

from mujoco_sim_debugging_playbook.provenance import write_manifest
from mujoco_sim_debugging_playbook.terrain import BladeState, SoilConfig, TerrainConfig, TerrainGrid, apply_blade_pass


def benchmark_terrain_kernels(
    *,
    repo_root: str | Path,
    output_dir: str | Path,
    repeats: int,
) -> dict[str, Any]:
    root = Path(repo_root)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    cxx = _run_cxx_kernel(root, repeats)
    python = _run_python_kernel(repeats)
    speedup = python["mean_ms"] / max(cxx["mean_ms"], 1e-12)
    payload = {
        "summary": {
            "repeats": repeats,
            "python_mean_ms": python["mean_ms"],
            "cxx_mean_ms": cxx["mean_ms"],
            "cxx_speedup": speedup,
            "moved_volume_delta": abs(python["moved_volume"] - cxx["moved_volume"]),
            "end_volume_delta": abs(python["end_volume"] - cxx["end_volume"]),
        },
        "python": python,
        "cxx": cxx,
    }
    summary_path = output / "terrain_kernel_benchmark.json"
    report_path = output / "report.md"
    summary_path.write_text(json.dumps(payload, indent=2))
    _write_report(payload, report_path)
    write_manifest(
        repo_root=root,
        output_dir=output,
        run_type="terrain_kernel_benchmark",
        config={"repeats": repeats},
        inputs=[root / "cpp" / "terrain_kernel.cpp"],
        outputs=[summary_path, report_path],
        metadata=payload["summary"],
    )
    return payload


def _run_cxx_kernel(root: Path, repeats: int) -> dict[str, float]:
    compiler = shutil.which("c++")
    if compiler is None:
        raise RuntimeError("c++ compiler not found")
    binary = Path("/tmp") / "mujoco_terrain_kernel_benchmark"
    subprocess.run(
        [compiler, "-std=c++17", "-O3", "-Wall", "-Wextra", "-pedantic", str(root / "cpp" / "terrain_kernel.cpp"), "-o", str(binary)],
        check=True,
    )
    completed = subprocess.run([str(binary), str(repeats)], check=True, capture_output=True, text=True)
    return _parse_key_values(completed.stdout)


def _run_python_kernel(repeats: int) -> dict[str, float]:
    result = {}
    start = time.perf_counter()
    for _ in range(repeats):
        terrain = TerrainGrid(
            TerrainConfig(
                x_range=(-0.55, 0.75),
                y_range=(-0.35, 0.35),
                resolution=(72, 40),
                base_height=0.0,
                pile_center=(-0.18, 0.0),
                pile_radius=0.22,
                pile_height=0.12,
            )
        )
        path = [
            BladeState(x=-0.42, y=0.0, yaw=0.0, width=0.2, depth=0.014),
            BladeState(x=-0.14, y=0.0, yaw=0.0, width=0.2, depth=0.014),
            BladeState(x=0.14, y=0.0, yaw=0.0, width=0.2, depth=0.014),
            BladeState(x=0.44, y=0.0, yaw=0.0, width=0.2, depth=0.014),
        ]
        result = apply_blade_pass(
            terrain,
            path,
            SoilConfig(cohesion=0.12, friction_angle_deg=30.0, compaction_rate=0.06, blade_coupling=0.8, spillover_rate=0.22),
        )
        end_volume = terrain.volume()
    elapsed_ms = (time.perf_counter() - start) * 1000.0
    return {
        "repeats": float(repeats),
        "elapsed_ms": elapsed_ms,
        "mean_ms": elapsed_ms / repeats,
        "start_volume": float(result["start_volume"]),
        "end_volume": float(end_volume),
        "moved_volume": float(result["moved_volume"]),
    }


def _parse_key_values(stdout: str) -> dict[str, float]:
    values = {}
    for line in stdout.splitlines():
        key, value = line.split("=")
        values[key] = float(value)
    return values


def _write_report(payload: dict[str, Any], output_path: Path) -> None:
    summary = payload["summary"]
    lines = [
        "# Terrain Kernel Benchmark",
        "",
        f"Repeats: `{summary['repeats']}`",
        f"Python mean: `{summary['python_mean_ms']:.6f}` ms",
        f"C++ mean: `{summary['cxx_mean_ms']:.6f}` ms",
        f"C++ speedup: `{summary['cxx_speedup']:.2f}x`",
        f"Moved-volume delta: `{summary['moved_volume_delta']:.8f}`",
        f"End-volume delta: `{summary['end_volume_delta']:.8f}`",
        "",
        "| kernel | elapsed_ms | mean_ms | moved_volume | end_volume |",
        "| --- | ---: | ---: | ---: | ---: |",
        f"| Python | {payload['python']['elapsed_ms']:.6f} | {payload['python']['mean_ms']:.6f} | {payload['python']['moved_volume']:.8f} | {payload['python']['end_volume']:.8f} |",
        f"| C++ | {payload['cxx']['elapsed_ms']:.6f} | {payload['cxx']['mean_ms']:.6f} | {payload['cxx']['moved_volume']:.8f} | {payload['cxx']['end_volume']:.8f} |",
    ]
    output_path.write_text("\n".join(lines))
