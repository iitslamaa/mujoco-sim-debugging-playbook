# Dashboard Snapshot Recovery Forecast Guide

The dashboard snapshot recovery forecast estimates the next likely readiness state from the current gate and active plan.

It summarizes:

- the current readiness status
- the projected next status
- forecast confidence
- the plan and alert context behind that projection

Generate it with:

```bash
python scripts/generate_dashboard_snapshot_recovery_forecast.py
```

The outputs are written to:

- `outputs/dashboard_snapshots/recovery_forecast.json`
- `outputs/dashboard_snapshots/recovery_forecast.md`
