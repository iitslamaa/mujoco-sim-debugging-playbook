# Artifact Packet Guide

## What this report does

The artifact packet bundles the scorecard, digest, handoff, and closeout views into one release-style package.

It is useful when you want a single artifact to share instead of pointing people at several separate reports.

## Generate the packet

```bash
python scripts/generate_artifact_packet.py
```

This writes:

- `outputs/artifact_packet/artifact_packet.json`
- `outputs/artifact_packet/artifact_packet.md`

## Why it matters

This gives the repo a top-level package artifact for sharing the current maintenance state.
