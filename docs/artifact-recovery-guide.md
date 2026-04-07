# Artifact Recovery Guide

## What this report does

The artifact-recovery layer turns artifact scenarios into a phased remediation plan.

It answers:

- what to refresh first
- what outcome each phase should produce
- which commands correspond to each phase

## Generate the roadmap

```bash
python scripts/generate_artifact_recovery.py
```

This writes:

- `outputs/artifact_recovery/artifact_recovery.json`
- `outputs/artifact_recovery/artifact_recovery.md`

## Why it matters

This makes the maintenance side of the repo feel more operational:

- readiness says the current state is failing
- scenarios show which interventions help
- recovery turns that into an ordered execution plan
