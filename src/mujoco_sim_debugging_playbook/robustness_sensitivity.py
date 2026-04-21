from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from mujoco_sim_debugging_playbook.provenance import write_manifest


def build_robustness_sensitivity(
    *,
    robustness_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    robustness = _read_json(robustness_path)
    rows = robustness["rows"]
    sensitivities = _sensitivities(rows)
    payload = {
        "candidate": robustness["candidate"],
        "scenario": robustness["scenario"],
        "summary": {
            "episode_count": robustness["summary"]["episode_count"],
            "top_driver": sensitivities[0] if sensitivities else None,
            "pass_rate": robustness["summary"]["pass_rate"],
        },
        "sensitivities": sensitivities,
        "recommendations": _recommendations(sensitivities),
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "robustness_sensitivity.json"
    md_path = output / "robustness_sensitivity.md"
    json_path.write_text(json.dumps(payload, indent=2))
    md_path.write_text(render_robustness_sensitivity(payload))
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="robustness_sensitivity",
        config={},
        inputs=[robustness_path],
        outputs=[json_path, md_path],
        metadata=payload["summary"],
    )
    return payload


def render_robustness_sensitivity(payload: dict[str, Any]) -> str:
    top = payload["summary"]["top_driver"]
    lines = [
        "# Robustness Sensitivity",
        "",
        f"Scenario: `{payload['scenario']}`",
        f"Candidate: `{payload['candidate']}`",
        f"Episodes: `{payload['summary']['episode_count']}`",
        f"Pass rate: `{payload['summary']['pass_rate']:.0%}`",
    ]
    if top:
        lines.append(
            f"Top productivity driver: `{top['input']}` with correlation `{top['productivity_correlation']:.3f}`."
        )
    lines.extend(
        [
            "",
            "## Ranked Inputs",
            "",
            "| input | productivity_correlation | pass_margin_correlation |",
            "| --- | ---: | ---: |",
        ]
    )
    for row in payload["sensitivities"]:
        lines.append(
            f"| {row['input']} | {row['productivity_correlation']:.3f} | {row['pass_margin_correlation']:.3f} |"
        )
    lines.extend(["", "## Recommendations", ""])
    for item in payload["recommendations"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


def _sensitivities(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    productivity = np.asarray([row["productivity_m3_per_hr"] for row in rows], dtype=float)
    pass_margin = np.asarray([1.0 if row["decision"] == "release_candidate" else 0.0 for row in rows], dtype=float)
    fields = {
        "soil.cohesion": [row["soil"]["cohesion"] for row in rows],
        "soil.friction_angle_deg": [row["soil"]["friction_angle_deg"] for row in rows],
        "soil.compaction_rate": [row["soil"]["compaction_rate"] for row in rows],
        "soil.blade_coupling": [row["soil"]["blade_coupling"] for row in rows],
        "soil.spillover_rate": [row["soil"]["spillover_rate"] for row in rows],
        "machine.blade_speed_mps": [row["machine_variant"]["blade_speed_mps"] for row in rows],
        "machine.return_speed_mps": [row["machine_variant"]["return_speed_mps"] for row in rows],
        "machine.turnaround_s": [row["machine_variant"]["turnaround_s"] for row in rows],
        "machine.dump_settle_s": [row["machine_variant"]["dump_settle_s"] for row in rows],
    }
    results = []
    for name, values in fields.items():
        values_array = np.asarray(values, dtype=float)
        results.append(
            {
                "input": name,
                "productivity_correlation": _corr(values_array, productivity),
                "pass_margin_correlation": _corr(values_array, pass_margin),
            }
        )
    results.sort(key=lambda row: abs(row["productivity_correlation"]), reverse=True)
    return results


def _recommendations(sensitivities: list[dict[str, Any]]) -> list[str]:
    if not sensitivities:
        return ["Collect more robustness episodes before ranking sensitivity drivers."]
    top = sensitivities[0]
    direction = "increase" if top["productivity_correlation"] > 0 else "decrease"
    return [
        f"Prioritize measurement and control of `{top['input']}`; productivity tends to {direction} as it rises.",
        "Rerun the robustness sweep after tuning the top driver to verify pass-rate improvement.",
        "Use the ranked inputs to decide which telemetry fields are worth collecting first on a real machine.",
    ]


def _corr(left: np.ndarray, right: np.ndarray) -> float:
    if left.size < 2 or right.size < 2:
        return 0.0
    if float(np.std(left)) <= 1e-12 or float(np.std(right)) <= 1e-12:
        return 0.0
    return float(np.corrcoef(left, right)[0, 1])


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())
