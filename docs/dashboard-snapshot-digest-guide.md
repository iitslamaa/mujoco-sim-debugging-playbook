# Dashboard Snapshot Digest Guide

The dashboard snapshot digest turns the scorecard and closeout state into a compact briefing note.

It summarizes:

- the current status
- the closeout state
- the main attention points
- the remaining open items

Generate it with:

```bash
python scripts/generate_dashboard_snapshot_digest.py
```

The outputs are written to:

- `outputs/dashboard_snapshots/digest.json`
- `outputs/dashboard_snapshots/digest.md`
