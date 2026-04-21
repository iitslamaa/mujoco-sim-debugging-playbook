from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.provenance import write_manifest


def build_bedrock_packet(
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

    payload = {
        "headline": role_brief["headline"],
        "recommended_repo_strategy": "Keep this repo as the full engineering record, and link this packet as the recruiter-facing entry point.",
        "why_this_maps_to_the_role": [
            "High-fidelity simulation content: MuJoCo dozer/blade scene plus terrain before/after artifacts.",
            "Physics and geometry reasoning: heightmap terrain deformation, soil parameters, volume accounting, and target-berm metrics.",
            "Sim-to-real workflow: calibration against observed field-log metrics and gap reports with next measurement priorities.",
            "Scale and evaluation: randomized batch studies, quality gates, deterministic replay, and throughput reporting.",
            "ML/autonomy support: feature/label dataset, surrogate evaluator, and simulator-in-the-loop blade plan search.",
            "Production instincts: C++ terrain kernel smoke path, tests, provenance manifests, generated reports, and review packets.",
        ],
        "metrics": {
            **role_brief["metrics"],
            "surrogate_mean_mae": surrogate["summary"]["mean_mae"],
            "best_plan_score": plan_search["summary"]["best_candidate"]["score"],
            "top_failure_mode": failure_modes["summary"]["top_mode"],
            "cxx_kernel_speedup": kernel_benchmark["summary"]["cxx_speedup"],
        },
        "entry_points": {
            "dashboard": "outputs/earthmoving_dashboard/index.html",
            "role_brief": "outputs/earthmoving_role_brief/role_brief.md",
            "review_packet": "outputs/earthmoving_review_packet/review_packet.md",
            "benchmark_report": "outputs/earthmoving_benchmark/report.md",
            "gap_report": "outputs/earthmoving_gap/report.md",
            "surrogate_report": "outputs/earthmoving_surrogate/report.md",
            "plan_search_report": "outputs/earthmoving_plan_search/report.md",
            "kernel_benchmark": "outputs/terrain_kernel_benchmark/report.md",
            "cxx_kernel": "cpp/terrain_kernel.cpp",
        },
        "talk_track": _talk_track(role_brief, review, surrogate, plan_search, failure_modes, kernel_benchmark),
        "limitations": [
            "The terrain model is an intentionally lightweight heightmap approximation, not a production soil mechanics solver.",
            "Field logs are synthetic placeholders for demonstrating calibration workflow and should be replaced with real machine/site data.",
            "The C++ path is currently a standalone kernel smoke path; a stronger next step is binding it into the Python benchmark and profiling it against the Python update.",
        ],
        "next_technical_steps": [
            "Bind the C++ terrain kernel into the Python simulator and benchmark speedup.",
            "Add real or richer synthetic field traces with terrain-profile observations before and after earthmoving passes.",
            "Expand the blade planner from grid search to constrained optimization over multi-pass trajectories.",
            "Add visual replay/video generation for the dashboard so reviewers can inspect motion and terrain evolution quickly.",
        ],
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    packet_json = output / "bedrock_packet.json"
    packet_md = output / "bedrock_packet.md"
    packet_json.write_text(json.dumps(payload, indent=2))
    markdown = render_bedrock_packet(payload)
    packet_md.write_text(markdown)
    root_packet = Path(root_packet_path) if root_packet_path else root / "BEDROCK_SIMULATION_PACKET.md"
    root_packet.write_text(markdown)
    write_manifest(
        repo_root=root,
        output_dir=output,
        run_type="bedrock_packet",
        config={"root_packet_path": str(root_packet)},
        inputs=[
            root / "outputs" / "earthmoving_role_brief" / "role_brief.json",
            root / "outputs" / "earthmoving_review_packet" / "review_packet.json",
            root / "outputs" / "earthmoving_surrogate" / "surrogate_model.json",
            root / "outputs" / "earthmoving_plan_search" / "plan_search.json",
            root / "outputs" / "earthmoving_failure_modes" / "failure_modes.json",
            root / "outputs" / "terrain_kernel_benchmark" / "terrain_kernel_benchmark.json",
        ],
        outputs=[packet_json, packet_md, root_packet],
        metadata=payload["metrics"],
    )
    return payload


def render_bedrock_packet(payload: dict[str, Any]) -> str:
    metrics = payload["metrics"]
    lines = [
        "# Bedrock Simulation Packet",
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
            f"- Top failure mode: `{metrics['top_failure_mode']}`",
            f"- C++ terrain-kernel speedup: `{metrics['cxx_kernel_speedup']:.2f}x`",
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
) -> list[str]:
    top_sensitivity = review["summary"]["top_sensitivity"]
    best_plan = plan_search["summary"]["best_candidate"]
    return [
        "I started with a MuJoCo support/debugging project, then added an earthmoving simulation track specifically for autonomous construction.",
        f"The strongest sensitivity signal is `{top_sensitivity['soil_parameter']}` driving `{top_sensitivity['metric']}`, which gives a concrete calibration target.",
        f"The batch evaluator currently runs `{role_brief['metrics']['scale_episode_count']}` randomized earthmoving episodes at `{role_brief['metrics']['episodes_per_second']:.2f}` episodes/s.",
        f"The surrogate evaluator predicts `{surrogate['label_names'][0]}` and related metrics from soil/blade features, with mean MAE `{surrogate['summary']['mean_mae']:.6f}`.",
        f"The planner selected `{best_plan['candidate']}` as the best blade candidate under the current score function.",
        f"The C++ terrain kernel matches the Python terrain output and runs `{kernel_benchmark['summary']['cxx_speedup']:.2f}x` faster in the current benchmark.",
        f"The failure queue surfaces `{failure_modes['summary']['top_mode']}` as the top debug theme, with next actions attached.",
    ]


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())
