from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "mujoco_sim_debugging_playbook_mpl"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from mujoco_sim_debugging_playbook.environment import capture_environment_report


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _mean_by_controller(rows: list[dict[str, Any]], metric: str) -> dict[str, float]:
    grouped: dict[str, list[float]] = {}
    for row in rows:
        grouped.setdefault(row["controller"], []).append(float(row[metric]))
    return {controller: float(np.mean(values)) for controller, values in grouped.items()}


def create_regression_snapshot(repo_root: str | Path, name: str) -> Path:
    root = Path(repo_root)
    snapshot_dir = root / "outputs" / "regression" / "snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    baseline = _read_json(root / "outputs" / "baseline" / "summary.json")["summary"]
    imitation = _read_json(root / "outputs" / "learning" / "evaluation" / "summary.json")["summary"]
    rl_eval = _read_json(root / "outputs" / "rl" / "evaluation" / "summary.json")["summary"]
    benchmark = _read_json(root / "outputs" / "controller_benchmark" / "benchmark_summary.json")["benchmark_rows"]
    randomization = _read_json(root / "outputs" / "domain_randomization" / "evaluation_rows.json")["rows"]

    payload = {
        "name": name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "environment": capture_environment_report(root),
        "metrics": {
            "baseline_success_rate": baseline["success_rate"],
            "baseline_final_error_mean": baseline["final_error_mean"],
            "imitation_success_rate": imitation["success_rate"],
            "imitation_final_error_mean": imitation["final_error_mean"],
            "rl_success_rate": rl_eval["success_rate"],
            "rl_final_error_mean": rl_eval["final_error_mean"],
            "benchmark_success_rate_by_controller": _mean_by_controller(benchmark, "success_rate"),
            "randomization_success_rate_by_controller": _mean_by_controller(randomization, "success"),
            "randomization_final_error_by_controller": _mean_by_controller(randomization, "final_error"),
        },
    }
    path = snapshot_dir / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2))
    return path


def compare_snapshots(left_path: str | Path, right_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    left = _read_json(left_path)
    right = _read_json(right_path)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    scalar_keys = [
        "baseline_success_rate",
        "baseline_final_error_mean",
        "imitation_success_rate",
        "imitation_final_error_mean",
        "rl_success_rate",
        "rl_final_error_mean",
    ]
    scalar_deltas = {
        key: float(right["metrics"][key] - left["metrics"][key])
        for key in scalar_keys
    }

    controller_delta = {}
    for metric_key in ["benchmark_success_rate_by_controller", "randomization_success_rate_by_controller", "randomization_final_error_by_controller"]:
        all_controllers = sorted(set(left["metrics"][metric_key]) | set(right["metrics"][metric_key]))
        controller_delta[metric_key] = {
            controller: float(right["metrics"][metric_key].get(controller, 0.0) - left["metrics"][metric_key].get(controller, 0.0))
            for controller in all_controllers
        }

    payload = {
        "left": left["name"],
        "right": right["name"],
        "scalar_deltas": scalar_deltas,
        "controller_deltas": controller_delta,
    }
    (output / "regression_diff.json").write_text(json.dumps(payload, indent=2))
    _write_markdown(payload, output / "regression_diff.md")
    _plot_regression(payload, output / "regression_diff.png")
    return payload


def load_regression_thresholds(path: str | Path) -> dict[str, Any]:
    return _read_json(path)


def evaluate_regression_diff(
    diff_payload: dict[str, Any],
    thresholds: dict[str, Any],
) -> dict[str, Any]:
    scalar_results = {}
    controller_results = {}
    violations: list[dict[str, Any]] = []

    for metric, delta in diff_payload.get("scalar_deltas", {}).items():
        threshold = thresholds.get("scalar_thresholds", {}).get(metric, {})
        result = _evaluate_delta(delta, threshold)
        scalar_results[metric] = result
        if not result["passed"]:
            violations.append(
                {
                    "scope": "scalar",
                    "metric": metric,
                    "delta": delta,
                    "rule": threshold,
                    "message": result["message"],
                }
            )

    for metric, controllers in diff_payload.get("controller_deltas", {}).items():
        metric_thresholds = thresholds.get("controller_thresholds", {}).get(metric, {})
        controller_results[metric] = {}
        for controller, delta in controllers.items():
            threshold = metric_thresholds.get(controller, metric_thresholds.get("*", {}))
            result = _evaluate_delta(delta, threshold)
            controller_results[metric][controller] = result
            if not result["passed"]:
                violations.append(
                    {
                        "scope": "controller",
                        "metric": metric,
                        "controller": controller,
                        "delta": delta,
                        "rule": threshold,
                        "message": result["message"],
                    }
                )

    return {
        "status": "pass" if not violations else "fail",
        "left": diff_payload["left"],
        "right": diff_payload["right"],
        "violation_count": len(violations),
        "violations": violations,
        "scalar_results": scalar_results,
        "controller_results": controller_results,
    }


def write_regression_gate_report(report: dict[str, Any], output_dir: str | Path) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "regression_gate.json").write_text(json.dumps(report, indent=2))
    _write_gate_markdown(report, output / "regression_gate.md")


def build_regression_history(
    snapshot_paths: list[str | Path],
    gate_reports: dict[str, dict[str, Any]] | None,
    output_dir: str | Path,
) -> dict[str, Any]:
    snapshots = [_read_json(path) for path in snapshot_paths]
    snapshots.sort(key=lambda item: item.get("created_at", item["name"]))

    scalar_metric_names = [
        "baseline_success_rate",
        "baseline_final_error_mean",
        "imitation_success_rate",
        "imitation_final_error_mean",
        "rl_success_rate",
        "rl_final_error_mean",
    ]
    series = {
        metric: [
            {
                "name": snapshot["name"],
                "created_at": snapshot.get("created_at"),
                "value": float(snapshot["metrics"][metric]),
            }
            for snapshot in snapshots
        ]
        for metric in scalar_metric_names
    }

    trend_summary = {
        metric: _summarize_trend(points)
        for metric, points in series.items()
    }

    gate_status = []
    for snapshot in snapshots:
        report = (gate_reports or {}).get(snapshot["name"])
        gate_status.append(
            {
                "name": snapshot["name"],
                "created_at": snapshot.get("created_at"),
                "status": report["status"] if report else "unknown",
                "violation_count": int(report["violation_count"]) if report else None,
            }
        )

    payload = {
        "snapshots": [
            {
                "name": snapshot["name"],
                "created_at": snapshot.get("created_at"),
            }
            for snapshot in snapshots
        ],
        "series": series,
        "trend_summary": trend_summary,
        "gate_status": gate_status,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "history.json").write_text(json.dumps(payload, indent=2))
    _write_history_markdown(payload, output / "history.md")
    _plot_history(payload, output / "history.png")
    return payload


def _evaluate_delta(delta: float, threshold: dict[str, Any]) -> dict[str, Any]:
    min_delta = threshold.get("min_delta")
    max_delta = threshold.get("max_delta")
    passed = True
    message = "within configured thresholds"

    if min_delta is not None and delta < float(min_delta):
        passed = False
        message = f"delta {delta:.4f} is below minimum allowed {float(min_delta):.4f}"
    if max_delta is not None and delta > float(max_delta):
        passed = False
        message = f"delta {delta:.4f} is above maximum allowed {float(max_delta):.4f}"

    return {
        "delta": float(delta),
        "min_delta": None if min_delta is None else float(min_delta),
        "max_delta": None if max_delta is None else float(max_delta),
        "passed": passed,
        "message": message,
    }


def _write_markdown(payload: dict[str, Any], path: str | Path) -> None:
    lines = [
        "# Regression Diff",
        "",
        f"Comparing `{payload['left']}` -> `{payload['right']}`.",
        "",
        "## Scalar deltas",
        "",
        "| metric | delta |",
        "| --- | ---: |",
    ]
    for key, value in payload["scalar_deltas"].items():
        lines.append(f"| {key} | {value:.4f} |")

    lines.extend(["", "## Controller deltas", ""])
    for metric_key, deltas in payload["controller_deltas"].items():
        lines.extend(
            [
                f"### {metric_key}",
                "",
                "| controller | delta |",
                "| --- | ---: |",
            ]
        )
        for controller, value in deltas.items():
            lines.append(f"| {controller} | {value:.4f} |")
        lines.append("")

    Path(path).write_text("\n".join(lines))


def _write_gate_markdown(report: dict[str, Any], path: str | Path) -> None:
    lines = [
        "# Regression Gate",
        "",
        f"Comparison: `{report['left']}` -> `{report['right']}`",
        "",
        f"Status: **{report['status'].upper()}**",
        "",
        f"Violation count: `{report['violation_count']}`",
        "",
    ]

    if report["violations"]:
        lines.extend(["## Violations", ""])
        for violation in report["violations"]:
            scope = violation["scope"]
            metric = violation["metric"]
            controller = violation.get("controller")
            target = f"{metric} / {controller}" if controller else metric
            lines.append(f"- `{scope}` `{target}`: {violation['message']}")
        lines.append("")
    else:
        lines.extend(["## Violations", "", "- None", ""])

    lines.extend(["## Scalar checks", "", "| metric | delta | min | max | passed |", "| --- | ---: | ---: | ---: | --- |"])
    for metric, result in report["scalar_results"].items():
        lines.append(
            f"| {metric} | {result['delta']:.4f} | {_fmt_limit(result['min_delta'])} | {_fmt_limit(result['max_delta'])} | {'yes' if result['passed'] else 'no'} |"
        )

    lines.extend(["", "## Controller checks", ""])
    for metric, controllers in report["controller_results"].items():
        lines.extend([f"### {metric}", "", "| controller | delta | min | max | passed |", "| --- | ---: | ---: | ---: | --- |"])
        for controller, result in controllers.items():
            lines.append(
                f"| {controller} | {result['delta']:.4f} | {_fmt_limit(result['min_delta'])} | {_fmt_limit(result['max_delta'])} | {'yes' if result['passed'] else 'no'} |"
            )
        lines.append("")

    Path(path).write_text("\n".join(lines))


def _fmt_limit(value: float | None) -> str:
    return "--" if value is None else f"{value:.4f}"


def _summarize_trend(points: list[dict[str, Any]]) -> dict[str, Any]:
    if not points:
        return {"direction": "unknown", "delta": 0.0, "latest": None}

    first_value = float(points[0]["value"])
    latest_value = float(points[-1]["value"])
    delta = latest_value - first_value
    if abs(delta) < 1e-9:
        direction = "flat"
    elif delta > 0:
        direction = "up"
    else:
        direction = "down"
    return {
        "direction": direction,
        "delta": float(delta),
        "latest": latest_value,
        "count": len(points),
    }


def _write_history_markdown(payload: dict[str, Any], path: str | Path) -> None:
    lines = [
        "# Regression History",
        "",
        "Tracked snapshots over time with scalar metric trends and gate outcomes.",
        "",
        "## Snapshots",
        "",
        "| name | created_at | gate status | violations |",
        "| --- | --- | --- | ---: |",
    ]
    gate_lookup = {entry["name"]: entry for entry in payload["gate_status"]}
    for snapshot in payload["snapshots"]:
        gate = gate_lookup.get(snapshot["name"], {})
        lines.append(
            f"| {snapshot['name']} | {snapshot.get('created_at', '--')} | {gate.get('status', 'unknown')} | {gate.get('violation_count', '--')} |"
        )

    lines.extend(["", "## Trend summary", "", "| metric | direction | delta | latest | count |", "| --- | --- | ---: | ---: | ---: |"])
    for metric, summary in payload["trend_summary"].items():
        latest = "--" if summary["latest"] is None else f"{summary['latest']:.4f}"
        lines.append(
            f"| {metric} | {summary['direction']} | {summary['delta']:.4f} | {latest} | {summary.get('count', 0)} |"
        )

    Path(path).write_text("\n".join(lines))


def _plot_history(payload: dict[str, Any], path: str | Path) -> None:
    metric_names = [
        "baseline_success_rate",
        "imitation_success_rate",
        "rl_success_rate",
        "baseline_final_error_mean",
        "imitation_final_error_mean",
        "rl_final_error_mean",
    ]
    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
    groups = [
        ("Success rate history", metric_names[:3], axes[0]),
        ("Final error history", metric_names[3:], axes[1]),
    ]
    x_labels = [snapshot["name"] for snapshot in payload["snapshots"]]
    x = np.arange(len(x_labels))
    palette = ["#0F9D58", "#3367D6", "#C85C2C"]

    for title, metrics, axis in groups:
        for index, metric in enumerate(metrics):
            values = [point["value"] for point in payload["series"][metric]]
            axis.plot(x, values, marker="o", linewidth=2.2, color=palette[index], label=metric)
        axis.set_title(title)
        axis.grid(True, alpha=0.25)
        axis.legend(frameon=False, fontsize=8)

    axes[-1].set_xticks(x, x_labels, rotation=20)
    fig.tight_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _plot_regression(payload: dict[str, Any], path: str | Path) -> None:
    labels = list(payload["scalar_deltas"].keys())
    values = [payload["scalar_deltas"][key] for key in labels]

    fig, axis = plt.subplots(figsize=(10, 4.8))
    colors = ["#0F9D58" if value >= 0 else "#C85C2C" for value in values]
    axis.bar(labels, values, color=colors)
    axis.axhline(0.0, color="black", linewidth=1)
    axis.set_title("Regression delta summary")
    axis.set_ylabel("Delta")
    axis.tick_params(axis="x", rotation=25)
    axis.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)
