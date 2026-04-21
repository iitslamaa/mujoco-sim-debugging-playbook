from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.provenance import write_manifest
from mujoco_sim_debugging_playbook.rust_kernel_benchmark import _run_rust_ffi_kernel
from mujoco_sim_debugging_playbook.terrain_kernel_benchmark import _run_cxx_kernel, _run_python_kernel


def build_native_kernel_matrix(
    *,
    repo_root: str | Path,
    output_dir: str | Path,
    repeats: int,
) -> dict[str, Any]:
    root = Path(repo_root)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    python = _entry("python", "available", _run_python_kernel(repeats), None)
    entries = [python]
    for name, runner in [
        ("cxx", lambda: _run_cxx_kernel(root, repeats)),
        ("rust_ffi", lambda: _run_rust_ffi_kernel(root, repeats)),
    ]:
        try:
            entries.append(_entry(name, "available", runner(), None))
        except Exception as exc:
            entries.append(_entry(name, "skipped", None, str(exc)))

    python_mean = python["mean_ms"]
    for entry in entries:
        if entry["status"] == "available":
            entry["speedup_vs_python"] = python_mean / max(entry["mean_ms"], 1e-12)
            entry["moved_volume_delta_vs_python"] = abs(entry["moved_volume"] - python["moved_volume"])
            entry["end_volume_delta_vs_python"] = abs(entry["end_volume"] - python["end_volume"])

    payload = {
        "summary": {
            "repeats": repeats,
            "available_kernels": [entry["kernel"] for entry in entries if entry["status"] == "available"],
            "skipped_kernels": [entry["kernel"] for entry in entries if entry["status"] == "skipped"],
            "fastest_kernel": min(
                [entry for entry in entries if entry["status"] == "available"],
                key=lambda item: item["mean_ms"],
            )["kernel"],
        },
        "entries": entries,
    }
    summary_path = output / "native_kernel_matrix.json"
    report_path = output / "report.md"
    summary_path.write_text(json.dumps(payload, indent=2))
    _write_report(payload, report_path)
    write_manifest(
        repo_root=root,
        output_dir=output,
        run_type="native_kernel_matrix",
        config={"repeats": repeats},
        inputs=[root / "cpp" / "terrain_kernel.cpp", root / "rust" / "terrain_kernel_ffi.rs"],
        outputs=[summary_path, report_path],
        metadata=payload["summary"],
    )
    return payload


def _entry(kernel: str, status: str, result: dict[str, float] | None, reason: str | None) -> dict[str, Any]:
    if result is None:
        return {"kernel": kernel, "status": status, "reason": reason}
    return {
        "kernel": kernel,
        "status": status,
        "repeats": result["repeats"],
        "elapsed_ms": result["elapsed_ms"],
        "mean_ms": result["mean_ms"],
        "moved_volume": result["moved_volume"],
        "end_volume": result["end_volume"],
    }


def _write_report(payload: dict[str, Any], output_path: Path) -> None:
    lines = [
        "# Native Terrain Kernel Matrix",
        "",
        f"Repeats: `{payload['summary']['repeats']}`",
        f"Available kernels: `{', '.join(payload['summary']['available_kernels'])}`",
        f"Skipped kernels: `{', '.join(payload['summary']['skipped_kernels']) or 'none'}`",
        f"Fastest available kernel: `{payload['summary']['fastest_kernel']}`",
        "",
        "| kernel | status | mean_ms | speedup_vs_python | moved_delta | end_delta | reason |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for entry in payload["entries"]:
        lines.append(
            f"| {entry['kernel']} | {entry['status']} | "
            f"{_fmt(entry.get('mean_ms'))} | {_fmt(entry.get('speedup_vs_python'))} | "
            f"{_fmt(entry.get('moved_volume_delta_vs_python'))} | {_fmt(entry.get('end_volume_delta_vs_python'))} | "
            f"{entry.get('reason', '')} |"
        )
    output_path.write_text("\n".join(lines))


def _fmt(value: Any) -> str:
    if value is None:
        return ""
    return f"{float(value):.6f}"
