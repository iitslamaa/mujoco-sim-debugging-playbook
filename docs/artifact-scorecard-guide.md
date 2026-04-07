# Artifact Scorecard Guide

## What this report does

The artifact scorecard is a one-screen KPI summary for the artifact-maintenance stack.

It captures:

- current status
- closeout status
- projected terminal status
- failure count
- top risk score
- critical alerts
- remaining actions
- trend direction

## Generate the scorecard

```bash
python scripts/generate_artifact_scorecard.py
```

This writes:

- `outputs/artifact_scorecard/artifact_scorecard.json`
- `outputs/artifact_scorecard/artifact_scorecard.md`

## Why it matters

This gives the repo a compact metrics surface above the longer narrative artifacts.
