# Artifact Scenarios Guide

## What this report does

The artifact-scenarios layer answers a practical question:

What happens to artifact readiness if only part of the refresh plan gets done?

## Generate the report

```bash
python scripts/generate_artifact_scenarios.py
```

This writes:

- `outputs/artifact_scenarios/artifact_scenarios.json`
- `outputs/artifact_scenarios/artifact_scenarios.md`

## Included scenarios

- `Dashboard refresh only`
- `Support report sprint`
- `Top-risk stabilization`
- `Full artifact refresh`

## Why it matters

This makes the repo more realistic operationally:

- artifact readiness says whether the current state is acceptable
- artifact scenarios show which targeted interventions are enough to recover trust in the published outputs
