# Artifact Alerts Guide

## What this report does

The artifact-alert layer converts the artifact-health stack into short operator-style notifications.

It highlights:

- failing readiness
- breaching recovery phases
- overloaded owners
- immediate next actions

## Generate the alerts

```bash
python scripts/generate_artifact_alerts.py
```

This writes:

- `outputs/artifact_alerts/artifact_alerts.json`
- `outputs/artifact_alerts/artifact_alerts.md`

## Why it matters

This gives the repo a lightweight signal layer that sits above the longer reports.
