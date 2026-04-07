from pathlib import Path
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], env: dict[str, str] | None = None) -> None:
    print(f"$ {' '.join(command)}")
    subprocess.run(command, cwd=ROOT, check=True, env=env)


def main() -> None:
    env = dict(os.environ)
    env.setdefault("MPLCONFIGDIR", "/tmp/mpl")

    run([sys.executable, "scripts/run_baseline.py", "--episodes", "2"], env=env)
    run([sys.executable, "scripts/run_issue_case.py", "--case", "actuator_gain_overshoot"], env=env)
    run(
        [
            sys.executable,
            "scripts/generate_diagnostics_bundle.py",
            "--summary",
            "outputs/baseline/summary.json",
            "--label",
            "baseline",
            "--summary",
            "outputs/interesting_sweeps/actuator_gain_18p0/summary.json",
            "--label",
            "actuator_gain_18",
        ],
        env=env,
    )
    run(
        [
            sys.executable,
            "scripts/train_torch_policy.py",
            "--dataset-episodes",
            "4",
            "--epochs",
            "3",
        ],
        env=env,
    )
    run(
        [
            sys.executable,
            "scripts/evaluate_torch_policy.py",
            "--episodes",
            "2",
        ],
        env=env,
    )
    run(
        [
            sys.executable,
            "scripts/generate_demo_gif.py",
            "--trace",
            "outputs/learning/evaluation/traces/episode_000.json",
            "--output",
            "outputs/media/reacher_demo.gif",
            "--title",
            "PyTorch policy rollout",
        ],
        env=env,
    )
    run([sys.executable, "scripts/backfill_provenance_manifests.py"], env=env)
    run([sys.executable, "scripts/build_provenance_index.py"], env=env)
    run([sys.executable, "scripts/generate_anomaly_report.py"], env=env)
    run([sys.executable, "scripts/generate_recommendations.py"], env=env)
    run([sys.executable, "scripts/generate_triage_queue.py"], env=env)
    run([sys.executable, "scripts/generate_incident_bundles.py"], env=env)
    run([sys.executable, "scripts/generate_knowledge_base.py"], env=env)
    run([sys.executable, "scripts/generate_escalation_matrix.py"], env=env)
    run([sys.executable, "scripts/generate_support_ops_report.py"], env=env)
    run([sys.executable, "scripts/generate_support_gap_report.py"], env=env)
    run([sys.executable, "scripts/generate_workstream_plan.py"], env=env)
    run([sys.executable, "scripts/generate_sla_report.py"], env=env)
    run([sys.executable, "scripts/generate_capacity_plan.py"], env=env)
    run([sys.executable, "scripts/generate_ops_review.py"], env=env)
    run([sys.executable, "scripts/generate_support_readiness.py"], env=env)
    run([sys.executable, "scripts/generate_scenario_plan.py"], env=env)
    run([sys.executable, "scripts/generate_artifact_freshness.py"], env=env)
    run([sys.executable, "scripts/generate_regeneration_plan.py"], env=env)
    run([sys.executable, "scripts/generate_dependency_map.py"], env=env)
    run([sys.executable, "scripts/generate_impact_analysis.py"], env=env)
    run([sys.executable, "scripts/generate_refresh_bundle.py"], env=env)
    run([sys.executable, "scripts/generate_refresh_checklist.py"], env=env)
    run([sys.executable, "scripts/generate_maintenance_risk.py"], env=env)
    run([sys.executable, "scripts/generate_artifact_readiness.py"], env=env)
    run([sys.executable, "scripts/generate_artifact_scenarios.py"], env=env)
    run([sys.executable, "scripts/generate_artifact_recovery.py"], env=env)
    run([sys.executable, "scripts/generate_artifact_delivery.py"], env=env)
    run([sys.executable, "scripts/generate_artifact_capacity.py"], env=env)
    run([sys.executable, "scripts/generate_artifact_exec_summary.py"], env=env)
    run([sys.executable, "scripts/generate_artifact_history.py"], env=env)
    run([sys.executable, "scripts/generate_artifact_actions.py"], env=env)
    run([sys.executable, "scripts/generate_artifact_alerts.py"], env=env)
    run([sys.executable, "scripts/generate_artifact_digest.py"], env=env)
    run([sys.executable, "scripts/generate_artifact_handoff.py"], env=env)
    run([sys.executable, "scripts/generate_artifact_review_note.py"], env=env)
    run([sys.executable, "scripts/generate_artifact_closeout.py"], env=env)
    run([sys.executable, "scripts/generate_artifact_scorecard.py"], env=env)
    run([sys.executable, "scripts/generate_artifact_packet.py"], env=env)
    run([sys.executable, "scripts/generate_dashboard_snapshot.py"], env=env)
    run([sys.executable, "scripts/generate_dashboard_snapshot_history.py"], env=env)
    run([sys.executable, "scripts/generate_dashboard_snapshot_drift.py"], env=env)
    run([sys.executable, "scripts/generate_dashboard_snapshot_alerts.py"], env=env)
    run([sys.executable, "scripts/generate_dashboard_snapshot_monitor.py"], env=env)
    run([sys.executable, "scripts/generate_dashboard_snapshot_review.py"], env=env)
    run([sys.executable, "scripts/generate_dashboard_snapshot_handoff.py"], env=env)
    run([sys.executable, "scripts/generate_dashboard_snapshot_closeout.py"], env=env)
    run([sys.executable, "scripts/generate_dashboard_snapshot_scorecard.py"], env=env)
    run([sys.executable, "scripts/generate_dashboard_snapshot_digest.py"], env=env)
    run([sys.executable, "scripts/generate_dashboard_snapshot_actions.py"], env=env)
    run([sys.executable, "scripts/generate_dashboard_snapshot_alert_packet.py"], env=env)
    run([sys.executable, "scripts/generate_dashboard_snapshot_resolution_plan.py"], env=env)
    run([sys.executable, "scripts/generate_dashboard_snapshot_execution_board.py"], env=env)
    run([sys.executable, "scripts/generate_dashboard_snapshot_owner_load.py"], env=env)
    run([sys.executable, "scripts/generate_dashboard_snapshot_readiness_gate.py"], env=env)
    run(
        [
            sys.executable,
            "scripts/generate_release_notes.py",
            "--base",
            "9947b32",
            "--head",
            "HEAD",
            "--output-dir",
            "outputs/releases/latest",
        ],
        env=env,
    )
    run([sys.executable, "scripts/generate_dashboard.py"], env=env)

    summary_path = ROOT / "outputs" / "support_cases" / "actuator_gain_overshoot.md"
    if not summary_path.exists():
        raise SystemExit(f"Expected support case output at {summary_path}")
    diagnostics_path = ROOT / "outputs" / "diagnostics" / "diagnostics.md"
    if not diagnostics_path.exists():
        raise SystemExit(f"Expected diagnostics bundle at {diagnostics_path}")
    learning_checkpoint = ROOT / "outputs" / "learning" / "training" / "policy.pt"
    if not learning_checkpoint.exists():
        raise SystemExit(f"Expected policy checkpoint at {learning_checkpoint}")
    demo_gif = ROOT / "outputs" / "media" / "reacher_demo.gif"
    if not demo_gif.exists():
        raise SystemExit(f"Expected demo GIF at {demo_gif}")
    dashboard_data = ROOT / "dashboard" / "data.json"
    if not dashboard_data.exists():
        raise SystemExit(f"Expected dashboard data at {dashboard_data}")
    provenance_index = ROOT / "outputs" / "provenance" / "index.json"
    if not provenance_index.exists():
        raise SystemExit(f"Expected provenance index at {provenance_index}")
    release_notes = ROOT / "outputs" / "releases" / "latest" / "release_notes.json"
    if not release_notes.exists():
        raise SystemExit(f"Expected release notes at {release_notes}")
    anomaly_report = ROOT / "outputs" / "anomalies" / "anomaly_report.json"
    if not anomaly_report.exists():
        raise SystemExit(f"Expected anomaly report at {anomaly_report}")
    recommendation_report = ROOT / "outputs" / "recommendations" / "recommendations.json"
    if not recommendation_report.exists():
        raise SystemExit(f"Expected recommendations at {recommendation_report}")
    triage_queue = ROOT / "outputs" / "triage" / "triage_queue.json"
    if not triage_queue.exists():
        raise SystemExit(f"Expected triage queue at {triage_queue}")
    incidents_index = ROOT / "outputs" / "incidents" / "index.json"
    if not incidents_index.exists():
        raise SystemExit(f"Expected incident bundles at {incidents_index}")
    knowledge_base = ROOT / "outputs" / "knowledge_base" / "index.json"
    if not knowledge_base.exists():
        raise SystemExit(f"Expected knowledge base at {knowledge_base}")
    escalation = ROOT / "outputs" / "escalation" / "escalation_matrix.json"
    if not escalation.exists():
        raise SystemExit(f"Expected escalation matrix at {escalation}")
    support_ops = ROOT / "outputs" / "support_ops" / "support_ops.json"
    if not support_ops.exists():
        raise SystemExit(f"Expected support ops report at {support_ops}")
    support_gaps = ROOT / "outputs" / "support_gaps" / "support_gaps.json"
    if not support_gaps.exists():
        raise SystemExit(f"Expected support gap report at {support_gaps}")
    workstreams = ROOT / "outputs" / "workstreams" / "workstream_plan.json"
    if not workstreams.exists():
        raise SystemExit(f"Expected workstream plan at {workstreams}")
    sla = ROOT / "outputs" / "sla" / "sla_report.json"
    if not sla.exists():
        raise SystemExit(f"Expected SLA report at {sla}")
    capacity = ROOT / "outputs" / "capacity" / "capacity_plan.json"
    if not capacity.exists():
        raise SystemExit(f"Expected capacity plan at {capacity}")
    ops_review = ROOT / "outputs" / "ops_review" / "ops_review.json"
    if not ops_review.exists():
        raise SystemExit(f"Expected ops review at {ops_review}")
    support_readiness = ROOT / "outputs" / "support_readiness" / "support_readiness.json"
    if not support_readiness.exists():
        raise SystemExit(f"Expected support readiness report at {support_readiness}")
    scenario_plan = ROOT / "outputs" / "scenario_plan" / "scenario_plan.json"
    if not scenario_plan.exists():
        raise SystemExit(f"Expected scenario plan at {scenario_plan}")
    artifact_freshness = ROOT / "outputs" / "artifact_freshness" / "artifact_freshness.json"
    if not artifact_freshness.exists():
        raise SystemExit(f"Expected artifact freshness report at {artifact_freshness}")
    regeneration_plan = ROOT / "outputs" / "regeneration_plan" / "regeneration_plan.json"
    if not regeneration_plan.exists():
        raise SystemExit(f"Expected regeneration plan at {regeneration_plan}")
    dependency_map = ROOT / "outputs" / "dependency_map" / "dependency_map.json"
    if not dependency_map.exists():
        raise SystemExit(f"Expected dependency map at {dependency_map}")
    impact_analysis = ROOT / "outputs" / "impact_analysis" / "impact_analysis.json"
    if not impact_analysis.exists():
        raise SystemExit(f"Expected impact analysis at {impact_analysis}")
    refresh_bundle = ROOT / "outputs" / "refresh_bundle" / "refresh_bundle.json"
    if not refresh_bundle.exists():
        raise SystemExit(f"Expected refresh bundle at {refresh_bundle}")
    refresh_checklist = ROOT / "outputs" / "refresh_checklist" / "refresh_checklist.json"
    if not refresh_checklist.exists():
        raise SystemExit(f"Expected refresh checklist at {refresh_checklist}")
    maintenance_risk = ROOT / "outputs" / "maintenance_risk" / "maintenance_risk.json"
    if not maintenance_risk.exists():
        raise SystemExit(f"Expected maintenance risk report at {maintenance_risk}")
    artifact_readiness = ROOT / "outputs" / "artifact_readiness" / "artifact_readiness.json"
    if not artifact_readiness.exists():
        raise SystemExit(f"Expected artifact readiness report at {artifact_readiness}")
    artifact_scenarios = ROOT / "outputs" / "artifact_scenarios" / "artifact_scenarios.json"
    if not artifact_scenarios.exists():
        raise SystemExit(f"Expected artifact scenarios report at {artifact_scenarios}")
    artifact_recovery = ROOT / "outputs" / "artifact_recovery" / "artifact_recovery.json"
    if not artifact_recovery.exists():
        raise SystemExit(f"Expected artifact recovery report at {artifact_recovery}")
    artifact_delivery = ROOT / "outputs" / "artifact_delivery" / "artifact_delivery.json"
    if not artifact_delivery.exists():
        raise SystemExit(f"Expected artifact delivery report at {artifact_delivery}")
    artifact_capacity = ROOT / "outputs" / "artifact_capacity" / "artifact_capacity.json"
    if not artifact_capacity.exists():
        raise SystemExit(f"Expected artifact capacity report at {artifact_capacity}")
    artifact_exec_summary = ROOT / "outputs" / "artifact_exec_summary" / "artifact_exec_summary.json"
    if not artifact_exec_summary.exists():
        raise SystemExit(f"Expected artifact executive summary at {artifact_exec_summary}")
    artifact_history = ROOT / "outputs" / "artifact_history" / "artifact_history.json"
    if not artifact_history.exists():
        raise SystemExit(f"Expected artifact history at {artifact_history}")
    artifact_actions = ROOT / "outputs" / "artifact_actions" / "artifact_actions.json"
    if not artifact_actions.exists():
        raise SystemExit(f"Expected artifact actions at {artifact_actions}")
    artifact_alerts = ROOT / "outputs" / "artifact_alerts" / "artifact_alerts.json"
    if not artifact_alerts.exists():
        raise SystemExit(f"Expected artifact alerts at {artifact_alerts}")
    artifact_digest = ROOT / "outputs" / "artifact_digest" / "artifact_digest.json"
    if not artifact_digest.exists():
        raise SystemExit(f"Expected artifact digest at {artifact_digest}")
    artifact_handoff = ROOT / "outputs" / "artifact_handoff" / "artifact_handoff.json"
    if not artifact_handoff.exists():
        raise SystemExit(f"Expected artifact handoff at {artifact_handoff}")
    artifact_review_note = ROOT / "outputs" / "artifact_review_note" / "artifact_review_note.json"
    if not artifact_review_note.exists():
        raise SystemExit(f"Expected artifact review note at {artifact_review_note}")
    artifact_closeout = ROOT / "outputs" / "artifact_closeout" / "artifact_closeout.json"
    if not artifact_closeout.exists():
        raise SystemExit(f"Expected artifact closeout at {artifact_closeout}")
    artifact_scorecard = ROOT / "outputs" / "artifact_scorecard" / "artifact_scorecard.json"
    if not artifact_scorecard.exists():
        raise SystemExit(f"Expected artifact scorecard at {artifact_scorecard}")
    artifact_packet = ROOT / "outputs" / "artifact_packet" / "artifact_packet.json"
    if not artifact_packet.exists():
        raise SystemExit(f"Expected artifact packet at {artifact_packet}")
    dashboard_snapshot = ROOT / "outputs" / "dashboard_snapshots" / "latest.json"
    if not dashboard_snapshot.exists():
        raise SystemExit(f"Expected dashboard snapshot at {dashboard_snapshot}")
    dashboard_snapshot_history = ROOT / "outputs" / "dashboard_snapshots" / "history.json"
    if not dashboard_snapshot_history.exists():
        raise SystemExit(f"Expected dashboard snapshot history at {dashboard_snapshot_history}")
    dashboard_snapshot_drift = ROOT / "outputs" / "dashboard_snapshots" / "drift.json"
    if not dashboard_snapshot_drift.exists():
        raise SystemExit(f"Expected dashboard snapshot drift at {dashboard_snapshot_drift}")
    dashboard_snapshot_alerts = ROOT / "outputs" / "dashboard_snapshots" / "alerts.json"
    if not dashboard_snapshot_alerts.exists():
        raise SystemExit(f"Expected dashboard snapshot alerts at {dashboard_snapshot_alerts}")
    dashboard_snapshot_monitor = ROOT / "outputs" / "dashboard_snapshots" / "monitor.json"
    if not dashboard_snapshot_monitor.exists():
        raise SystemExit(f"Expected dashboard snapshot monitor at {dashboard_snapshot_monitor}")
    dashboard_snapshot_review = ROOT / "outputs" / "dashboard_snapshots" / "review.json"
    if not dashboard_snapshot_review.exists():
        raise SystemExit(f"Expected dashboard snapshot review at {dashboard_snapshot_review}")
    dashboard_snapshot_handoff = ROOT / "outputs" / "dashboard_snapshots" / "handoff.json"
    if not dashboard_snapshot_handoff.exists():
        raise SystemExit(f"Expected dashboard snapshot handoff at {dashboard_snapshot_handoff}")
    dashboard_snapshot_closeout = ROOT / "outputs" / "dashboard_snapshots" / "closeout.json"
    if not dashboard_snapshot_closeout.exists():
        raise SystemExit(f"Expected dashboard snapshot closeout at {dashboard_snapshot_closeout}")
    dashboard_snapshot_scorecard = ROOT / "outputs" / "dashboard_snapshots" / "scorecard.json"
    if not dashboard_snapshot_scorecard.exists():
        raise SystemExit(f"Expected dashboard snapshot scorecard at {dashboard_snapshot_scorecard}")
    dashboard_snapshot_digest = ROOT / "outputs" / "dashboard_snapshots" / "digest.json"
    if not dashboard_snapshot_digest.exists():
        raise SystemExit(f"Expected dashboard snapshot digest at {dashboard_snapshot_digest}")
    dashboard_snapshot_actions = ROOT / "outputs" / "dashboard_snapshots" / "actions.json"
    if not dashboard_snapshot_actions.exists():
        raise SystemExit(f"Expected dashboard snapshot actions at {dashboard_snapshot_actions}")
    dashboard_snapshot_alert_packet = ROOT / "outputs" / "dashboard_snapshots" / "alert_packet.json"
    if not dashboard_snapshot_alert_packet.exists():
        raise SystemExit(f"Expected dashboard snapshot alert packet at {dashboard_snapshot_alert_packet}")
    dashboard_snapshot_resolution_plan = ROOT / "outputs" / "dashboard_snapshots" / "resolution_plan.json"
    if not dashboard_snapshot_resolution_plan.exists():
        raise SystemExit(f"Expected dashboard snapshot resolution plan at {dashboard_snapshot_resolution_plan}")
    dashboard_snapshot_execution_board = ROOT / "outputs" / "dashboard_snapshots" / "execution_board.json"
    if not dashboard_snapshot_execution_board.exists():
        raise SystemExit(f"Expected dashboard snapshot execution board at {dashboard_snapshot_execution_board}")
    dashboard_snapshot_owner_load = ROOT / "outputs" / "dashboard_snapshots" / "owner_load.json"
    if not dashboard_snapshot_owner_load.exists():
        raise SystemExit(f"Expected dashboard snapshot owner load at {dashboard_snapshot_owner_load}")
    dashboard_snapshot_readiness_gate = ROOT / "outputs" / "dashboard_snapshots" / "readiness_gate.json"
    if not dashboard_snapshot_readiness_gate.exists():
        raise SystemExit(f"Expected dashboard snapshot readiness gate at {dashboard_snapshot_readiness_gate}")

    payload = json.loads((ROOT / "outputs" / "baseline" / "summary.json").read_text())
    print("Baseline success rate:", payload["summary"]["success_rate"])
    print("Smoke test complete.")


if __name__ == "__main__":
    main()
