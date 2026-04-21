from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.provenance import write_manifest


def build_simulation_packet(
    *,
    repo_root: str | Path,
    output_dir: str | Path,
    root_packet_path: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(repo_root)
    role_brief = _read_json(root / "outputs" / "earthmoving_role_brief" / "role_brief.json")
    review = _read_json(root / "outputs" / "earthmoving_review_packet" / "review_packet.json")
    surrogate = _read_json(root / "outputs" / "earthmoving_surrogate" / "surrogate_model.json")
    plan_search = _read_json(root / "outputs" / "earthmoving_plan_search" / "plan_search.json")
    failure_modes = _read_json(root / "outputs" / "earthmoving_failure_modes" / "failure_modes.json")
    kernel_benchmark = _read_json(root / "outputs" / "terrain_kernel_benchmark" / "terrain_kernel_benchmark.json")
    native_matrix = _read_json(root / "outputs" / "native_kernel_matrix" / "native_kernel_matrix.json")
    jobsite = _read_json(root / "outputs" / "jobsite_autonomy_eval" / "jobsite_autonomy_eval.json")
    multipass = _read_json(root / "outputs" / "multipass_plan_eval" / "multipass_plan_eval.json")
    robustness = _read_json(root / "outputs" / "task_plan_robustness" / "task_plan_robustness.json")

    payload = {
        "headline": role_brief["headline"],
        "recommended_repo_strategy": "Keep this repo as the full engineering record, and link this packet as the recruiter-facing entry point.",
        "why_this_maps_to_the_role": [
            "High-fidelity simulation content: MuJoCo dozer/blade scene plus terrain before/after artifacts.",
            "Physics and geometry reasoning: heightmap terrain deformation, soil parameters, volume accounting, and target-berm metrics.",
            "Sim-to-real workflow: calibration against observed field-log metrics and gap reports with next measurement priorities.",
            "Scale and evaluation: randomized batch studies, quality gates, deterministic replay, and throughput reporting.",
            "Deployment relevance: cycle-time, productivity, target-capture, bottleneck, and rework-risk scoring from simulation outputs.",
            "ML/autonomy support: feature/label dataset, surrogate evaluator, and simulator-in-the-loop blade plan search.",
            "Production instincts: C++ terrain kernel smoke path, tests, provenance manifests, generated reports, and review packets.",
        ],
        "metrics": {
            **role_brief["metrics"],
            "surrogate_mean_mae": surrogate["summary"]["mean_mae"],
            "best_plan_score": plan_search["summary"]["best_candidate"]["score"],
            "top_failure_mode": failure_modes["summary"]["top_mode"],
            "cxx_kernel_speedup": kernel_benchmark["summary"]["cxx_speedup"],
            "fastest_native_kernel": native_matrix["summary"]["fastest_kernel"],
            "rust_ffi_speedup": _kernel_speedup(native_matrix, "rust_ffi"),
            "jobsite_decision": jobsite["summary"]["overall_decision"],
            "mean_productivity_m3_per_hr": jobsite["summary"]["mean_productivity_m3_per_hr"],
            "top_jobsite_bottleneck": jobsite["summary"]["top_bottleneck"],
            "best_task_plan": multipass["summary"]["best_candidate"]["candidate"],
            "best_task_plan_productivity": multipass["summary"]["best_candidate"]["productivity_m3_per_hr"],
            "best_task_plan_decision": multipass["summary"]["best_candidate"]["decision"],
            "task_plan_robustness_pass_rate": robustness["summary"]["pass_rate"],
            "task_plan_robustness_p10_productivity": robustness["summary"]["p10_productivity_m3_per_hr"],
        },
        "entry_points": {
            "hiring_manager_packet": "outputs/hiring_manager_packet/hiring_manager_packet.md",
            "dashboard": "outputs/earthmoving_dashboard/index.html",
            "role_brief": "outputs/earthmoving_role_brief/role_brief.md",
            "review_packet": "outputs/earthmoving_review_packet/review_packet.md",
            "benchmark_report": "outputs/earthmoving_benchmark/report.md",
            "gap_report": "outputs/earthmoving_gap/report.md",
            "jobsite_eval": "outputs/jobsite_autonomy_eval/report.md",
            "field_trial_visuals": "outputs/field_trial_visuals/field_trial_visuals.md",
            "field_trial_case_study": "outputs/field_trial_case_study/field_trial_case_study.md",
            "multipass_plan_eval": "outputs/multipass_plan_eval/multipass_plan_eval.md",
            "task_plan_robustness": "outputs/task_plan_robustness/task_plan_robustness.md",
            "surrogate_report": "outputs/earthmoving_surrogate/report.md",
            "plan_search_report": "outputs/earthmoving_plan_search/report.md",
            "kernel_benchmark": "outputs/terrain_kernel_benchmark/report.md",
            "native_kernel_matrix": "outputs/native_kernel_matrix/report.md",
            "cxx_kernel": "cpp/terrain_kernel.cpp",
            "rust_kernel_note": "docs/rust-simulation-kernel-note.md",
        },
        "talk_track": _talk_track(role_brief, review, surrogate, plan_search, failure_modes, kernel_benchmark, native_matrix, jobsite),
        "limitations": [
            "The terrain model is an intentionally lightweight heightmap approximation, not a production soil mechanics solver.",
            "Field logs are synthetic placeholders for demonstrating calibration workflow and should be replaced with real machine/site data.",
            "The jobsite productivity model uses proxy cycle-time assumptions until real machine telemetry is available.",
            "The C++ path is currently a standalone kernel smoke path; a stronger next step is binding it into the Python benchmark and profiling it against the Python update.",
        ],
        "next_technical_steps": [
            "Bind the C++ terrain kernel into the Python simulator and benchmark speedup.",
            "Expand task-plan evaluation into robustness sweeps across soil, blade-width, cut-depth, and cycle-time uncertainty.",
            "Add real or richer synthetic field traces with terrain-profile observations before and after earthmoving passes.",
            "Expand the blade planner from grid search to constrained optimization over multi-pass trajectories.",
            "Add visual replay/video generation for the dashboard so reviewers can inspect motion and terrain evolution quickly.",
        ],
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    packet_json = output / "simulation_packet.json"
    packet_md = output / "simulation_packet.md"
    packet_json.write_text(json.dumps(payload, indent=2))
    markdown = render_simulation_packet(payload)
    packet_md.write_text(markdown)
    root_packet = Path(root_packet_path) if root_packet_path else root / "EARTHMOVING_SIMULATION_PACKET.md"
    root_packet.write_text(markdown)
    write_manifest(
        repo_root=root,
        output_dir=output,
        run_type="simulation_packet",
        config={"root_packet_path": str(root_packet)},
        inputs=[
            root / "outputs" / "earthmoving_role_brief" / "role_brief.json",
            root / "outputs" / "earthmoving_review_packet" / "review_packet.json",
            root / "outputs" / "earthmoving_surrogate" / "surrogate_model.json",
            root / "outputs" / "earthmoving_plan_search" / "plan_search.json",
            root / "outputs" / "earthmoving_failure_modes" / "failure_modes.json",
            root / "outputs" / "terrain_kernel_benchmark" / "terrain_kernel_benchmark.json",
            root / "outputs" / "native_kernel_matrix" / "native_kernel_matrix.json",
            root / "outputs" / "jobsite_autonomy_eval" / "jobsite_autonomy_eval.json",
        ],
        outputs=[packet_json, packet_md, root_packet],
        metadata=payload["metrics"],
    )
    return payload


def render_simulation_packet(payload: dict[str, Any]) -> str:
    metrics = payload["metrics"]
    lines = [
        "# Earthmoving Simulation Packet",
        "",
        payload["headline"],
        "",
        f"Repo strategy: {payload['recommended_repo_strategy']}",
        "",
        "## Why This Maps To The Role",
        "",
    ]
    for item in payload["why_this_maps_to_the_role"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Current Metrics",
            "",
            f"- Gate status: `{metrics['gate_status']}`",
            f"- Earthmoving scenarios: `{metrics['scenario_count']}`",
            f"- Randomized scale episodes: `{metrics['scale_episode_count']}`",
            f"- Throughput: `{metrics['episodes_per_second']:.2f}` episodes/s",
            f"- Dataset rows: `{metrics['dataset_rows']}`",
            f"- Surrogate mean MAE: `{metrics['surrogate_mean_mae']:.6f}`",
            f"- Best blade-plan score: `{metrics['best_plan_score']:.6f}`",
            f"- Jobsite decision: `{metrics['jobsite_decision']}`",
            f"- Mean scaled productivity: `{metrics['mean_productivity_m3_per_hr']:.2f}` m3/hr",
            f"- Top jobsite bottleneck: `{metrics['top_jobsite_bottleneck']}`",
            f"- Best evaluated task plan: `{metrics['best_task_plan']}`",
            f"- Best task-plan productivity: `{metrics['best_task_plan_productivity']:.2f}` m3/hr",
            f"- Best task-plan decision: `{metrics['best_task_plan_decision']}`",
            f"- Task-plan robustness pass rate: `{metrics['task_plan_robustness_pass_rate']:.0%}`",
            f"- Task-plan robustness P10 productivity: `{metrics['task_plan_robustness_p10_productivity']:.2f}` m3/hr",
            f"- Top failure mode: `{metrics['top_failure_mode']}`",
            f"- C++ terrain-kernel speedup: `{metrics['cxx_kernel_speedup']:.2f}x`",
            f"- Fastest native terrain kernel: `{metrics['fastest_native_kernel']}`",
            f"- Rust FFI terrain-kernel speedup: `{metrics['rust_ffi_speedup']:.2f}x`",
            "",
            "## Best Review Links",
            "",
        ]
    )
    for label, path in payload["entry_points"].items():
        lines.append(f"- `{label}`: [{path}]({path})")
    lines.extend(["", "## Interview Talk Track", ""])
    for item in payload["talk_track"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Limitations I Would State Clearly", ""])
    for item in payload["limitations"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Next Technical Steps", ""])
    for item in payload["next_technical_steps"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


def _talk_track(
    role_brief: dict[str, Any],
    review: dict[str, Any],
    surrogate: dict[str, Any],
    plan_search: dict[str, Any],
    failure_modes: dict[str, Any],
    kernel_benchmark: dict[str, Any],
    native_matrix: dict[str, Any],
    jobsite: dict[str, Any],
) -> list[str]:
    top_sensitivity = review["summary"]["top_sensitivity"]
    best_plan = plan_search["summary"]["best_candidate"]
    return [
        "I started with a MuJoCo support/debugging project, then added an earthmoving simulation track specifically for autonomous construction.",
        f"The strongest sensitivity signal is `{top_sensitivity['soil_parameter']}` driving `{top_sensitivity['metric']}`, which gives a concrete calibration target.",
        f"The batch evaluator currently runs `{role_brief['metrics']['scale_episode_count']}` randomized earthmoving episodes at `{role_brief['metrics']['episodes_per_second']:.2f}` episodes/s.",
        f"The surrogate evaluator predicts `{surrogate['label_names'][0]}` and related metrics from soil/blade features, with mean MAE `{surrogate['summary']['mean_mae']:.6f}`.",
        f"The planner selected `{best_plan['candidate']}` as the best blade candidate under the current score function.",
        f"The jobsite scorecard translates sim outputs into cycle-time, productivity, target-capture, and rework-risk signals; the current decision is `{jobsite['summary']['overall_decision']}`, mainly because `{jobsite['summary']['top_bottleneck']}` is below target.",
        f"The C++ terrain kernel matches the Python terrain output and runs `{kernel_benchmark['summary']['cxx_speedup']:.2f}x` faster in its benchmark.",
        f"The native kernel matrix currently reports `{native_matrix['summary']['fastest_kernel']}` as the fastest available terrain kernel.",
        f"The Rust FFI terrain kernel shows how this workload can move toward memory-safe native kernels called from Python simulation tooling.",
        f"The failure queue surfaces `{failure_modes['summary']['top_mode']}` as the top debug theme, with next actions attached.",
    ]


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _kernel_speedup(native_matrix: dict[str, Any], kernel: str) -> float:
    for entry in native_matrix["entries"]:
        if entry["kernel"] == kernel and entry["status"] == "available":
            return float(entry["speedup_vs_python"])
    return 0.0
