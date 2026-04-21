from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.provenance import write_manifest


def build_field_trial_case_study(
    *,
    review_packet_path: str | Path,
    jobsite_eval_path: str | Path,
    replay_path: str | Path,
    gap_report_path: str | Path,
    plan_search_path: str | Path,
    multipass_eval_path: str | Path | None = None,
    visuals_path: str | Path | None = None,
    output_dir: str | Path,
) -> dict[str, Any]:
    review = _read_json(review_packet_path)
    jobsite = _read_json(jobsite_eval_path)
    replay = _read_json(replay_path)
    gap = _read_json(gap_report_path)
    plan = _read_json(plan_search_path)
    multipass = _read_json(multipass_eval_path) if multipass_eval_path and Path(multipass_eval_path).exists() else None
    visuals = _read_json(visuals_path) if visuals_path and Path(visuals_path).exists() else None

    scenario = replay["scenario"]
    jobsite_row = _find(jobsite["rows"], "scenario", scenario)
    review_row = _find(review["scenario_table"], "scenario", scenario)
    gap_item = _find(gap["items"], "scenario", scenario)
    best_plan = plan["summary"]["best_candidate"]
    payload = {
        "title": f"Field Trial Case Study: {scenario}",
        "scenario": scenario,
        "decision": jobsite_row["decision"],
        "executive_readout": _executive_readout(jobsite_row, review_row, gap_item, best_plan),
        "observations": _observations(replay, review_row, jobsite_row),
        "root_cause_hypotheses": _root_cause_hypotheses(replay, gap_item, jobsite_row),
        "next_experiment": _next_experiment(gap_item, best_plan, multipass),
        "acceptance_criteria": _acceptance_criteria(jobsite["targets"]),
        "multipass_eval": multipass,
        "visuals": visuals,
        "review_links": {
            "multipass_plan_eval": "../multipass_plan_eval/multipass_plan_eval.md",
            "field_trial_visuals": "../field_trial_visuals/field_trial_visuals.md",
            "jobsite_eval": "../jobsite_autonomy_eval/report.md",
            "review_packet": "../earthmoving_review_packet/review_packet.md",
            "replay_bundle": "../earthmoving_replay/cohesive_soil_replay.md",
            "gap_report": "../earthmoving_gap/report.md",
            "plan_search": "../earthmoving_plan_search/report.md",
        },
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "field_trial_case_study.json"
    md_path = output / "field_trial_case_study.md"
    json_path.write_text(json.dumps(payload, indent=2))
    md_path.write_text(render_field_trial_case_study(payload))
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="field_trial_case_study",
        config={"scenario": scenario},
        inputs=[
            review_packet_path,
            jobsite_eval_path,
            replay_path,
            gap_report_path,
            plan_search_path,
            *([multipass_eval_path] if multipass_eval_path else []),
            *([visuals_path] if visuals_path else []),
        ],
        outputs=[json_path, md_path],
        metadata={"scenario": scenario, "decision": jobsite_row["decision"]},
    )
    return payload


def render_field_trial_case_study(payload: dict[str, Any]) -> str:
    lines = [
        f"# {payload['title']}",
        "",
        f"Decision: `{payload['decision']}`",
        "",
        "## Executive Readout",
        "",
    ]
    for item in payload["executive_readout"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Observations", ""])
    for item in payload["observations"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Root-Cause Hypotheses", ""])
    for item in payload["root_cause_hypotheses"]:
        lines.append(f"- {item}")
    if payload.get("multipass_eval"):
        best = payload["multipass_eval"]["summary"]["best_candidate"]
        lines.extend(
            [
                "",
                "## Multi-Pass Evaluation",
                "",
                f"- Best evaluated sequence: `{best['candidate']}`",
                f"- Decision: `{best['decision']}`",
                f"- Productivity: `{best['productivity_m3_per_hr']:.2f}` m3/hr",
                f"- Target capture: `{best['target_capture_ratio']:.3f}`",
                f"- Terrain RMSE: `{best['terrain_profile_rmse']:.6f}`",
            ]
        )
    lines.extend(["", "## Next Experiment", ""])
    for item in payload["next_experiment"]:
        lines.append(f"- {item}")
    if payload.get("visuals"):
        lines.extend(
            [
                "",
                "## Visual Review",
                "",
                "![Terrain delta and blade path](../field_trial_visuals/cohesive_soil_terrain_delta.png)",
                "",
                "![Jobsite productivity bottleneck](../field_trial_visuals/jobsite_productivity_bottleneck.png)",
            ]
        )
    lines.extend(["", "## Acceptance Criteria", ""])
    for item in payload["acceptance_criteria"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Review Links", ""])
    for label, path in payload["review_links"].items():
        lines.append(f"- `{label}`: [{path}]({path})")
    return "\n".join(lines)


def _executive_readout(
    jobsite_row: dict[str, Any],
    review_row: dict[str, Any],
    gap_item: dict[str, Any],
    best_plan: dict[str, Any],
) -> list[str]:
    return [
        f"The scenario is marked `{jobsite_row['decision']}` because `{jobsite_row['bottleneck']}` is the current deployment bottleneck.",
        f"Simulated productivity is `{jobsite_row['productivity_m3_per_hr']:.2f}` m3/hr with cycle time `{jobsite_row['cycle_time_s']:.2f}` s.",
        f"Target capture is `{jobsite_row['target_capture_ratio']:.3f}`, while terrain RMSE is `{review_row['terrain_profile_rmse']:.6f}`.",
        f"The dominant sim-to-field gap is `{gap_item['dominant_gap_metric']}`; recommended action: {gap_item['recommended_action']}",
        f"The current blade-plan search suggests `{best_plan['candidate']}` as the best single-pass candidate.",
    ]


def _observations(replay: dict[str, Any], review_row: dict[str, Any], jobsite_row: dict[str, Any]) -> list[str]:
    metrics = replay["metrics"]
    soil = replay["soil"]
    return [
        f"Soil settings use cohesion `{soil['cohesion']:.2f}`, friction angle `{soil['friction_angle_deg']:.1f}` deg, and blade coupling `{soil['blade_coupling']:.2f}`.",
        f"Moved volume is `{metrics['moved_volume']:.6f}` with deposit forward progress `{metrics['deposit_forward_progress']:.4f}` m.",
        f"Volume conservation error is `{metrics['volume_conservation_error']:.6f}`, so the immediate concern is not volume accounting.",
        f"Rework risk is `{jobsite_row['rework_risk_score']:.2f}` and target-zone volume is `{review_row['target_zone_volume']:.6f}`.",
    ]


def _root_cause_hypotheses(
    replay: dict[str, Any],
    gap_item: dict[str, Any],
    jobsite_row: dict[str, Any],
) -> list[str]:
    hypotheses = list(replay["debug_hypotheses"])
    hypotheses.append(
        f"`{jobsite_row['bottleneck']}` is likely a task-design issue: one pass is too conservative for the configured productivity target."
    )
    hypotheses.append(
        f"`{gap_item['dominant_gap_metric']}` should be checked against richer before/after terrain measurements before changing model structure."
    )
    return hypotheses


def _next_experiment(
    gap_item: dict[str, Any],
    best_plan: dict[str, Any],
    multipass: dict[str, Any] | None,
) -> list[str]:
    items = [
        f"Run the best candidate `{best_plan['candidate']}` as a replay bundle and compare it against the current scenario baseline.",
        "Evaluate a two-pass cut/carry/dump sequence with the same target-zone objective and explicit cycle-time accounting.",
        f"Collect or synthesize richer observations for `{gap_item['dominant_gap_metric']}` and rerun calibration.",
        "Promote the experiment only if productivity improves without increasing terrain RMSE or volume residuals beyond gate thresholds.",
    ]
    if multipass:
        best = multipass["summary"]["best_candidate"]
        items[0] = (
            f"Run `{best['candidate']}` as a replay bundle and compare it against the current scenario baseline."
        )
        items[1] = (
            f"Use `{best['candidate']}` as the evaluated task-plan baseline and replay it with robustness sweeps."
        )
    return items


def _acceptance_criteria(targets: dict[str, float]) -> list[str]:
    return [
        f"Productivity at or above `{targets['min_productivity_m3_per_hr']:.2f}` m3/hr.",
        f"Target capture ratio at or above `{targets['min_target_capture_ratio']:.2f}`.",
        f"Terrain RMSE at or below `{targets['max_terrain_rmse']:.3f}`.",
        f"Volume conservation error at or below `{targets['max_volume_conservation_error']:.3f}`.",
        f"Deposit forward progress at or above `{targets['min_deposit_forward_progress_m']:.2f}` m.",
    ]


def _find(rows: list[dict[str, Any]], key: str, value: str) -> dict[str, Any]:
    for row in rows:
        if row[key] == value:
            return row
    raise ValueError(f"could not find {key}={value}")


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())
