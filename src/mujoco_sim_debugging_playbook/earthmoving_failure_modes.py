from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mujoco_sim_debugging_playbook.provenance import write_manifest


def build_earthmoving_failure_modes(
    *,
    benchmark_summary_path: str | Path,
    scale_summary_path: str | Path,
    replay_dir: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    benchmark = _read_json(benchmark_summary_path)
    scale = _read_json(scale_summary_path)
    replay_items = [_read_json(path) for path in sorted(Path(replay_dir).glob("*_replay.json"))]
    items = []
    for row in benchmark["rows"]:
        items.extend(_scenario_failure_items(row))
    for replay in replay_items:
        for hypothesis in replay.get("debug_hypotheses", []):
            items.append(
                {
                    "source": "replay",
                    "scenario": replay["scenario"],
                    "mode": "debug_hypothesis",
                    "severity": "medium",
                    "score": 45.0,
                    "evidence": hypothesis,
                    "next_action": "Open the replay bundle and compare blade path, terrain stats, and soil parameters.",
                }
            )
    if scale["summary"]["episodes_per_second"] < 150.0:
        items.append(
            {
                "source": "scale",
                "scenario": "batch",
                "mode": "throughput_risk",
                "severity": "high",
                "score": 75.0,
                "evidence": f"Throughput is {scale['summary']['episodes_per_second']:.2f} episodes/s.",
                "next_action": "Profile terrain update hot spots and consider using the C++ kernel path.",
            }
        )
    ranked = sorted(items, key=lambda item: item["score"], reverse=True)
    payload = {
        "summary": {
            "item_count": len(ranked),
            "high_count": sum(1 for item in ranked if item["severity"] == "high"),
            "top_mode": ranked[0]["mode"] if ranked else None,
        },
        "items": ranked,
    }
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    summary_path = output / "failure_modes.json"
    report_path = output / "report.md"
    summary_path.write_text(json.dumps(payload, indent=2))
    _write_report(payload, report_path)
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="earthmoving_failure_modes",
        config={
            "benchmark_summary": str(benchmark_summary_path),
            "scale_summary": str(scale_summary_path),
            "replay_dir": str(replay_dir),
        },
        inputs=[benchmark_summary_path, scale_summary_path, *sorted(Path(replay_dir).glob("*_replay.json"))],
        outputs=[summary_path, report_path],
        metadata=payload["summary"],
    )
    return payload


def _scenario_failure_items(row: dict[str, Any]) -> list[dict[str, Any]]:
    items = []
    if row["moved_volume"] < 0.0008:
        items.append(_item(row, "under_excavation", "high", 80.0, "Moved volume is below the practical debugging threshold.", "Increase blade depth/coupling or calibrate soil resistance."))
    if row["terrain_profile_rmse"] > 0.04:
        items.append(_item(row, "target_profile_miss", "high", 72.0, "Final terrain profile is far from the target berm.", "Tune deposit spread, target geometry, and path planning."))
    if row["volume_conservation_error"] > 0.00025:
        items.append(_item(row, "volume_residual", "medium", 58.0, "Compaction-adjusted volume residual is elevated.", "Inspect compaction rate and transport/deposit accounting."))
    if row["runtime_s"] > 0.05:
        items.append(_item(row, "slow_episode", "medium", 50.0, "Scenario runtime is slower than expected for scale runs.", "Profile terrain update and reduce grid resolution for batch studies."))
    return items


def _item(row: dict[str, Any], mode: str, severity: str, score: float, evidence: str, next_action: str) -> dict[str, Any]:
    return {
        "source": "benchmark",
        "scenario": row["scenario"],
        "mode": mode,
        "severity": severity,
        "score": score,
        "evidence": evidence,
        "next_action": next_action,
    }


def _write_report(payload: dict[str, Any], output_path: Path) -> None:
    lines = [
        "# Earthmoving Failure Modes",
        "",
        f"Items: `{payload['summary']['item_count']}`",
        f"High severity: `{payload['summary']['high_count']}`",
        f"Top mode: `{payload['summary']['top_mode']}`",
        "",
        "| scenario | mode | severity | score | next_action |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for item in payload["items"]:
        lines.append(
            f"| {item['scenario']} | {item['mode']} | {item['severity']} | "
            f"{item['score']:.1f} | {item['next_action']} |"
        )
    output_path.write_text("\n".join(lines))


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())
