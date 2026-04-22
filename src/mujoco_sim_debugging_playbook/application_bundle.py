from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.provenance import file_digest, write_manifest


def build_application_bundle(*, repo_root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    items = [
        _item("first_send", "Application packet", "outputs/application_packet/application_packet.md", "Recruiter or hiring manager"),
        _item("technical_review", "Hiring manager packet", "outputs/hiring_manager_packet/hiring_manager_packet.md", "Engineering manager"),
        _item("case_study", "Field trial case study", "outputs/field_trial_case_study/field_trial_case_study.md", "Simulation engineer"),
        _item("visual_review", "Field trial visuals", "outputs/field_trial_visuals/field_trial_visuals.md", "Fast visual skim"),
        _item("robustness", "Task plan robustness", "outputs/task_plan_robustness/task_plan_robustness.md", "Autonomy validation"),
        _item("sensitivity", "Robustness sensitivity", "outputs/robustness_sensitivity/robustness_sensitivity.md", "Calibration discussion"),
        _item("interview", "Interview assets", "outputs/interview_assets/interview_assets.md", "Personal preparation"),
        _item("kernel", "C++ terrain kernel", "cpp/terrain_kernel.cpp", "Low-level implementation review"),
    ]
    for item in items:
        path = root / item["path"]
        item["exists"] = path.exists()
        item["sha256"] = file_digest(path)
        item["size_bytes"] = path.stat().st_size if path.exists() else None

    payload = {
        "name": "application_bundle",
        "summary": {
            "item_count": len(items),
            "missing_count": sum(not item["exists"] for item in items),
            "first_send": "outputs/application_packet/application_packet.md",
        },
        "items": items,
        "send_order": [item["path"] for item in items[:3]],
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "application_bundle.json"
    md_path = output / "application_bundle.md"
    json_path.write_text(json.dumps(payload, indent=2))
    md_path.write_text(render_application_bundle(payload))
    write_manifest(
        repo_root=root,
        output_dir=output,
        run_type="application_bundle",
        config={},
        inputs=[root / item["path"] for item in items],
        outputs=[json_path, md_path],
        metadata=payload["summary"],
    )
    return payload


def render_application_bundle(payload: dict[str, Any]) -> str:
    lines = [
        "# Application Bundle",
        "",
        f"Items: `{payload['summary']['item_count']}`",
        f"Missing: `{payload['summary']['missing_count']}`",
        f"First send: [{payload['summary']['first_send']}]({payload['summary']['first_send']})",
        "",
        "## Send Order",
        "",
    ]
    for path in payload["send_order"]:
        lines.append(f"- [{path}]({path})")
    lines.extend(
        [
            "",
            "## Bundle Items",
            "",
            "| role | label | audience | path | exists |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["items"]:
        exists = "yes" if item["exists"] else "no"
        lines.append(
            f"| {item['role']} | {item['label']} | {item['audience']} | "
            f"[{item['path']}]({item['path']}) | {exists} |"
        )
    return "\n".join(lines)


def _item(role: str, label: str, path: str, audience: str) -> dict[str, Any]:
    return {
        "role": role,
        "label": label,
        "path": path,
        "audience": audience,
    }
