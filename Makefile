PYTHON ?= .venv/bin/python
PIP ?= .venv/bin/pip

.PHONY: install test baseline sweep smoke support-case diagnostics compare format-help

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

format-help:
	@echo "No formatter is configured yet. Add one only if it improves reproducibility for contributors."
