# Artifact Capacity Guide

## What this report does

The artifact-capacity layer translates delivery risk into staffing and ownership recommendations.

It answers:

- which recovery phases are overloaded
- which owners are carrying too much command volume
- which artifacts should be reassigned to reduce breach risk

## Generate the plan

```bash
python scripts/generate_artifact_capacity.py
```

This writes:

- `outputs/artifact_capacity/artifact_capacity.json`
- `outputs/artifact_capacity/artifact_capacity.md`

## Why it matters

This closes another operational loop in the repo:

- delivery says which phases will slip
- capacity says how to redistribute the work
