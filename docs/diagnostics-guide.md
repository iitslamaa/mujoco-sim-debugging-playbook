# Diagnostics Guide

This repo now includes a diagnostics layer intended to look like the kind of artifact bundle you would hand to a user, teammate, or release owner during simulation triage.

## What gets captured

- environment metadata including Python, MuJoCo, NumPy, Git HEAD, and available CLI tooling
- experiment-level summaries with worst-episode pointers
- scenario comparisons with deltas for success, error, overshoot, and oscillation
- per-episode trace plots for quick visual inspection

## Commands

Generate a diagnostics bundle:

```bash
python scripts/generate_diagnostics_bundle.py \
  --summary outputs/baseline/summary.json \
  --label baseline \
  --summary outputs/interesting_sweeps/actuator_gain_18p0/summary.json \
  --label actuator_gain_18
```

Compare two runs directly:

```bash
python scripts/compare_configs.py \
  --left outputs/baseline/summary.json \
  --right outputs/interesting_sweeps/actuator_gain_18p0/summary.json \
  --left-label baseline \
  --right-label actuator_gain_18
```

## Why this matters

A strong support engineer does not only reproduce a bug. They package the evidence in a way that helps other people act:

- users get a clear explanation
- maintainers get reproducible artifacts
- release owners get a validation surface
