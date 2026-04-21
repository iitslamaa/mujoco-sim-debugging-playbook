PYTHON ?= .venv/bin/python
PIP ?= .venv/bin/pip

.PHONY: install bootstrap-env debug-bundle debug-bundle-manifest container-smoke compatibility dependency-snapshot docker-context issue-template-audit toolchain-inventory support-case-catalog setup-faq response-rubric support-response-template support-triage-reply support-escalation-brief local-paths-report repro-inventory repro-bundle-index repro-readiness release-checklist release-dry-run environment-diff support-intake-checklist machine-profile bundle-verifier release-matrix machine-readiness bundle-quality bundle-coverage release-blockers release-evidence-packet release-handoff-note support-session-note environment-alignment support-command-catalog test baseline sweep smoke support-case diagnostics compare train-policy eval-policy train-rl eval-rl benchmark earthmoving-benchmark earthmoving-calibration earthmoving-scale earthmoving-sensitivity earthmoving-gate earthmoving-gap earthmoving-review-packet earthmoving-replay earthmoving-dashboard earthmoving-dataset earthmoving-surrogate earthmoving-failure-modes earthmoving-role-brief terrain-kernel-smoke randomization anomalies recommendations triage incidents knowledge-base escalation support-ops support-gaps workstreams sla capacity ops-review support-readiness scenario-plan responder-load backlog-aging documentation-audit risk-register owner-alerts release-packet evidence-inventory action-register scorecard briefing-note artifact-freshness regeneration-plan dependency-map impact-analysis refresh-bundle refresh-checklist maintenance-risk artifact-readiness artifact-scenarios artifact-recovery artifact-delivery artifact-capacity artifact-exec-summary artifact-history artifact-actions artifact-alerts artifact-digest artifact-handoff artifact-review-note artifact-closeout artifact-scorecard artifact-packet environment-doctor dashboard-snapshot dashboard-snapshot-history dashboard-snapshot-drift dashboard-snapshot-alerts dashboard-snapshot-monitor dashboard-snapshot-review dashboard-snapshot-handoff dashboard-snapshot-closeout dashboard-snapshot-scorecard dashboard-snapshot-digest dashboard-snapshot-actions dashboard-snapshot-alert-packet dashboard-snapshot-resolution-plan dashboard-snapshot-execution-board dashboard-snapshot-owner-load dashboard-snapshot-readiness-gate dashboard-snapshot-recovery-forecast dashboard-snapshot-milestones dashboard-snapshot-watchlist dashboard-snapshot-focus dashboard-snapshot-priorities dashboard-snapshot-status-brief dashboard-snapshot-lead case-studies snapshot regression-diff regression-check regression-history provenance release-notes demo-gif dashboard format-help

install:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e . --no-build-isolation

bootstrap-env:
	bash scripts/bootstrap_env.sh

debug-bundle:
	bash scripts/collect_debug_bundle.sh

debug-bundle-manifest:
	$(PYTHON) scripts/generate_debug_bundle_manifest.py

container-smoke:
	bash scripts/run_container_smoke.sh

compatibility:
	$(PYTHON) scripts/generate_compatibility_report.py

dependency-snapshot:
	$(PYTHON) scripts/generate_dependency_snapshot.py

docker-context:
	$(PYTHON) scripts/generate_docker_context.py

issue-template-audit:
	$(PYTHON) scripts/generate_issue_template_audit.py

toolchain-inventory:
	$(PYTHON) scripts/generate_toolchain_inventory.py

support-case-catalog:
	$(PYTHON) scripts/generate_support_case_catalog.py

setup-faq:
	$(PYTHON) scripts/generate_setup_faq.py

response-rubric:
	$(PYTHON) scripts/generate_response_rubric.py

support-response-template:
	$(PYTHON) scripts/generate_support_response_template.py

support-triage-reply:
	$(PYTHON) scripts/generate_support_triage_reply.py

support-escalation-brief:
	$(PYTHON) scripts/generate_support_escalation_brief.py

local-paths-report:
	$(PYTHON) scripts/generate_local_paths_report.py

release-checklist:
	$(PYTHON) scripts/generate_release_checklist.py

release-dry-run:
	$(PYTHON) scripts/generate_release_dry_run.py

environment-diff:
	$(PYTHON) scripts/generate_environment_diff.py

support-intake-checklist:
	$(PYTHON) scripts/generate_support_intake_checklist.py

machine-profile:
	$(PYTHON) scripts/generate_machine_profile.py

bundle-verifier:
	$(PYTHON) scripts/generate_bundle_verifier.py

release-matrix:
	$(PYTHON) scripts/generate_release_matrix.py

machine-readiness:
	$(PYTHON) scripts/generate_machine_readiness.py

bundle-quality:
	$(PYTHON) scripts/generate_bundle_quality.py

bundle-coverage:
	$(PYTHON) scripts/generate_bundle_coverage.py

release-blockers:
	$(PYTHON) scripts/generate_release_blockers.py

release-evidence-packet:
	$(PYTHON) scripts/generate_release_evidence_packet.py

release-handoff-note:
	$(PYTHON) scripts/generate_release_handoff_note.py

support-session-note:
	$(PYTHON) scripts/generate_support_session_note.py

environment-alignment:
	$(PYTHON) scripts/generate_environment_alignment.py

support-command-catalog:
	$(PYTHON) scripts/generate_support_command_catalog.py

repro-inventory:
	$(PYTHON) scripts/generate_repro_inventory.py

repro-bundle-index:
	$(PYTHON) scripts/generate_repro_bundle_index.py

repro-readiness:
	$(PYTHON) scripts/generate_repro_readiness.py

test:
	$(PYTHON) -m pytest -q

baseline:
	$(PYTHON) scripts/run_baseline.py --episodes 8

sweep:
	MPLCONFIGDIR=/tmp/mpl $(PYTHON) scripts/run_sweep.py --config configs/interesting_sweeps.json

smoke:
	MPLCONFIGDIR=/tmp/mpl $(PYTHON) scripts/smoke_test.py

support-case:
	$(PYTHON) scripts/run_issue_case.py --case actuator_gain_overshoot

diagnostics:
	$(PYTHON) scripts/generate_diagnostics_bundle.py \
		--summary outputs/baseline/summary.json \
		--label baseline \
		--summary outputs/interesting_sweeps/actuator_gain_18p0/summary.json \
		--label actuator_gain_18

compare:
	$(PYTHON) scripts/compare_configs.py \
		--left outputs/baseline/summary.json \
		--right outputs/interesting_sweeps/actuator_gain_18p0/summary.json \
		--left-label baseline \
		--right-label actuator_gain_18

train-policy:
	MPLCONFIGDIR=/tmp/mpl $(PYTHON) scripts/train_torch_policy.py --dataset-episodes 20 --epochs 80

eval-policy:
	MPLCONFIGDIR=/tmp/mpl $(PYTHON) scripts/evaluate_torch_policy.py --episodes 8

train-rl:
	MPLCONFIGDIR=/tmp/mpl $(PYTHON) scripts/train_rl_policy.py --iterations 12 --episodes-per-iteration 6

eval-rl:
	MPLCONFIGDIR=/tmp/mpl $(PYTHON) scripts/evaluate_rl_policy.py --episodes 8

benchmark:
	MPLCONFIGDIR=/tmp/mpl $(PYTHON) scripts/run_controller_benchmark.py

earthmoving-benchmark:
	MPLCONFIGDIR=/tmp/mpl $(PYTHON) scripts/run_earthmoving_benchmark.py

earthmoving-calibration:
	$(PYTHON) scripts/calibrate_earthmoving_soil.py

earthmoving-scale:
	$(PYTHON) scripts/run_earthmoving_scale.py

earthmoving-sensitivity:
	$(PYTHON) scripts/run_earthmoving_sensitivity.py

earthmoving-gate:
	$(PYTHON) scripts/check_earthmoving_gate.py

earthmoving-gap:
	$(PYTHON) scripts/generate_earthmoving_gap_report.py

earthmoving-review-packet:
	$(PYTHON) scripts/generate_earthmoving_review_packet.py

earthmoving-replay:
	$(PYTHON) scripts/generate_earthmoving_replay.py

earthmoving-dashboard:
	$(PYTHON) scripts/generate_earthmoving_dashboard.py

earthmoving-dataset:
	$(PYTHON) scripts/generate_earthmoving_dataset.py

earthmoving-surrogate:
	$(PYTHON) scripts/train_earthmoving_surrogate.py

earthmoving-failure-modes:
	$(PYTHON) scripts/generate_earthmoving_failure_modes.py

earthmoving-role-brief:
	$(PYTHON) scripts/generate_earthmoving_role_brief.py

terrain-kernel-smoke:
	bash scripts/build_terrain_kernel.sh

randomization:
	MPLCONFIGDIR=/tmp/mpl $(PYTHON) scripts/run_domain_randomization.py

anomalies:
	MPLCONFIGDIR=/tmp/mpl $(PYTHON) scripts/generate_anomaly_report.py

recommendations:
	$(PYTHON) scripts/generate_recommendations.py

triage:
	$(PYTHON) scripts/generate_triage_queue.py

incidents:
	$(PYTHON) scripts/generate_incident_bundles.py

knowledge-base:
	$(PYTHON) scripts/generate_knowledge_base.py

escalation:
	$(PYTHON) scripts/generate_escalation_matrix.py

support-ops:
	$(PYTHON) scripts/generate_support_ops_report.py

support-gaps:
	$(PYTHON) scripts/generate_support_gap_report.py

workstreams:
	$(PYTHON) scripts/generate_workstream_plan.py

sla:
	$(PYTHON) scripts/generate_sla_report.py

capacity:
	$(PYTHON) scripts/generate_capacity_plan.py

ops-review:
	$(PYTHON) scripts/generate_ops_review.py

support-readiness:
	$(PYTHON) scripts/generate_support_readiness.py

scenario-plan:
	$(PYTHON) scripts/generate_scenario_plan.py

responder-load:
	$(PYTHON) scripts/generate_responder_load.py

backlog-aging:
	$(PYTHON) scripts/generate_backlog_aging.py

documentation-audit:
	$(PYTHON) scripts/generate_documentation_audit.py

risk-register:
	$(PYTHON) scripts/generate_risk_register.py

owner-alerts:
	$(PYTHON) scripts/generate_owner_alerts.py

release-packet:
	$(PYTHON) scripts/generate_release_packet.py

evidence-inventory:
	$(PYTHON) scripts/generate_evidence_inventory.py

action-register:
	$(PYTHON) scripts/generate_action_register.py

scorecard:
	$(PYTHON) scripts/generate_scorecard.py

briefing-note:
	$(PYTHON) scripts/generate_briefing_note.py

artifact-freshness:
	$(PYTHON) scripts/generate_artifact_freshness.py

regeneration-plan:
	$(PYTHON) scripts/generate_regeneration_plan.py

dependency-map:
	$(PYTHON) scripts/generate_dependency_map.py

impact-analysis:
	$(PYTHON) scripts/generate_impact_analysis.py

refresh-bundle:
	$(PYTHON) scripts/generate_refresh_bundle.py

refresh-checklist:
	$(PYTHON) scripts/generate_refresh_checklist.py

maintenance-risk:
	$(PYTHON) scripts/generate_maintenance_risk.py

artifact-readiness:
	$(PYTHON) scripts/generate_artifact_readiness.py

artifact-scenarios:
	$(PYTHON) scripts/generate_artifact_scenarios.py

artifact-recovery:
	$(PYTHON) scripts/generate_artifact_recovery.py

artifact-delivery:
	$(PYTHON) scripts/generate_artifact_delivery.py

artifact-capacity:
	$(PYTHON) scripts/generate_artifact_capacity.py

artifact-exec-summary:
	$(PYTHON) scripts/generate_artifact_exec_summary.py

artifact-history:
	$(PYTHON) scripts/generate_artifact_history.py

artifact-actions:
	$(PYTHON) scripts/generate_artifact_actions.py

artifact-alerts:
	$(PYTHON) scripts/generate_artifact_alerts.py

artifact-digest:
	$(PYTHON) scripts/generate_artifact_digest.py

artifact-handoff:
	$(PYTHON) scripts/generate_artifact_handoff.py

artifact-review-note:
	$(PYTHON) scripts/generate_artifact_review_note.py

artifact-closeout:
	$(PYTHON) scripts/generate_artifact_closeout.py

artifact-scorecard:
	$(PYTHON) scripts/generate_artifact_scorecard.py

artifact-packet:
	$(PYTHON) scripts/generate_artifact_packet.py

environment-doctor:
	$(PYTHON) scripts/run_environment_doctor.py

dashboard-snapshot:
	$(PYTHON) scripts/generate_dashboard_snapshot.py

dashboard-snapshot-history:
	$(PYTHON) scripts/generate_dashboard_snapshot_history.py

dashboard-snapshot-drift:
	$(PYTHON) scripts/generate_dashboard_snapshot_drift.py

dashboard-snapshot-alerts:
	$(PYTHON) scripts/generate_dashboard_snapshot_alerts.py

dashboard-snapshot-monitor:
	$(PYTHON) scripts/generate_dashboard_snapshot_monitor.py

dashboard-snapshot-review:
	$(PYTHON) scripts/generate_dashboard_snapshot_review.py

dashboard-snapshot-handoff:
	$(PYTHON) scripts/generate_dashboard_snapshot_handoff.py

dashboard-snapshot-closeout:
	$(PYTHON) scripts/generate_dashboard_snapshot_closeout.py

dashboard-snapshot-scorecard:
	$(PYTHON) scripts/generate_dashboard_snapshot_scorecard.py

dashboard-snapshot-digest:
	$(PYTHON) scripts/generate_dashboard_snapshot_digest.py

dashboard-snapshot-actions:
	$(PYTHON) scripts/generate_dashboard_snapshot_actions.py

dashboard-snapshot-alert-packet:
	$(PYTHON) scripts/generate_dashboard_snapshot_alert_packet.py

dashboard-snapshot-resolution-plan:
	$(PYTHON) scripts/generate_dashboard_snapshot_resolution_plan.py

dashboard-snapshot-execution-board:
	$(PYTHON) scripts/generate_dashboard_snapshot_execution_board.py

dashboard-snapshot-owner-load:
	$(PYTHON) scripts/generate_dashboard_snapshot_owner_load.py

dashboard-snapshot-readiness-gate:
	$(PYTHON) scripts/generate_dashboard_snapshot_readiness_gate.py

dashboard-snapshot-recovery-forecast:
	$(PYTHON) scripts/generate_dashboard_snapshot_recovery_forecast.py

dashboard-snapshot-milestones:
	$(PYTHON) scripts/generate_dashboard_snapshot_milestones.py

dashboard-snapshot-watchlist:
	$(PYTHON) scripts/generate_dashboard_snapshot_watchlist.py

dashboard-snapshot-focus:
	$(PYTHON) scripts/generate_dashboard_snapshot_focus.py

dashboard-snapshot-priorities:
	$(PYTHON) scripts/generate_dashboard_snapshot_priorities.py

dashboard-snapshot-status-brief:
	$(PYTHON) scripts/generate_dashboard_snapshot_status_brief.py

dashboard-snapshot-lead:
	$(PYTHON) scripts/generate_dashboard_snapshot_lead.py

case-studies:
	MPLCONFIGDIR=/tmp/mpl $(PYTHON) scripts/generate_case_studies.py

snapshot:
	$(PYTHON) scripts/create_regression_snapshot.py --name current

regression-diff:
	$(PYTHON) scripts/compare_regression_snapshots.py \
		--left outputs/regression/snapshots/baseline_reference.json \
		--right outputs/regression/snapshots/current.json

regression-check:
	$(PYTHON) scripts/check_regressions.py \
		--left outputs/regression/snapshots/baseline_reference.json \
		--right outputs/regression/snapshots/current.json \
		--thresholds configs/regression_thresholds.json \
		--output-dir outputs/regression/gate

regression-history:
	$(PYTHON) scripts/build_regression_history.py \
		--snapshot-dir outputs/regression/snapshots \
		--output-dir outputs/regression/history \
		--gate-report outputs/regression/gate/regression_gate.json

provenance:
	$(PYTHON) scripts/backfill_provenance_manifests.py
	$(PYTHON) scripts/build_provenance_index.py

release-notes:
	$(PYTHON) scripts/generate_release_notes.py \
		--base 9947b32 \
		--head HEAD \
		--output-dir outputs/releases/latest

demo-gif:
	MPLCONFIGDIR=/tmp/mpl $(PYTHON) scripts/generate_demo_gif.py \
		--trace outputs/learning/evaluation/traces/episode_000.json \
		--output outputs/media/reacher_demo.gif \
		--title "PyTorch policy rollout"

dashboard:
	$(PYTHON) scripts/generate_dashboard.py

format-help:
	@echo "No formatter is configured yet. Add one only if it improves reproducibility for contributors."
