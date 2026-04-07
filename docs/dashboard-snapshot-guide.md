# Dashboard Snapshot Guide

## What this report does

The dashboard snapshot captures a lightweight static summary of the live dashboard state.

It includes:

- repo name
- baseline success rate
- artifact packet summary
- short highlights

## Generate the snapshot

```bash
python scripts/generate_dashboard_snapshot.py
```

This writes:

- `outputs/dashboard_snapshots/latest.json`
- `outputs/dashboard_snapshots/latest.md`

## Why it matters

This gives the repo a simple preserved snapshot of the dashboard surface over time.
