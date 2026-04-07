# Regression Guide

This repository includes regression tracking to snapshot key outputs and compare them over time.

## Why this exists

Experiment-heavy projects often change quickly. Regression tracking makes it easier to notice when a refactor, controller tweak, or training change quietly improves or degrades behavior.

## Commands

Create a snapshot:

```bash
python scripts/create_regression_snapshot.py --name current
```

Compare two snapshots:

```bash
python scripts/compare_regression_snapshots.py \
  --left outputs/regression/snapshots/baseline_reference.json \
  --right outputs/regression/snapshots/current.json
```

Evaluate the diff against configured thresholds:

```bash
python scripts/check_regressions.py \
  --left outputs/regression/snapshots/baseline_reference.json \
  --right outputs/regression/snapshots/current.json \
  --thresholds configs/regression_thresholds.json \
  --output-dir outputs/regression/gate
```

## Outputs

- `outputs/regression/snapshots/*.json`
- `outputs/regression/latest_diff/regression_diff.json`
- `outputs/regression/latest_diff/regression_diff.md`
- `outputs/regression/latest_diff/regression_diff.png`
- `outputs/regression/gate/regression_gate.json`
- `outputs/regression/gate/regression_gate.md`

## Threshold policy

The default policy lives in `configs/regression_thresholds.json`.

- Success-rate metrics use minimum allowed deltas so modest noise is tolerated while real drops are flagged.
- Error metrics use maximum allowed deltas so rising final error is treated as a regression.
- Controller-level checks support either controller-specific overrides or a `*` default per metric family.
