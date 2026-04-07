# Dashboard Snapshot Readiness Gate Guide

The dashboard snapshot readiness gate turns the current owner-load and closeout state into a pass/warn/fail decision.

It highlights:

- whether the snapshot state is ready
- how many hard failures remain
- whether residual warning pressure still exists

Generate it with:

```bash
python scripts/generate_dashboard_snapshot_readiness_gate.py
```

The outputs are written to:

- `outputs/dashboard_snapshots/readiness_gate.json`
- `outputs/dashboard_snapshots/readiness_gate.md`
