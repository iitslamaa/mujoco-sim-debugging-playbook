# Support Ops Review

- Queue count: `11`
- Incident coverage: `45.5%`
- Knowledge base coverage: `45.5%`
- Breaches: `2`
- At risk: `3`
- Highest-pressure lane: `incident_backfill`
- Overloaded owner: `controls-and-policy`
- Top gap: `low_damping_high_gain / expert_pd`

## Wins

- Knowledge base coverage is 45.5% of the open queue.
- The triage system has 5 incident bundles and 5 knowledge-base entries ready for reuse.
- Regression gate status remains `pass` across the latest release range.

## Risks

- 2 items are already in breach and 3 more are at risk.
- The highest-pressure lane is `incident_backfill` and the most overloaded owner is `controls-and-policy`.
- The top uncovered support gap is `low_damping_high_gain / expert_pd`.
- The riskiest benchmark scenario remains `low_damping_high_gain / expert_pd` with risk score `0.366`.

## Next Actions

| target | owner | action | reason |
| --- | --- | --- | --- |
| low_damping_high_gain / expert_pd | simulation-debugging | Increase joint damping and reduce actuator gain before changing controller structure. | Current owner has a breaching item and should offload work to keep the queue moving. |
| low_damping_high_gain / hybrid_guardrail | simulation-debugging | Increase joint damping and reduce actuator gain before changing controller structure. | Current owner has a breaching item and should offload work to keep the queue moving. |
| delay_heavy / expert_pd | simulation-debugging | Increase control frequency or use a more delay-tolerant guarded policy blend. | This item is at risk and benefits from parallel evidence gathering. |