# Artifact Handoff Guide

## What this report does

The artifact handoff report packages the current artifact-health state for the next owner or shift.

It includes:

- top headlines
- current alerts
- top actions
- owner context

## Generate the handoff

```bash
python scripts/generate_artifact_handoff.py
```

This writes:

- `outputs/artifact_handoff/artifact_handoff.json`
- `outputs/artifact_handoff/artifact_handoff.md`

## Why it matters

This gives the repo a concise transfer artifact for whoever owns the next recovery cycle.
