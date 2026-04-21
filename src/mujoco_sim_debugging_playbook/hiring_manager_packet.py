from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.provenance import write_manifest


def build_hiring_manager_packet(*, repo_root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    review = _read_json(root / "outputs" / "earthmoving_review_packet" / "review_packet.json")
    role_brief = _read_json(root / "outputs" / "earthmoving_role_brief" / "role_brief.json")
    jobsite = _read_json(root / "outputs" / "jobsite_autonomy_eval" / "jobsite_autonomy_eval.json")
    gap = _read_json(root / "outputs" / "earthmoving_gap" / "gap_report.json")
    plan = _read_json(root / "outputs" / "earthmoving_plan_search" / "plan_search.json")
    surrogate = _read_json(root / "outputs" / "earthmoving_surrogate" / "surrogate_model.json")
    kernel = _read_json(root / "outputs" / "terrain_kernel_benchmark" / "terrain_kernel_benchmark.json")
    case_study = _read_json(root / "outputs" / "field_trial_case_study" / "field_trial_case_study.json")
    visuals = _read_json(root / "outputs" / "field_trial_visuals" / "field_trial_visuals.json")
    multipass = _read_json(root / "outputs" / "multipass_plan_eval" / "multipass_plan_eval.json")
    robustness = _read_json(root / "outputs" / "task_plan_robustness" / "task_plan_robustness.json")
    sensitivity = _read_json(root / "outputs" / "robustness_sensitivity" / "robustness_sensitivity.json")

    payload = {
        "headline": "Autonomous earthmoving simulation validation packet",
        "one_sentence": (
            "A MuJoCo-based construction autonomy simulation track that connects deformable-terrain "
            "experiments to calibration, release gating, jobsite productivity, and native-kernel performance."
        ),
        "manager_summary": _manager_summary(
            review, jobsite, gap, plan, surrogate, kernel, case_study, multipass, robustness, sensitivity
        ),
        "architecture": _architecture(),
        "evidence": _evidence(
            review, role_brief, jobsite, gap, plan, surrogate, kernel, case_study, visuals, multipass, robustness, sensitivity
        ),
        "review_path": _review_path(),
        "technical_judgment": _technical_judgment(review, jobsite, gap),
        "limitations": _limitations(),
        "next_30_days": _next_30_days(),
        "outreach_note": _outreach_note(),
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "hiring_manager_packet.json"
    md_path = output / "hiring_manager_packet.md"
    json_path.write_text(json.dumps(payload, indent=2))
    md_path.write_text(render_hiring_manager_packet(payload))
    write_manifest(
        repo_root=root,
        output_dir=output,
        run_type="hiring_manager_packet",
        config={},
        inputs=[
            root / "outputs" / "earthmoving_review_packet" / "review_packet.json",
            root / "outputs" / "earthmoving_role_brief" / "role_brief.json",
            root / "outputs" / "jobsite_autonomy_eval" / "jobsite_autonomy_eval.json",
            root / "outputs" / "earthmoving_gap" / "gap_report.json",
            root / "outputs" / "earthmoving_plan_search" / "plan_search.json",
            root / "outputs" / "earthmoving_surrogate" / "surrogate_model.json",
            root / "outputs" / "terrain_kernel_benchmark" / "terrain_kernel_benchmark.json",
            root / "outputs" / "field_trial_case_study" / "field_trial_case_study.json",
            root / "outputs" / "field_trial_visuals" / "field_trial_visuals.json",
            root / "outputs" / "multipass_plan_eval" / "multipass_plan_eval.json",
            root / "outputs" / "task_plan_robustness" / "task_plan_robustness.json",
            root / "outputs" / "robustness_sensitivity" / "robustness_sensitivity.json",
        ],
        outputs=[json_path, md_path],
        metadata={
            "jobsite_decision": jobsite["summary"]["overall_decision"],
            "mean_productivity_m3_per_hr": jobsite["summary"]["mean_productivity_m3_per_hr"],
            "gate_status": review["summary"]["gate_status"],
        },
    )
    return payload


def render_hiring_manager_packet(payload: dict[str, Any]) -> str:
    lines = [
        "# Hiring Manager Packet",
        "",
        payload["headline"],
        "",
        payload["one_sentence"],
        "",
        "## Manager Summary",
        "",
    ]
    for item in payload["manager_summary"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Architecture", ""])
    for item in payload["architecture"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Evidence To Inspect", "", "| area | artifact | why it matters |", "| --- | --- | --- |"])
    for item in payload["evidence"]:
        lines.append(f"| {item['area']} | [{item['artifact']}]({item['path']}) | {item['why']} |")

    lines.extend(["", "## Suggested Review Path", ""])
    for index, item in enumerate(payload["review_path"], start=1):
        lines.append(f"{index}. {item}")

    lines.extend(["", "## Technical Judgment Signals", ""])
    for item in payload["technical_judgment"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Limitations", ""])
    for item in payload["limitations"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Next 30 Days With Real Machine Data", ""])
    for item in payload["next_30_days"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Short Note To Send", "", "```text", payload["outreach_note"], "```"])
    return "\n".join(lines)


def _manager_summary(
    review: dict[str, Any],
    jobsite: dict[str, Any],
    gap: dict[str, Any],
    plan: dict[str, Any],
    surrogate: dict[str, Any],
    kernel: dict[str, Any],
    case_study: dict[str, Any],
    multipass: dict[str, Any],
    robustness: dict[str, Any],
    sensitivity: dict[str, Any],
) -> list[str]:
    best = plan["summary"]["best_candidate"]
    best_multipass = multipass["summary"]["best_candidate"]
    return [
        f"The earthmoving gate is `{review['summary']['gate_status']}` across `{review['summary']['scenario_count']}` scenarios, with deterministic generated artifacts for review.",
        f"The jobsite scorecard converts sim outputs into a deployment decision: `{jobsite['summary']['overall_decision']}` with mean productivity `{jobsite['summary']['mean_productivity_m3_per_hr']:.2f}` m3/hr.",
        f"The current bottleneck is `{jobsite['summary']['top_bottleneck']}`, which creates a concrete next engineering loop instead of a vague demo.",
        f"The sim-to-field gap report identifies `{gap['summary']['top_global_sensitivity']['soil_parameter']}` as the top global calibration signal for `{gap['summary']['top_global_sensitivity']['metric']}`.",
        f"The blade-plan search evaluates `{plan['summary']['candidate_count']}` candidates and selects `{best['candidate']}` under the current score.",
        f"The multi-pass evaluator compares `{multipass['summary']['candidate_count']}` task sequences; best is `{best_multipass['candidate']}` at `{best_multipass['productivity_m3_per_hr']:.2f}` m3/hr.",
        f"The robustness sweep runs `{robustness['summary']['episode_count']}` uncertainty episodes for `{robustness['candidate']}` with pass rate `{robustness['summary']['pass_rate']:.0%}`.",
        f"The robustness sensitivity report ranks `{sensitivity['summary']['top_driver']['input']}` as the strongest productivity driver.",
        f"The field-trial case study traces `{case_study['scenario']}` from replay metrics to root-cause hypotheses and the next experiment.",
        f"The surrogate model reports mean MAE `{surrogate['summary']['mean_mae']:.6f}`, showing how the generated dataset can support learned evaluators.",
        f"The C++ terrain kernel benchmark shows `{kernel['summary']['cxx_speedup']:.2f}x` speedup over Python for the terrain update workload.",
    ]


def _architecture() -> list[str]:
    return [
        "MuJoCo machine scene defines the blade/dozer kinematic path used for deterministic replay.",
        "A heightmap terrain layer applies blade passes with soil cohesion, friction, compaction, coupling, spillover, and volume accounting.",
        "Benchmark, scale, sensitivity, calibration, and gap-report stages turn raw runs into validation evidence.",
        "Jobsite evaluation translates physical metrics into cycle time, productivity, target capture, bottleneck, and rework risk.",
        "Dataset, surrogate, and plan-search stages connect the simulator to ML autonomy evaluation and planner tuning.",
        "Native-kernel smoke and benchmark paths show where hot terrain operations could move from Python to C++ or Rust.",
    ]


def _evidence(
    review: dict[str, Any],
    role_brief: dict[str, Any],
    jobsite: dict[str, Any],
    gap: dict[str, Any],
    plan: dict[str, Any],
    surrogate: dict[str, Any],
    kernel: dict[str, Any],
    case_study: dict[str, Any],
    visuals: dict[str, Any],
    multipass: dict[str, Any],
    robustness: dict[str, Any],
    sensitivity: dict[str, Any],
) -> list[dict[str, str]]:
    _ = (review, role_brief, jobsite, gap, plan, surrogate, kernel, case_study, visuals, multipass, robustness, sensitivity)
    return [
        {
            "area": "Hiring overview",
            "artifact": "Earthmoving role brief",
            "path": "../earthmoving_role_brief/role_brief.md",
            "why": "Fastest proof that the project maps to autonomy simulation work.",
        },
        {
            "area": "Release evidence",
            "artifact": "Earthmoving review packet",
            "path": "../earthmoving_review_packet/review_packet.md",
            "why": "Rolls up scenario results, readiness signals, sensitivities, and sim-to-field gaps.",
        },
        {
            "area": "Deployment relevance",
            "artifact": "Jobsite autonomy evaluation",
            "path": "../jobsite_autonomy_eval/report.md",
            "why": "Shows cycle-time, productivity, placement, and bottleneck thinking.",
        },
        {
            "area": "Debug narrative",
            "artifact": "Field trial case study",
            "path": "../field_trial_case_study/field_trial_case_study.md",
            "why": "Connects one replay to observations, hypotheses, and a next experiment.",
        },
        {
            "area": "Visual review",
            "artifact": "Field trial visuals",
            "path": "../field_trial_visuals/field_trial_visuals.md",
            "why": "Shows terrain delta, blade path, and productivity bottleneck plots.",
        },
        {
            "area": "Calibration",
            "artifact": "Sim-to-field gap report",
            "path": "../earthmoving_gap/report.md",
            "why": "Demonstrates how field observations would drive the next simulation updates.",
        },
        {
            "area": "Autonomy loop",
            "artifact": "Blade plan search",
            "path": "../earthmoving_plan_search/report.md",
            "why": "Uses the simulator to evaluate candidate task parameters.",
        },
        {
            "area": "Task planning",
            "artifact": "Multi-pass plan evaluation",
            "path": "../multipass_plan_eval/multipass_plan_eval.md",
            "why": "Compares single-pass and multi-pass task sequences against productivity and placement gates.",
        },
        {
            "area": "Robustness",
            "artifact": "Task plan robustness sweep",
            "path": "../task_plan_robustness/task_plan_robustness.md",
            "why": "Stress-tests the selected task plan under soil and cycle-time uncertainty.",
        },
        {
            "area": "Sensitivity",
            "artifact": "Robustness sensitivity",
            "path": "../robustness_sensitivity/robustness_sensitivity.md",
            "why": "Ranks which uncertain inputs most explain productivity misses.",
        },
        {
            "area": "ML evaluation",
            "artifact": "Surrogate evaluator",
            "path": "../earthmoving_surrogate/report.md",
            "why": "Shows generated labels and learned evaluator scaffolding.",
        },
        {
            "area": "Performance",
            "artifact": "Terrain kernel benchmark",
            "path": "../terrain_kernel_benchmark/report.md",
            "why": "Shows native implementation and benchmark instinct for simulation hot paths.",
        },
    ]


def _review_path() -> list[str]:
    return [
        "Start with the role brief for a two-minute overview.",
        "Open the review packet to see the scenario table, readiness signals, and jobsite scorecard.",
        "Open the jobsite autonomy evaluation to see how sim outputs become deployment decisions.",
        "Open the field-trial case study to see one scenario traced from replay to next experiment.",
        "Open the field-trial visuals to quickly inspect terrain delta, blade path, and productivity bottleneck.",
        "Open the multi-pass plan evaluation to see whether changing task structure improves the bottleneck.",
        "Open the task-plan robustness sweep to see uncertainty sensitivity around the selected candidate.",
        "Open the robustness sensitivity report to see which telemetry or model inputs matter most next.",
        "Open the gap report to see calibration priorities and limitations.",
        "Skim the terrain kernel and benchmark if evaluating low-level implementation ability.",
    ]


def _technical_judgment(review: dict[str, Any], jobsite: dict[str, Any], gap: dict[str, Any]) -> list[str]:
    top_gap = gap["items"][0]
    return [
        "The project does not claim production soil mechanics; it frames the heightmap model as a validation scaffold with explicit limitations.",
        f"The scorecard chooses `{jobsite['summary']['overall_decision']}` rather than forcing a pass, because productivity is below the configured field-trial target.",
        f"The review packet separates sim quality gates from jobsite readiness, avoiding one metric pretending to answer every deployment question.",
        f"The largest gap is `{top_gap['dominant_gap_metric']}`, and the report turns that into a concrete measurement request instead of a vague tuning note.",
        f"The current top sensitivity is `{review['summary']['top_sensitivity']['soil_parameter']}` to `{review['summary']['top_sensitivity']['metric']}`, which makes calibration inspectable.",
    ]


def _limitations() -> list[str]:
    return [
        "The terrain deformation is a lightweight heightmap approximation, not DEM/FEM soil mechanics.",
        "The field logs are synthetic placeholders used to exercise the calibration workflow.",
        "The machine profile uses proxy cycle-time parameters and should be replaced with real excavator/dozer telemetry.",
        "The planner is a grid search over single-pass blade parameters; multi-pass task planning is the natural next step.",
        "The native terrain kernel is benchmarked as a standalone path; deeper integration would require Python bindings and profiling inside the full evaluation loop.",
    ]


def _next_30_days() -> list[str]:
    return [
        "Replace synthetic field logs with before/after terrain scans, machine pose, blade state, and cycle-time telemetry.",
        "Fit soil parameters per site condition and report confidence intervals across repeated passes.",
        "Extend plan search to multi-pass cut, carry, dump, and return sequences with productivity and target-placement objectives.",
        "Add scenario replay media that overlays blade trajectory, terrain delta, and target-zone capture for fast engineering review.",
        "Move the terrain update hot path behind a native binding and measure end-to-end throughput impact in batch evaluation.",
    ]


def _outreach_note() -> str:
    return (
        "Hi [Name], I built a focused autonomous earthmoving simulation packet that I think is relevant to Bedrock's Simulation role. "
        "It uses MuJoCo plus a heightmap terrain model to evaluate blade passes, soil calibration, randomized scale runs, sim-to-field gaps, "
        "jobsite productivity, and native terrain-kernel performance. The most manager-friendly entry point is "
        "`outputs/hiring_manager_packet/hiring_manager_packet.md`; the project is explicit about limitations and current bottlenecks rather than presenting it as a production soil solver. "
        "I would be grateful if you would be open to taking a look or pointing me toward the right engineering manager."
    )


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())
