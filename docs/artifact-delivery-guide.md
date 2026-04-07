# Artifact Delivery Guide

## What this report does

The artifact-delivery layer forecasts whether the artifact recovery phases are likely to stay on track.

It combines:

- the phased recovery roadmap
- maintenance-risk scores
- refresh-bundle structure

## Generate the report

```bash
python scripts/generate_artifact_delivery.py
```

This writes:

- `outputs/artifact_delivery/artifact_delivery.json`
- `outputs/artifact_delivery/artifact_delivery.md`

## Why it matters

This makes the repo feel more operationally complete:

- recovery says what to do
- delivery says which phases are most likely to slip
