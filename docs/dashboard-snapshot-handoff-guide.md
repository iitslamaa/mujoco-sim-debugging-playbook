# Dashboard Snapshot Handoff Guide

The dashboard snapshot handoff turns the current review state into a lightweight transfer packet.

It captures:

- who should pick up the next cycle
- the current and projected status
- the most important open items
- the dominant transition in the recent timeline

Generate it with:

```bash
python scripts/generate_dashboard_snapshot_handoff.py
```

The outputs are written to:

- `outputs/dashboard_snapshots/handoff.json`
- `outputs/dashboard_snapshots/handoff.md`
