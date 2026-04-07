# Artifact Executive Summary Guide

## What this report does

The artifact executive summary compresses the full artifact-maintenance stack into one leadership-style note.

It highlights:

- current readiness status
- top artifact risk
- current breach phase
- overloaded owner
- immediate recommended actions

## Generate the summary

```bash
python scripts/generate_artifact_exec_summary.py
```

This writes:

- `outputs/artifact_exec_summary/artifact_exec_summary.json`
- `outputs/artifact_exec_summary/artifact_exec_summary.md`

## Why it matters

This gives the repo a concise top layer above the more detailed maintenance artifacts.
