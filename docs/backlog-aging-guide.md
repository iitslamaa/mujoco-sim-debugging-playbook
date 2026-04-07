# Backlog Aging Guide

The backlog-aging report is a lightweight support-debt view.

Each item receives an `aging_score` based on:

- due horizon
- workstream effort
- extra weight for `breach` and `at_risk` status

Buckets are intended for quick review:

- `fresh`: not urgent yet
- `warming`: worth planning around
- `stale`: should be treated as latent support debt
