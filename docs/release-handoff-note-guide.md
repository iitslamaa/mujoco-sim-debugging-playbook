# Release Handoff Note Guide

`scripts/generate_release_handoff_note.py` turns the release evidence packet and dry-run summary into a short handoff note.

Use it when a release candidate needs to move from validation into formal review.

```bash
make release-handoff-note
```

Outputs:

- `outputs/release_handoff_note/release_handoff_note.json`
- `outputs/release_handoff_note/release_handoff_note.md`
