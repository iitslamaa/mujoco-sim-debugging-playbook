# Multi-Pass Plan Evaluation

Scenario: `cohesive_soil`
Best candidate: `single_pass_wide_cut`
Best decision: `release_candidate`
Best productivity: `7.65` m3/hr

## Candidate Comparison

| candidate | decision | passes | productivity_m3_hr | cycle_time_s | moved_volume | target_capture | terrain_rmse | score |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| single_pass_wide_cut | release_candidate | 1 | 7.65 | 10.75 | 0.001270 | 0.350 | 0.013881 | 1.530 |
| single_pass_baseline | tune_before_field | 1 | 5.25 | 10.75 | 0.000871 | 0.357 | 0.014993 | 1.218 |
| two_pass_deeper_finish | tune_before_field | 2 | 4.18 | 21.50 | 0.001386 | 0.351 | 0.013448 | 1.071 |
| two_pass_offset_cleanup | tune_before_field | 2 | 4.11 | 21.50 | 0.001365 | 0.346 | 0.013675 | 1.053 |

## Recommendation

Promote `single_pass_wide_cut` to replay and robustness testing: it clears the configured 7.50 m3/hr productivity target and the placement gates.