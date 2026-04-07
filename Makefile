PYTHON ?= .venv/bin/python
PIP ?= .venv/bin/pip

.PHONY: install test baseline sweep smoke support-case diagnostics compare train-policy eval-policy train-rl eval-rl benchmark randomization case-studies demo-gif dashboard format-help

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

case-studies:
	MPLCONFIGDIR=/tmp/mpl $(PYTHON) scripts/generate_case_studies.py

demo-gif:
	MPLCONFIGDIR=/tmp/mpl $(PYTHON) scripts/generate_demo_gif.py \
		--trace outputs/learning/evaluation/traces/episode_000.json \
		--output outputs/media/reacher_demo.gif \
		--title "PyTorch policy rollout"

dashboard:
	$(PYTHON) scripts/generate_dashboard.py

format-help:
	@echo "No formatter is configured yet. Add one only if it improves reproducibility for contributors."
