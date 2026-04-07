# Provenance Guide

This repository tracks experiment provenance with per-run manifests and a repo-level index.

## What gets recorded

- run type
- creation time
- Git SHA, branch, and dirty-state snapshot
- environment details and installed packages
- declared inputs with file hashes
- declared outputs with file hashes and sizes
- run-specific metadata such as summary metrics or row counts

## Commands

Backfill manifests for existing outputs:

```bash
python scripts/backfill_provenance_manifests.py
```

Build the aggregate index:

```bash
python scripts/build_provenance_index.py
```

## Outputs

- `outputs/*/manifest.json`
- `outputs/provenance/index.json`
- `outputs/provenance/index.md`

## Why it helps

The manifests make it easier to answer:

- which commit produced this artifact
- which checkpoint or config fed into this report
- whether an output was generated from a dirty worktree
- whether two artifacts came from the same dependency state
