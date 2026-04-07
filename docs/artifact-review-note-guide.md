# Artifact Review Note Guide

## What this report does

The artifact review note is a short reviewer-facing summary built from the handoff, digest, history, and action register.

It answers:

- what changed
- what still blocks progress
- what should be approved next

## Generate the note

```bash
python scripts/generate_artifact_review_note.py
```

This writes:

- `outputs/artifact_review_note/artifact_review_note.json`
- `outputs/artifact_review_note/artifact_review_note.md`

## Why it matters

This gives the repo a compact reviewer handoff above the broader operational artifacts.
