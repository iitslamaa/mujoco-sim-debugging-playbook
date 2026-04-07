# Dashboard Snapshot Drift

- Transitions: `3`
- First pass snapshot: `full_refresh_projection`
- Largest failure drop: `current_state -> support_sprint_projection` (`4`)
- Largest risk drop: `support_sprint_projection -> full_refresh_projection` (`1.358`)

| from | to | status | failure_delta | risk_delta | baseline_success_rate_delta |
| --- | --- | --- | ---: | ---: | ---: |
| baseline_backlog | current_state | fail -> fail | -1 | -0.149 | 0.000 |
| current_state | support_sprint_projection | fail -> fail | -4 | -0.193 | 0.000 |
| support_sprint_projection | full_refresh_projection | fail -> pass | -1 | -1.358 | 0.000 |