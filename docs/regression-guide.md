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

## Outputs

- `outputs/regression/snapshots/*.json`
- `outputs/regression/latest_diff/regression_diff.json`
- `outputs/regression/latest_diff/regression_diff.md`
- `outputs/regression/latest_diff/regression_diff.png`

