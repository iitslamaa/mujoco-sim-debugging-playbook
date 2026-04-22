from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.provenance import write_manifest


def build_interview_assets(*, repo_root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    simulation = _read_json(root / "outputs" / "simulation_packet" / "simulation_packet.json")
    application = _read_json(root / "outputs" / "application_packet" / "application_packet.json")
    sensitivity = _read_json(root / "outputs" / "robustness_sensitivity" / "robustness_sensitivity.json")
    metrics = simulation["metrics"]
    payload = {
        "headline": "Interview and resume assets",
        "resume_bullets": _resume_bullets(metrics),
        "phone_screen_story": _phone_screen_story(metrics, sensitivity),
        "questions_to_invite": _questions_to_invite(),
        "links_to_send": application["links"],
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "interview_assets.json"
    md_path = output / "interview_assets.md"
    json_path.write_text(json.dumps(payload, indent=2))
    md_path.write_text(render_interview_assets(payload))
    write_manifest(
        repo_root=root,
        output_dir=output,
        run_type="interview_assets",
        config={},
        inputs=[
            root / "outputs" / "simulation_packet" / "simulation_packet.json",
            root / "outputs" / "application_packet" / "application_packet.json",
            root / "outputs" / "robustness_sensitivity" / "robustness_sensitivity.json",
        ],
        outputs=[json_path, md_path],
        metadata={"resume_bullet_count": len(payload["resume_bullets"])},
    )
    return payload


def render_interview_assets(payload: dict[str, Any]) -> str:
    lines = [
        "# Interview Assets",
        "",
        "## Resume Bullets",
        "",
    ]
    for item in payload["resume_bullets"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Phone Screen Story", ""])
    for item in payload["phone_screen_story"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Questions To Invite", ""])
    for item in payload["questions_to_invite"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Links To Send", ""])
    for label, path in payload["links_to_send"].items():
        lines.append(f"- `{label}`: [{path}]({path})")
    return "\n".join(lines)


def _resume_bullets(metrics: dict[str, Any]) -> list[str]:
    return [
        (
            "Built a MuJoCo autonomous earthmoving simulation track with heightmap terrain deformation, "
            "soil calibration, deterministic replay bundles, and release-style review artifacts."
        ),
        (
            f"Implemented jobsite productivity scoring and task-plan evaluation; selected `{metrics['best_task_plan']}` "
            f"as a nominal `{metrics['best_task_plan_decision']}` at `{metrics['best_task_plan_productivity']:.2f}` m3/hr."
        ),
        (
            f"Ran robustness analysis over soil and cycle-time uncertainty, surfacing `{metrics['top_robustness_driver']}` "
            f"as the top productivity driver with `{metrics['task_plan_robustness_pass_rate']:.0%}` pass rate."
        ),
        (
            f"Benchmarked native terrain-update kernels, including a C++ path with `{metrics['cxx_kernel_speedup']:.2f}x` "
            "speedup over the Python baseline."
        ),
    ]


def _phone_screen_story(metrics: dict[str, Any], sensitivity: dict[str, Any]) -> list[str]:
    top = sensitivity["summary"]["top_driver"]
    return [
        "I built the project to show simulation validation judgment, not just a visual demo.",
        "The core loop is: run terrain scenarios, score jobsite productivity, compare task plans, stress the chosen plan, then report calibration priorities.",
        f"The nominal best plan reaches `{metrics['best_task_plan_productivity']:.2f}` m3/hr, but robustness drops to `{metrics['task_plan_robustness_pass_rate']:.0%}` pass rate.",
        f"The sensitivity report points to `{top['input']}` as the strongest productivity driver, so I would prioritize that telemetry or calibration path next.",
        "I call out that the terrain model is a lightweight heightmap approximation, because production simulation work requires being honest about model validity.",
    ]


def _questions_to_invite() -> list[str]:
    return [
        "How would you replace the synthetic field logs with real machine/site observations?",
        "How would you decide whether this belongs in sim content, planner evaluation, or field operations tooling?",
        "What would you move from Python into native code first, and how would you prove it matters end to end?",
        "How would you set pass/fail gates before letting a candidate behavior reach a supervised field trial?",
    ]


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())
