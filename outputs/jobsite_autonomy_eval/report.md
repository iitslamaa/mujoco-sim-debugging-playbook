# Jobsite Autonomy Evaluation

Deployment-style scorecard that turns terrain simulation outputs into cycle-time, productivity, placement, and rework-risk signals.

- Overall decision: `needs_calibration_before_field_trial`
- Release-candidate scenarios: `0` / `3`
- Mean scaled productivity: `5.16` m3/hr
- Mean target capture: `0.341`
- Top bottleneck: `cycle_productivity`

## Scenario Scorecard

| scenario | decision | productivity_m3_hr | cycle_time_s | target_capture | rework_risk | bottleneck |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| baseline_push | tune_before_field | 6.71 | 10.75 | 0.344 | 0.15 | cycle_productivity |
| cohesive_soil | tune_before_field | 5.25 | 10.75 | 0.357 | 0.15 | cycle_productivity |
| shallow_blade_slip | tune_before_field | 3.54 | 10.75 | 0.322 | 0.15 | cycle_productivity |

## Operator Notes

- baseline_push: tune before field work; primary bottleneck is cycle_productivity with failed checks productivity.
- cohesive_soil: tune before field work; primary bottleneck is cycle_productivity with failed checks productivity.
- shallow_blade_slip: tune before field work; primary bottleneck is cycle_productivity with failed checks productivity.