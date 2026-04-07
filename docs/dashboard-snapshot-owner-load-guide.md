# Dashboard Snapshot Owner Load Guide

The dashboard snapshot owner load report summarizes how much execution pressure is currently assigned to the active owner.

It captures:

- active versus planned lanes
- active versus planned items
- critical and warning alert pressure

Generate it with:

```bash
python scripts/generate_dashboard_snapshot_owner_load.py
```

The outputs are written to:

- `outputs/dashboard_snapshots/owner_load.json`
- `outputs/dashboard_snapshots/owner_load.md`
