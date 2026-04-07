# Case Study Guide

This repository can generate higher-level technical narratives from the raw experiment outputs.

## Why this exists

Simulation projects often accumulate plots, JSON files, and trace dumps without ever turning them into a coherent story. This layer exists to synthesize those artifacts into reusable writeups.

## Command

```bash
python scripts/generate_case_studies.py
```

## Outputs

- `outputs/case_studies/controller_robustness_story.md`
- `outputs/case_studies/controller_robustness_story.png`

## What gets summarized

- benchmark winners across curated stress scenarios
- domain-randomization robustness trends
- high-level interpretation of where expert, learned, and hybrid control each help

