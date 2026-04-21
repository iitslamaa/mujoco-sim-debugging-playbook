from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_earthmoving_thresholds(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def evaluate_earthmoving_gate(
    benchmark_summary_path: str | Path,
    thresholds_path: str | Path,
    scale_summary_path: str | Path | None = None,
) -> dict[str, Any]:
    benchmark = json.loads(Path(benchmark_summary_path).read_text())
    thresholds = load_earthmoving_thresholds(thresholds_path)
    violations = []
    scenario_results = []
    for row in benchmark["rows"]:
        metric_results = {}
        for metric, rule in thresholds.get("metric_thresholds", {}).items():
            result = _evaluate_value(float(row[metric]), rule)
            metric_results[metric] = result
            if not result["passed"]:
                violations.append(
                    {
                        "scope": "scenario",
                        "scenario": row["scenario"],
                        "metric": metric,
                        "value": row[metric],
                        "rule": rule,
                        "message": result["message"],
                    }
                )
        scenario_results.append({"scenario": row["scenario"], "metrics": metric_results})

    scale_results = {}
    if scale_summary_path is not None:
        scale = json.loads(Path(scale_summary_path).read_text())["summary"]
        for metric, rule in thresholds.get("scale_thresholds", {}).items():
            result = _evaluate_value(float(scale[metric]), rule)
            scale_results[metric] = result
            if not result["passed"]:
                violations.append(
                    {
                        "scope": "scale",
                        "metric": metric,
                        "value": scale[metric],
                        "rule": rule,
                        "message": result["message"],
                    }
                )

    return {
        "status": "pass" if not violations else "fail",
        "violation_count": len(violations),
        "violations": violations,
        "scenario_results": scenario_results,
        "scale_results": scale_results,
    }


def write_earthmoving_gate_report(report: dict[str, Any], output_dir: str | Path) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "earthmoving_gate.json").write_text(json.dumps(report, indent=2))
    _write_markdown(report, output / "earthmoving_gate.md")


def _evaluate_value(value: float, rule: dict[str, float]) -> dict[str, Any]:
    if "max" in rule and value > float(rule["max"]):
        return {"passed": False, "message": f"{value:.6f} is above max {rule['max']:.6f}"}
    if "min" in rule and value < float(rule["min"]):
        return {"passed": False, "message": f"{value:.6f} is below min {rule['min']:.6f}"}
    return {"passed": True, "message": "within threshold"}


def _write_markdown(report: dict[str, Any], output_path: Path) -> None:
    lines = [
        "# Earthmoving Quality Gate",
        "",
        f"Status: `{report['status']}`",
        f"Violations: `{report['violation_count']}`",
        "",
    ]
    if report["violations"]:
        lines.extend(["| scope | target | metric | value | message |", "| --- | --- | --- | ---: | --- |"])
        for violation in report["violations"]:
            target = violation.get("scenario", "scale")
            lines.append(
                f"| {violation['scope']} | {target} | {violation['metric']} | "
                f"{float(violation['value']):.6f} | {violation['message']} |"
            )
    else:
        lines.append("All earthmoving realism and throughput thresholds passed.")
    output_path.write_text("\n".join(lines))
