# Support Capacity Plan

- Queue count: `11`
- Owners tracked: `1`
- Overloaded owners: `1`
- Lanes tracked: `1`
- Rebalance candidates: `5`
- Highest-pressure lane: `incident_backfill`

## Owner Pressure

| owner | status | effort_points | breaches | at_risk |
| --- | --- | ---: | ---: | ---: |
| controls-and-policy | overloaded | 22 | 2 | 3 |

## Lane Actions

| lane | pressure_shift | breaches | at_risk | action |
| --- | ---: | ---: | ---: | --- |
| incident_backfill | 7 | 2 | 3 | Reassign one blocking item immediately and split the lane across additional owners. |

## Rebalance Candidates

| status | target | current_owner | recommended_owner | effort_points | handoff_reason |
| --- | --- | --- | --- | ---: | --- |
| breach | low_damping_high_gain / expert_pd | controls-and-policy | simulation-debugging | 5 | Current owner has a breaching item and should offload work to keep the queue moving. |
| breach | low_damping_high_gain / hybrid_guardrail | controls-and-policy | simulation-debugging | 5 | Current owner has a breaching item and should offload work to keep the queue moving. |
| at_risk | delay_heavy / expert_pd | controls-and-policy | simulation-debugging | 4 | This item is at risk and benefits from parallel evidence gathering. |
| at_risk | noise_heavy / expert_pd | controls-and-policy | simulation-debugging | 4 | This item is at risk and benefits from parallel evidence gathering. |
| at_risk | noise_heavy / hybrid_guardrail | controls-and-policy | simulation-debugging | 4 | This item is at risk and benefits from parallel evidence gathering. |