# Artifact History Guide

## What this report does

The artifact-history layer gives the repo a simple trend view across past, current, and projected artifact-health snapshots.

It summarizes:

- readiness status direction
- failure-count direction
- breach direction
- top-risk direction

## Generate the history

```bash
python scripts/generate_artifact_history.py
```

This writes:

- `outputs/artifact_history/artifact_history.json`
- `outputs/artifact_history/artifact_history.md`

## Why it matters

This adds one more useful top-level view:

- the executive summary says where things stand now
- artifact history shows whether the system is moving in a better direction
