# Artifact Closeout Guide

## What this report does

The artifact closeout report decides whether the current recovery cycle is ready to close.

It summarizes:

- current review status
- projected terminal status
- remaining blockers
- remaining actions

## Generate the closeout

```bash
python scripts/generate_artifact_closeout.py
```

This writes:

- `outputs/artifact_closeout/artifact_closeout.json`
- `outputs/artifact_closeout/artifact_closeout.md`

## Why it matters

This gives the repo a final gate at the end of the artifact-maintenance workflow.
