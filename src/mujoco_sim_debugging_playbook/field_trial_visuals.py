from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from mujoco_sim_debugging_playbook.provenance import write_manifest


def build_field_trial_visuals(
    *,
    benchmark_summary_path: str | Path,
    jobsite_eval_path: str | Path,
    replay_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    benchmark = _read_json(benchmark_summary_path)
    jobsite = _read_json(jobsite_eval_path)
    replay = _read_json(replay_path)
    scenario = replay["scenario"]
    result = _find(benchmark["results"], "scenario", scenario)
    jobsite_row = _find(jobsite["rows"], "scenario", scenario)

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    terrain_path = output / f"{scenario}_terrain_delta.png"
    productivity_path = output / "jobsite_productivity_bottleneck.png"
    _plot_terrain_delta(result, replay, terrain_path)
    _plot_productivity(jobsite, productivity_path)

    payload = {
        "scenario": scenario,
        "summary": {
            "decision": jobsite_row["decision"],
            "bottleneck": jobsite_row["bottleneck"],
            "productivity_m3_per_hr": jobsite_row["productivity_m3_per_hr"],
            "target_capture_ratio": jobsite_row["target_capture_ratio"],
        },
        "plots": {
            "terrain_delta": str(terrain_path),
            "productivity_bottleneck": str(productivity_path),
        },
    }
    json_path = output / "field_trial_visuals.json"
    md_path = output / "field_trial_visuals.md"
    json_path.write_text(json.dumps(payload, indent=2))
    md_path.write_text(render_field_trial_visuals(payload))
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="field_trial_visuals",
        config={"scenario": scenario},
        inputs=[benchmark_summary_path, jobsite_eval_path, replay_path],
        outputs=[json_path, md_path, terrain_path, productivity_path],
        metadata=payload["summary"],
    )
    return payload


def render_field_trial_visuals(payload: dict[str, Any]) -> str:
    scenario = payload["scenario"]
    summary = payload["summary"]
    return "\n".join(
        [
            f"# Field Trial Visuals: {scenario}",
            "",
            f"- Decision: `{summary['decision']}`",
            f"- Bottleneck: `{summary['bottleneck']}`",
            f"- Productivity: `{summary['productivity_m3_per_hr']:.2f}` m3/hr",
            f"- Target capture: `{summary['target_capture_ratio']:.3f}`",
            "",
            "## Terrain Delta And Blade Path",
            "",
            f"![Terrain delta and blade path]({Path(payload['plots']['terrain_delta']).name})",
            "",
            "## Jobsite Productivity Bottleneck",
            "",
            f"![Jobsite productivity bottleneck]({Path(payload['plots']['productivity_bottleneck']).name})",
        ]
    )


def _plot_terrain_delta(result: dict[str, Any], replay: dict[str, Any], path: Path) -> None:
    initial = result["initial_terrain"]
    final = result["final_terrain"]
    target = result["target_terrain"]
    xs = np.asarray(final["xs"])
    ys = np.asarray(final["ys"])
    delta = np.asarray(final["heights"]) - np.asarray(initial["heights"])
    target_delta = np.asarray(target["heights"]) - np.asarray(initial["heights"])
    blade_path = replay["blade_path"]
    blade_x = [state["x"] for state in blade_path]
    blade_y = [state["y"] for state in blade_path]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharex=True, sharey=True, constrained_layout=True)
    vmax = max(float(np.max(np.abs(delta))), float(np.max(np.abs(target_delta))), 1e-6)
    for axis, values, title in [
        (axes[0], delta, "Simulated terrain delta"),
        (axes[1], target_delta, "Target terrain delta"),
    ]:
        mesh = axis.pcolormesh(xs, ys, values.T, shading="auto", cmap="coolwarm", vmin=-vmax, vmax=vmax)
        axis.plot(blade_x, blade_y, color="#111827", linewidth=2.0, label="blade path")
        axis.scatter([blade_x[0], blade_x[-1]], [blade_y[0], blade_y[-1]], color=["#047857", "#b91c1c"], s=32)
        axis.set_title(title)
        axis.set_xlabel("x (m)")
        axis.set_ylabel("y (m)")
        axis.grid(True, alpha=0.18)
    axes[0].legend(loc="upper left")
    fig.colorbar(mesh, ax=axes.ravel().tolist(), label="height delta (m)", shrink=0.86, pad=0.02)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _plot_productivity(jobsite: dict[str, Any], path: Path) -> None:
    rows = jobsite["rows"]
    target = jobsite["targets"]["min_productivity_m3_per_hr"]
    scenarios = [row["scenario"] for row in rows]
    productivity = [row["productivity_m3_per_hr"] for row in rows]
    colors = ["#1f7a5f" if value >= target else "#b45309" for value in productivity]

    fig, axis = plt.subplots(figsize=(8.5, 4.6))
    axis.bar(scenarios, productivity, color=colors)
    axis.axhline(target, color="#991b1b", linestyle="--", linewidth=1.8, label=f"target {target:.1f} m3/hr")
    axis.set_title("Jobsite productivity by scenario")
    axis.set_ylabel("scaled productivity (m3/hr)")
    axis.tick_params(axis="x", rotation=18)
    axis.grid(True, axis="y", alpha=0.28)
    axis.legend(loc="upper right")
    for index, row in enumerate(rows):
        axis.text(
            index,
            row["productivity_m3_per_hr"] + 0.12,
            row["bottleneck"].replace("_", " "),
            ha="center",
            va="bottom",
            fontsize=8,
            color="#374151",
        )
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _find(rows: list[dict[str, Any]], key: str, value: str) -> dict[str, Any]:
    for row in rows:
        if row[key] == value:
            return row
    raise ValueError(f"could not find {key}={value}")


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())
