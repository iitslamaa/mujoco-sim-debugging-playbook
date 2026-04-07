# Dashboard Snapshot Drift Guide

The dashboard snapshot drift report compares consecutive preserved dashboard states and highlights the biggest changes between them.

It answers questions like:

- When did the dashboard state first become `pass`?
- Which transition reduced the most failures?
- Which transition reduced the most maintenance risk?
- How much did the preserved baseline signal move between snapshots?

Generate it with:

```bash
python scripts/generate_dashboard_snapshot_drift.py
```

The outputs are written to:

- `outputs/dashboard_snapshots/drift.json`
- `outputs/dashboard_snapshots/drift.md`
