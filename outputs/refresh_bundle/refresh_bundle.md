# Refresh Bundles

- Bundles: `2`
- Actions: `6`

| bundle | action_count | high_priority_count | max_impact_count |
| --- | ---: | ---: | ---: |
| dashboard_refresh | 1 | 1 | 0 |
| support_report_refresh | 5 | 0 | 3 |

## Bundle Actions

- `dashboard_refresh`: dashboard/data.json via `python scripts/generate_dashboard.py`
- `support_report_refresh`: outputs/ops_review/ops_review.json via `python scripts/generate_ops_review.py`
- `support_report_refresh`: outputs/support_readiness/support_readiness.json via `python scripts/generate_support_readiness.py`
- `support_report_refresh`: outputs/scenario_plan/scenario_plan.json via `python scripts/generate_scenario_plan.py`
- `support_report_refresh`: outputs/scorecard/scorecard.json via `python scripts/generate_scorecard.py`
- `support_report_refresh`: outputs/briefing_note/briefing_note.json via `python scripts/generate_briefing_note.py`