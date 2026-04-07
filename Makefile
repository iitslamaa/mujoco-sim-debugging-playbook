PYTHON ?= .venv/bin/python
PIP ?= .venv/bin/pip

.PHONY: install test baseline sweep smoke support-case diagnostics compare train-policy eval-policy train-rl eval-rl benchmark randomization anomalies recommendations triage incidents knowledge-base escalation support-ops support-gaps workstreams sla capacity ops-review support-readiness scenario-plan responder-load backlog-aging documentation-audit risk-register owner-alerts release-packet evidence-inventory action-register scorecard briefing-note artifact-freshness regeneration-plan case-studies snapshot regression-diff regression-check regression-history provenance release-notes demo-gif dashboard format-help

install:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e . --no-build-isolation

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
