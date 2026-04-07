# Refresh Checklist

- Bundles: `2`
- Total steps: `6`

## dashboard_refresh

- Validation target: `dashboard/data.json`
1. `python scripts/generate_dashboard.py` to refresh `dashboard/data.json` (0 downstream artifacts)

## support_report_refresh

- Validation target: `outputs/briefing_note/briefing_note.json`
1. `python scripts/generate_scenario_plan.py` to refresh `outputs/scenario_plan/scenario_plan.json` (3 downstream artifacts)
2. `python scripts/generate_support_readiness.py` to refresh `outputs/support_readiness/support_readiness.json` (3 downstream artifacts)
3. `python scripts/generate_ops_review.py` to refresh `outputs/ops_review/ops_review.json` (2 downstream artifacts)
4. `python scripts/generate_scorecard.py` to refresh `outputs/scorecard/scorecard.json` (2 downstream artifacts)
5. `python scripts/generate_briefing_note.py` to refresh `outputs/briefing_note/briefing_note.json` (1 downstream artifacts)
