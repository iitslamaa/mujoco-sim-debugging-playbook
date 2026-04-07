# Release Evidence Packet Guide

`scripts/generate_release_evidence_packet.py` bundles the dry-run verdict, release blockers, and release matrix into one release-review artifact.

Use it when you want a compact packet for a release discussion or validation handoff.

```bash
make release-evidence-packet
```

Outputs:

- `outputs/release_evidence_packet/release_evidence_packet.json`
- `outputs/release_evidence_packet/release_evidence_packet.md`
