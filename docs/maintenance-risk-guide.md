# Maintenance Risk Guide

## What this report does

The maintenance-risk layer turns stale-artifact detection into a ranked refresh risk view.

Instead of only asking whether an artifact is stale, it asks:

- how stale it is
- whether the refresh is already marked high priority
- how many downstream artifacts depend on it
- how many refresh bundles it participates in

That makes it easier to tell which artifact is most dangerous to leave outdated.

## Generate the report

```bash
python scripts/generate_maintenance_risk.py
```

This writes:

- `outputs/maintenance_risk/maintenance_risk.json`
- `outputs/maintenance_risk/maintenance_risk.md`

## How to read it

- `high risk` means the artifact is stale or missing and also sits on a meaningful downstream path
- `medium risk` means the artifact should be refreshed soon, but the blast radius is smaller
- `top risk artifact` is the single best refresh target if you only have time to fix one thing

## Why it matters

This report gives the repo a more realistic maintenance story:

- freshness says what is out of date
- regeneration says how to rebuild it
- impact says what it affects
- maintenance risk says what matters most
