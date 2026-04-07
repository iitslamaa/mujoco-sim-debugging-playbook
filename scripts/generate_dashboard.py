from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def _read_json(path: Path):
    return json.loads(path.read_text()) if path.exists() else None


def main() -> None:
    dashboard_dir = ROOT / "dashboard"
    dashboard_dir.mkdir(parents=True, exist_ok=True)

    baseline = _read_json(ROOT / "outputs" / "baseline" / "summary.json")
    diagnostics = _read_json(ROOT / "outputs" / "diagnostics" / "environment.json")
    learning_training = _read_json(ROOT / "outputs" / "learning" / "training" / "training_summary.json")
    learning_eval = _read_json(ROOT / "outputs" / "learning" / "evaluation" / "summary.json")
    rl_training = _read_json(ROOT / "outputs" / "rl" / "training" / "training_summary.json")
    rl_evaluation = _read_json(ROOT / "outputs" / "rl" / "evaluation" / "summary.json")
    benchmark_summary = _read_json(ROOT / "outputs" / "controller_benchmark" / "benchmark_summary.json")
    randomization_summary = _read_json(ROOT / "outputs" / "domain_randomization" / "evaluation_rows.json")
    regression_diff = _read_json(ROOT / "outputs" / "regression" / "latest_diff" / "regression_diff.json")
    regression_gate = _read_json(ROOT / "outputs" / "regression" / "gate" / "regression_gate.json")
    regression_history = _read_json(ROOT / "outputs" / "regression" / "history" / "history.json")
    provenance_index = _read_json(ROOT / "outputs" / "provenance" / "index.json")
    release_notes = _read_json(ROOT / "outputs" / "releases" / "latest" / "release_notes.json")
    anomalies = _read_json(ROOT / "outputs" / "anomalies" / "anomaly_report.json")
    recommendations = _read_json(ROOT / "outputs" / "recommendations" / "recommendations.json")
    triage = _read_json(ROOT / "outputs" / "triage" / "triage_queue.json")
    incidents = _read_json(ROOT / "outputs" / "incidents" / "index.json")
    knowledge_base = _read_json(ROOT / "outputs" / "knowledge_base" / "index.json")
    escalation = _read_json(ROOT / "outputs" / "escalation" / "escalation_matrix.json")
    support_ops = _read_json(ROOT / "outputs" / "support_ops" / "support_ops.json")
    support_gaps = _read_json(ROOT / "outputs" / "support_gaps" / "support_gaps.json")
    workstreams = _read_json(ROOT / "outputs" / "workstreams" / "workstream_plan.json")
    sla = _read_json(ROOT / "outputs" / "sla" / "sla_report.json")
    capacity = _read_json(ROOT / "outputs" / "capacity" / "capacity_plan.json")
    ops_review = _read_json(ROOT / "outputs" / "ops_review" / "ops_review.json")
    support_readiness = _read_json(ROOT / "outputs" / "support_readiness" / "support_readiness.json")
    scenario_plan = _read_json(ROOT / "outputs" / "scenario_plan" / "scenario_plan.json")
    artifact_freshness = _read_json(ROOT / "outputs" / "artifact_freshness" / "artifact_freshness.json")
    regeneration_plan = _read_json(ROOT / "outputs" / "regeneration_plan" / "regeneration_plan.json")
    dependency_map = _read_json(ROOT / "outputs" / "dependency_map" / "dependency_map.json")
    impact_analysis = _read_json(ROOT / "outputs" / "impact_analysis" / "impact_analysis.json")
    refresh_bundle = _read_json(ROOT / "outputs" / "refresh_bundle" / "refresh_bundle.json")
    refresh_checklist = _read_json(ROOT / "outputs" / "refresh_checklist" / "refresh_checklist.json")
    maintenance_risk = _read_json(ROOT / "outputs" / "maintenance_risk" / "maintenance_risk.json")
    artifact_readiness = _read_json(ROOT / "outputs" / "artifact_readiness" / "artifact_readiness.json")
    artifact_scenarios = _read_json(ROOT / "outputs" / "artifact_scenarios" / "artifact_scenarios.json")
    artifact_recovery = _read_json(ROOT / "outputs" / "artifact_recovery" / "artifact_recovery.json")
    artifact_delivery = _read_json(ROOT / "outputs" / "artifact_delivery" / "artifact_delivery.json")
    artifact_capacity = _read_json(ROOT / "outputs" / "artifact_capacity" / "artifact_capacity.json")
    artifact_exec_summary = _read_json(ROOT / "outputs" / "artifact_exec_summary" / "artifact_exec_summary.json")
    artifact_history = _read_json(ROOT / "outputs" / "artifact_history" / "artifact_history.json")
    artifact_actions = _read_json(ROOT / "outputs" / "artifact_actions" / "artifact_actions.json")
    artifact_alerts = _read_json(ROOT / "outputs" / "artifact_alerts" / "artifact_alerts.json")
    artifact_digest = _read_json(ROOT / "outputs" / "artifact_digest" / "artifact_digest.json")
    artifact_handoff = _read_json(ROOT / "outputs" / "artifact_handoff" / "artifact_handoff.json")
    artifact_review_note = _read_json(ROOT / "outputs" / "artifact_review_note" / "artifact_review_note.json")
    artifact_closeout = _read_json(ROOT / "outputs" / "artifact_closeout" / "artifact_closeout.json")
    artifact_scorecard = _read_json(ROOT / "outputs" / "artifact_scorecard" / "artifact_scorecard.json")
    artifact_packet = _read_json(ROOT / "outputs" / "artifact_packet" / "artifact_packet.json")
    dashboard_snapshot = _read_json(ROOT / "outputs" / "dashboard_snapshots" / "latest.json")
    dashboard_snapshot_history = _read_json(ROOT / "outputs" / "dashboard_snapshots" / "history.json")
    dashboard_snapshot_drift = _read_json(ROOT / "outputs" / "dashboard_snapshots" / "drift.json")
    dashboard_snapshot_alerts = _read_json(ROOT / "outputs" / "dashboard_snapshots" / "alerts.json")
    dashboard_snapshot_monitor = _read_json(ROOT / "outputs" / "dashboard_snapshots" / "monitor.json")
    dashboard_snapshot_review = _read_json(ROOT / "outputs" / "dashboard_snapshots" / "review.json")
    dashboard_snapshot_handoff = _read_json(ROOT / "outputs" / "dashboard_snapshots" / "handoff.json")
    dashboard_snapshot_closeout = _read_json(ROOT / "outputs" / "dashboard_snapshots" / "closeout.json")
    dashboard_snapshot_scorecard = _read_json(ROOT / "outputs" / "dashboard_snapshots" / "scorecard.json")
    dashboard_snapshot_digest = _read_json(ROOT / "outputs" / "dashboard_snapshots" / "digest.json")
    case_study_exists = (ROOT / "outputs" / "case_studies" / "controller_robustness_story.md").exists()
    support_cases = []
    for case_path in sorted((ROOT / "outputs" / "support_cases").glob("*.md")):
        support_cases.append(
            {
                "name": case_path.stem,
                "path": str(case_path.relative_to(ROOT)),
            }
        )

    provenance_summary = None
    if provenance_index:
        provenance_summary = {
            "summary": provenance_index["summary"],
            "recent_manifests": [
                {
                    "run_type": entry["run_type"],
                    "created_at": entry["created_at"],
                    "manifest_path": entry["manifest_path"],
                    "git_head": entry["environment"]["tooling"].get("git_head"),
                    "git_is_dirty": entry["environment"]["tooling"].get("git_is_dirty"),
                }
                for entry in provenance_index.get("manifests", [])[:5]
            ],
        }

    payload = {
        "repo": "mujoco-sim-debugging-playbook",
        "baseline_summary": baseline["summary"] if baseline else None,
        "environment": {
            "platform": diagnostics["platform"] if diagnostics else None,
            "runtime": diagnostics["runtime"] if diagnostics else None,
            "tooling": diagnostics["tooling"] if diagnostics else None,
        } if diagnostics else None,
        "learning_training": {
            "epochs": learning_training["epochs"],
            "best_val_loss": learning_training["best_val_loss"],
            "batch_size": learning_training["batch_size"],
            "learning_rate": learning_training["learning_rate"],
            "final_train_loss": learning_training["history"][-1]["train_loss"],
            "final_val_loss": learning_training["history"][-1]["val_loss"],
        } if learning_training else None,
        "learning_evaluation": learning_eval,
        "rl_training": {
            "iterations": rl_training["iterations"],
            "episodes_per_iteration": rl_training["episodes_per_iteration"],
            "final_return": rl_training["history"][-1]["mean_episode_return"],
            "final_success_rate": rl_training["history"][-1]["success_rate"],
            "policy_std": rl_training["history"][-1]["policy_std"],
        } if rl_training else None,
        "rl_evaluation": rl_evaluation,
        "benchmark_summary": benchmark_summary,
        "randomization_summary": randomization_summary,
        "regression_diff": regression_diff,
        "regression_gate": regression_gate,
        "regression_history": regression_history,
        "provenance_index": provenance_summary,
        "release_notes": release_notes,
        "anomalies": anomalies,
        "recommendations": recommendations,
        "triage": triage,
        "incidents": incidents,
        "knowledge_base": knowledge_base,
        "escalation": escalation,
        "support_ops": support_ops,
        "support_gaps": support_gaps,
        "workstreams": workstreams,
        "sla": sla,
        "capacity": capacity,
        "ops_review": ops_review,
        "support_readiness": support_readiness,
        "scenario_plan": scenario_plan,
        "artifact_freshness": artifact_freshness,
        "regeneration_plan": regeneration_plan,
        "dependency_map": dependency_map,
        "impact_analysis": impact_analysis,
        "refresh_bundle": refresh_bundle,
        "refresh_checklist": refresh_checklist,
        "maintenance_risk": maintenance_risk,
        "artifact_readiness": artifact_readiness,
        "artifact_scenarios": artifact_scenarios,
        "artifact_recovery": artifact_recovery,
        "artifact_delivery": artifact_delivery,
        "artifact_capacity": artifact_capacity,
        "artifact_exec_summary": artifact_exec_summary,
        "artifact_history": artifact_history,
        "artifact_actions": artifact_actions,
        "artifact_alerts": artifact_alerts,
        "artifact_digest": artifact_digest,
        "artifact_handoff": artifact_handoff,
        "artifact_review_note": artifact_review_note,
        "artifact_closeout": artifact_closeout,
        "artifact_scorecard": artifact_scorecard,
        "artifact_packet": artifact_packet,
        "dashboard_snapshot": dashboard_snapshot,
        "dashboard_snapshot_history": dashboard_snapshot_history,
        "dashboard_snapshot_drift": dashboard_snapshot_drift,
        "dashboard_snapshot_alerts": dashboard_snapshot_alerts,
        "dashboard_snapshot_monitor": dashboard_snapshot_monitor,
        "dashboard_snapshot_review": dashboard_snapshot_review,
        "dashboard_snapshot_handoff": dashboard_snapshot_handoff,
        "dashboard_snapshot_closeout": dashboard_snapshot_closeout,
        "dashboard_snapshot_scorecard": dashboard_snapshot_scorecard,
        "dashboard_snapshot_digest": dashboard_snapshot_digest,
        "case_studies": {
            "controller_robustness_story": "outputs/case_studies/controller_robustness_story.md"
        } if case_study_exists else None,
        "support_cases": support_cases,
        "artifacts": {
            "demo_gif": "outputs/media/reacher_demo.gif",
            "training_curve": "outputs/learning/training/training_curve.png",
            "rl_training_curve": "outputs/rl/training/training_curve.png",
            "diagnostics_markdown": "outputs/diagnostics/diagnostics.md",
            "support_case_markdown": "outputs/support_cases/actuator_gain_overshoot.md",
            "benchmark_report": "outputs/controller_benchmark/report.md",
            "randomization_report": "outputs/domain_randomization/report.md",
            "case_study_image": "outputs/case_studies/controller_robustness_story.png",
            "regression_diff_markdown": "outputs/regression/latest_diff/regression_diff.md",
            "regression_diff_image": "outputs/regression/latest_diff/regression_diff.png",
            "regression_gate_markdown": "outputs/regression/gate/regression_gate.md",
            "regression_history_markdown": "outputs/regression/history/history.md",
            "regression_history_image": "outputs/regression/history/history.png",
            "provenance_index_markdown": "outputs/provenance/index.md",
            "release_notes_markdown": "outputs/releases/latest/release_notes.md",
            "anomaly_report_markdown": "outputs/anomalies/anomaly_report.md",
            "anomaly_benchmark_image": "outputs/anomalies/benchmark_risk_heatmap.png",
            "anomaly_difficulty_image": "outputs/anomalies/randomization_difficulty.png",
            "recommendations_markdown": "outputs/recommendations/recommendations.md",
            "triage_markdown": "outputs/triage/triage_queue.md",
            "incident_index_markdown": "outputs/incidents/index.md",
            "knowledge_base_markdown": "outputs/knowledge_base/index.md",
            "escalation_markdown": "outputs/escalation/escalation_matrix.md",
            "support_ops_markdown": "outputs/support_ops/support_ops.md",
            "support_gaps_markdown": "outputs/support_gaps/support_gaps.md",
            "workstream_plan_markdown": "outputs/workstreams/workstream_plan.md",
            "sla_markdown": "outputs/sla/sla_report.md",
            "capacity_markdown": "outputs/capacity/capacity_plan.md",
            "ops_review_markdown": "outputs/ops_review/ops_review.md",
            "support_readiness_markdown": "outputs/support_readiness/support_readiness.md",
            "scenario_plan_markdown": "outputs/scenario_plan/scenario_plan.md",
            "artifact_freshness_markdown": "outputs/artifact_freshness/artifact_freshness.md",
            "regeneration_plan_markdown": "outputs/regeneration_plan/regeneration_plan.md",
            "dependency_map_markdown": "outputs/dependency_map/dependency_map.md",
            "impact_analysis_markdown": "outputs/impact_analysis/impact_analysis.md",
            "refresh_bundle_markdown": "outputs/refresh_bundle/refresh_bundle.md",
            "refresh_checklist_markdown": "outputs/refresh_checklist/refresh_checklist.md",
            "maintenance_risk_markdown": "outputs/maintenance_risk/maintenance_risk.md",
            "artifact_readiness_markdown": "outputs/artifact_readiness/artifact_readiness.md",
            "artifact_scenarios_markdown": "outputs/artifact_scenarios/artifact_scenarios.md",
            "artifact_recovery_markdown": "outputs/artifact_recovery/artifact_recovery.md",
            "artifact_delivery_markdown": "outputs/artifact_delivery/artifact_delivery.md",
            "artifact_capacity_markdown": "outputs/artifact_capacity/artifact_capacity.md",
            "artifact_exec_summary_markdown": "outputs/artifact_exec_summary/artifact_exec_summary.md",
            "artifact_history_markdown": "outputs/artifact_history/artifact_history.md",
            "artifact_actions_markdown": "outputs/artifact_actions/artifact_actions.md",
            "artifact_alerts_markdown": "outputs/artifact_alerts/artifact_alerts.md",
            "artifact_digest_markdown": "outputs/artifact_digest/artifact_digest.md",
            "artifact_handoff_markdown": "outputs/artifact_handoff/artifact_handoff.md",
            "artifact_review_note_markdown": "outputs/artifact_review_note/artifact_review_note.md",
            "artifact_closeout_markdown": "outputs/artifact_closeout/artifact_closeout.md",
            "artifact_scorecard_markdown": "outputs/artifact_scorecard/artifact_scorecard.md",
            "artifact_packet_markdown": "outputs/artifact_packet/artifact_packet.md",
            "dashboard_snapshot_markdown": "outputs/dashboard_snapshots/latest.md",
            "dashboard_snapshot_history_markdown": "outputs/dashboard_snapshots/history.md",
            "dashboard_snapshot_drift_markdown": "outputs/dashboard_snapshots/drift.md",
            "dashboard_snapshot_alerts_markdown": "outputs/dashboard_snapshots/alerts.md",
            "dashboard_snapshot_monitor_markdown": "outputs/dashboard_snapshots/monitor.md",
            "dashboard_snapshot_review_markdown": "outputs/dashboard_snapshots/review.md",
            "dashboard_snapshot_handoff_markdown": "outputs/dashboard_snapshots/handoff.md",
            "dashboard_snapshot_closeout_markdown": "outputs/dashboard_snapshots/closeout.md",
            "dashboard_snapshot_scorecard_markdown": "outputs/dashboard_snapshots/scorecard.md",
            "dashboard_snapshot_digest_markdown": "outputs/dashboard_snapshots/digest.md",
        },
    }
    (dashboard_dir / "data.json").write_text(json.dumps(payload, indent=2))
    print(f"Dashboard data written to {dashboard_dir / 'data.json'}")


if __name__ == "__main__":
    main()
