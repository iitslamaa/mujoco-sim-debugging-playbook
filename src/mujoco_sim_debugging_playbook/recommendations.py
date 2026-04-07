from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text())


def build_recommendation_report(
    *,
    anomaly_report_path: str | Path,
    sweep_summary_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    anomalies = _read_json(anomaly_report_path)
    sweep_rows = _read_json(sweep_summary_path)

    recommendation_rows = []
    for case in anomalies["benchmark_anomalies"]["top_cases"][:5]:
        recommendation_rows.append(_recommend_for_benchmark_case(case, sweep_rows))
    for episode in anomalies["randomization_anomalies"]["episodes"][:5]:
        recommendation_rows.append(_recommend_for_randomized_episode(episode, sweep_rows))

    parameter_rankings = _parameter_rankings(sweep_rows)
    payload = {
        "recommendations": recommendation_rows,
        "parameter_rankings": parameter_rankings,
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "recommendations.json").write_text(json.dumps(payload, indent=2))
    _write_markdown(payload, output / "recommendations.md")
    return payload


def _recommend_for_benchmark_case(case: dict[str, Any], sweep_rows: list[dict[str, Any]]) -> dict[str, Any]:
    scenario = case["scenario"]
    if scenario == "low_damping_high_gain":
        sweep = _best_row_for_parameter(sweep_rows, "joint_damping")
        return {
            "kind": "benchmark_case",
            "target": f"{scenario} / {case['controller']}",
            "severity": float(case["risk_score"]),
            "recommendation": "Increase joint damping and reduce actuator gain before changing controller structure.",
            "evidence": (
                f"Highest benchmark risk is in `{scenario}`. Sweep evidence shows the best joint damping setting "
                f"in the playbook is `{sweep['value']}` with `{sweep['final_error_mean']:.4f}` final error."
            ),
            "tradeoff": "Higher damping reduces aggressiveness and may slightly slow settling.",
        }
    if scenario == "noise_heavy":
        sweep = _best_row_for_parameter(sweep_rows, "sensor_noise_std")
        return {
            "kind": "benchmark_case",
            "target": f"{scenario} / {case['controller']}",
            "severity": float(case["risk_score"]),
            "recommendation": "Add observation filtering or slightly lower controller aggressiveness under noisy sensing.",
            "evidence": (
                f"The noisy scenario is among the top anomaly cases. Sweep rows around sensor noise show best success at "
                f"`{sweep['value']}` with `{sweep['success_rate']:.3f}` success."
            ),
            "tradeoff": "Filtering helps stability but can add lag and reduce responsiveness.",
        }
    if scenario == "delay_heavy":
        sweep = _best_row_for_parameter(sweep_rows, "control_dt")
        return {
            "kind": "benchmark_case",
            "target": f"{scenario} / {case['controller']}",
            "severity": float(case["risk_score"]),
            "recommendation": "Increase control frequency or use a more delay-tolerant guarded policy blend.",
            "evidence": (
                f"Delay-heavy behavior is elevated in the benchmark, and the sweep suggests lower control_dt "
                f"(`{sweep['value']}`) gives the strongest success profile."
            ),
            "tradeoff": "Higher control frequency increases compute cost and can amplify noisy actuation if left untuned.",
        }
    sweep = _best_row_for_parameter(sweep_rows, "actuator_gain")
    return {
        "kind": "benchmark_case",
        "target": f"{scenario} / {case['controller']}",
        "severity": float(case["risk_score"]),
        "recommendation": "Retune actuator gain toward a lower-energy operating point and compare against the learned policy.",
        "evidence": (
            f"Actuator-gain sweeps peak at `{sweep['value']}` with `{sweep['success_rate']:.3f}` success "
            f"and `{sweep['control_energy_mean']:.2f}` control energy."
        ),
        "tradeoff": "Lower gain can improve stability but may underpower hard targets if reduced too far.",
    }


def _recommend_for_randomized_episode(episode: dict[str, Any], sweep_rows: list[dict[str, Any]]) -> dict[str, Any]:
    suggestions = []
    if episode["control_delay_steps"] >= 4:
        suggestions.append("reduce control delay or switch to the guarded/learned policy family")
    if episode["sensor_noise_std"] >= 0.01:
        suggestions.append("add observation smoothing")
    if episode["actuator_gain"] >= 45:
        suggestions.append("lower actuator gain")
    if episode["joint_damping"] <= 1.2:
        suggestions.append("raise joint damping")
    if not suggestions:
        suggestions.append("reproduce with the closest sweep setting and compare traces controller by controller")

    control_dt = _best_row_for_parameter(sweep_rows, "control_dt")
    return {
        "kind": "randomized_episode",
        "target": f"episode {episode['episode']}",
        "severity": float(episode["difficulty_score"]),
        "recommendation": "; ".join(suggestions).capitalize() + ".",
        "evidence": (
            f"This randomized episode had `{episode['success_rate']:.3f}` success rate with worst controller "
            f"`{episode['worst_controller']}`. The playbook's best control_dt sweep setting is `{control_dt['value']}`."
        ),
        "tradeoff": "Mitigations that improve robustness can trade off speed, energy, or nominal performance.",
    }


def _best_row_for_parameter(rows: list[dict[str, Any]], parameter: str) -> dict[str, Any]:
    parameter_rows = [row for row in rows if row["parameter"] == parameter]
    return sorted(parameter_rows, key=lambda row: (-row["success_rate"], row["final_error_mean"], row["control_energy_mean"]))[0]


def _parameter_rankings(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results = []
    for parameter in sorted({row["parameter"] for row in rows}):
        best = _best_row_for_parameter(rows, parameter)
        worst = sorted(
            [row for row in rows if row["parameter"] == parameter],
            key=lambda row: (row["success_rate"], -row["final_error_mean"], -row["control_energy_mean"]),
        )[0]
        results.append(
            {
                "parameter": parameter,
                "best_value": best["value"],
                "best_success_rate": float(best["success_rate"]),
                "worst_value": worst["value"],
                "worst_success_rate": float(worst["success_rate"]),
            }
        )
    return results


def _write_markdown(payload: dict[str, Any], path: str | Path) -> None:
    lines = [
        "# Mitigation Recommendations",
        "",
        "Recommended follow-up actions synthesized from anomaly analysis and sweep evidence.",
        "",
        "## Prioritized actions",
        "",
        "| target | severity | recommendation | tradeoff |",
        "| --- | ---: | --- | --- |",
    ]
    for row in payload["recommendations"]:
        lines.append(
            f"| {row['target']} | {row['severity']:.4f} | {row['recommendation']} | {row['tradeoff']} |"
        )

    lines.extend(["", "## Supporting evidence", ""])
    for row in payload["recommendations"]:
        lines.append(f"- `{row['target']}`: {row['evidence']}")

    lines.extend(["", "## Sweep parameter rankings", "", "| parameter | best_value | best_success_rate | worst_value | worst_success_rate |", "| --- | ---: | ---: | ---: | ---: |"])
    for row in payload["parameter_rankings"]:
        lines.append(
            f"| {row['parameter']} | {row['best_value']} | {row['best_success_rate']:.3f} | {row['worst_value']} | {row['worst_success_rate']:.3f} |"
        )

    Path(path).write_text("\n".join(lines))
