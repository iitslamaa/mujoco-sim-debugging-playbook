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

Build a historical trend view:

```bash
python scripts/build_regression_history.py \
  --snapshot-dir outputs/regression/snapshots \
  --output-dir outputs/regression/history \
  --gate-report outputs/regression/gate/regression_gate.json
```

## Outputs

- `outputs/regression/snapshots/*.json`
- `outputs/regression/latest_diff/regression_diff.json`
- `outputs/regression/latest_diff/regression_diff.md`
- `outputs/regression/latest_diff/regression_diff.png`
- `outputs/regression/gate/regression_gate.json`
- `outputs/regression/gate/regression_gate.md`
- `outputs/regression/history/history.json`
- `outputs/regression/history/history.md`
- `outputs/regression/history/history.png`

## Threshold policy

The default policy lives in `configs/regression_thresholds.json`.

- Success-rate metrics use minimum allowed deltas so modest noise is tolerated while real drops are flagged.
- Error metrics use maximum allowed deltas so rising final error is treated as a regression.
- Controller-level checks support either controller-specific overrides or a `*` default per metric family.

## History view

The history builder reads all saved snapshots, orders them chronologically, and emits:

- a compact `history.json` payload for dashboards and scripts
- a `history.md` summary with per-metric direction and latest values
- a `history.png` visualization for quick visual inspection
