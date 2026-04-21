from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.provenance import write_manifest


def build_application_packet(*, repo_root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    simulation = _read_json(root / "outputs" / "simulation_packet" / "simulation_packet.json")
    manager = _read_json(root / "outputs" / "hiring_manager_packet" / "hiring_manager_packet.json")
    robustness = _read_json(root / "outputs" / "task_plan_robustness" / "task_plan_robustness.json")
    sensitivity = _read_json(root / "outputs" / "robustness_sensitivity" / "robustness_sensitivity.json")
    metrics = simulation["metrics"]
    payload = {
        "headline": "Autonomous earthmoving simulation portfolio packet",
        "positioning": (
            "A focused MuJoCo construction-autonomy simulation project showing terrain deformation, "
            "jobsite productivity scoring, task-plan evaluation, robustness analysis, and native-kernel performance."
        ),
        "best_entry_point": "outputs/hiring_manager_packet/hiring_manager_packet.md",
        "proof_points": [
            f"Nominal best task plan `{metrics['best_task_plan']}` reaches `{metrics['best_task_plan_productivity']:.2f}` m3/hr and is marked `{metrics['best_task_plan_decision']}`.",
            f"Robustness sweep pass rate is `{metrics['task_plan_robustness_pass_rate']:.0%}` with P10 productivity `{metrics['task_plan_robustness_p10_productivity']:.2f}` m3/hr.",
            f"Top robustness driver is `{metrics['top_robustness_driver']}`, giving a concrete calibration/telemetry priority.",
            f"Batch scale evaluation runs `{metrics['scale_episode_count']}` randomized episodes at `{metrics['episodes_per_second']:.2f}` episodes/s.",
            f"C++ terrain-kernel benchmark reports `{metrics['cxx_kernel_speedup']:.2f}x` speedup over Python.",
        ],
        "links": {
            "hiring_manager_packet": "outputs/hiring_manager_packet/hiring_manager_packet.md",
            "simulation_packet": "EARTHMOVING_SIMULATION_PACKET.md",
            "field_trial_case_study": "outputs/field_trial_case_study/field_trial_case_study.md",
            "task_plan_robustness": "outputs/task_plan_robustness/task_plan_robustness.md",
            "robustness_sensitivity": "outputs/robustness_sensitivity/robustness_sensitivity.md",
            "terrain_kernel": "cpp/terrain_kernel.cpp",
        },
        "honest_limitations": [
            "The terrain model is a lightweight heightmap approximation, not a production soil solver.",
            "Field logs are synthetic and used to demonstrate calibration workflow until real machine data is available.",
            "The selected task plan clears nominal gates but needs more robustness work before field-trial confidence.",
        ],
        "message": _message(),
        "source_summaries": {
            "manager_summary_count": len(manager["manager_summary"]),
            "robustness_pass_rate": robustness["summary"]["pass_rate"],
            "top_sensitivity_driver": sensitivity["summary"]["top_driver"]["input"],
        },
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "application_packet.json"
    md_path = output / "application_packet.md"
    json_path.write_text(json.dumps(payload, indent=2))
    md_path.write_text(render_application_packet(payload))
    write_manifest(
        repo_root=root,
        output_dir=output,
        run_type="application_packet",
        config={},
        inputs=[
            root / "outputs" / "simulation_packet" / "simulation_packet.json",
            root / "outputs" / "hiring_manager_packet" / "hiring_manager_packet.json",
            root / "outputs" / "task_plan_robustness" / "task_plan_robustness.json",
            root / "outputs" / "robustness_sensitivity" / "robustness_sensitivity.json",
        ],
        outputs=[json_path, md_path],
        metadata=payload["source_summaries"],
    )
    return payload


def render_application_packet(payload: dict[str, Any]) -> str:
    lines = [
        "# Application Packet",
        "",
        payload["headline"],
        "",
        payload["positioning"],
        "",
        f"Best entry point: [{payload['best_entry_point']}]({payload['best_entry_point']})",
        "",
        "## Proof Points",
        "",
    ]
    for item in payload["proof_points"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Links", ""])
    for label, path in payload["links"].items():
        lines.append(f"- `{label}`: [{path}]({path})")
    lines.extend(["", "## Honest Limitations", ""])
    for item in payload["honest_limitations"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Message", "", "```text", payload["message"], "```"])
    return "\n".join(lines)


def _message() -> str:
    return (
        "Hi [Name], I applied for Bedrock's Simulation Engineer role and wanted to send a focused technical artifact. "
        "I built a MuJoCo-based autonomous earthmoving simulation track with deformable terrain, jobsite productivity scoring, "
        "task-plan evaluation, robustness sweeps, sensitivity analysis, and a native terrain-kernel benchmark. "
        "The best entry point is `outputs/hiring_manager_packet/hiring_manager_packet.md`; it includes the limitations and the next calibration steps clearly. "
        "I would be grateful if you would be open to taking a look or pointing me toward the right person on the simulation team."
    )


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())
