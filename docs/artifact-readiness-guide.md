# Artifact Readiness Guide

## What this report does

The artifact-readiness layer makes a simple operational call on whether generated outputs are in a healthy enough state to trust.

It combines:

- freshness status
- maintenance-risk scoring
- regeneration priority
- refresh checklist size

## Generate the report

```bash
python scripts/generate_artifact_readiness.py
```

This writes:

- `outputs/artifact_readiness/artifact_readiness.json`
- `outputs/artifact_readiness/artifact_readiness.md`

## How to read it

- `pass` means the artifact set is current and low risk
- `warn` means the repo is usable, but refresh debt is accumulating
- `fail` means artifact staleness or risk is high enough that the published outputs should not be treated as fully current

## Why it matters

This gives the repo a more realistic publishing story:

- maintenance risk ranks what matters most
- artifact readiness says whether the overall artifact surface is healthy enough right now
