# Artifact Digest Guide

## What this report does

The artifact digest is a compact briefing layer built from the artifact stack.

It includes:

- short headlines
- top alerts
- top actions

## Generate the digest

```bash
python scripts/generate_artifact_digest.py
```

This writes:

- `outputs/artifact_digest/artifact_digest.json`
- `outputs/artifact_digest/artifact_digest.md`

## Why it matters

This gives the repo a lightweight briefing artifact above the longer maintenance reports.
