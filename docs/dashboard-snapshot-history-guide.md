# Dashboard Snapshot History Guide

## What this report does

The dashboard snapshot history turns the latest preserved dashboard snapshot plus artifact history into a simple longitudinal summary.

It tracks:

- snapshot status
- failure count
- top risk score
- baseline success rate

## Generate the history

```bash
python scripts/generate_dashboard_snapshot_history.py
```

This writes:

- `outputs/dashboard_snapshots/history.json`
- `outputs/dashboard_snapshots/history.md`

## Why it matters

This gives the repo a lightweight history layer for preserved dashboard summaries.
