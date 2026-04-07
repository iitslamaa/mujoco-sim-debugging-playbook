# Dashboard Snapshot Resolution Plan Guide

The dashboard snapshot resolution plan converts the current alert packet and action register into phased work.

It highlights:

- the current owner
- the current alert pressure
- the immediate stabilization phase
- the follow-up cleanup phase

Generate it with:

```bash
python scripts/generate_dashboard_snapshot_resolution_plan.py
```

The outputs are written to:

- `outputs/dashboard_snapshots/resolution_plan.json`
- `outputs/dashboard_snapshots/resolution_plan.md`
