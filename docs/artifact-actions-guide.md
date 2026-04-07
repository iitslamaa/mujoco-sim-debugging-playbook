# Artifact Actions Guide

## What this report does

The artifact action register turns the artifact-health stack into a small prioritized queue.

It pulls from:

- executive summary
- delivery forecast
- capacity plan
- artifact history

## Generate the register

```bash
python scripts/generate_artifact_actions.py
```

This writes:

- `outputs/artifact_actions/artifact_actions.json`
- `outputs/artifact_actions/artifact_actions.md`

## Why it matters

This is the most direct execution layer in the artifact stack:

- other reports explain what is happening
- the action register says what to do next
