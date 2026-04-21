# Earthmoving Review Packet

- Gate status: `pass`
- Scenarios: `3`
- Scale episodes: `60`
- Throughput: `287.91` episodes/s
- Best scenario: `shallow_blade_slip`
- Hardest scenario: `cohesive_soil`
- Mean deposit progress: `0.510` m
- Mean calibration error: `0.3474`

## Readiness Signals

| signal | value | detail |
| --- | --- | --- |
| Quality gate | pass | Earthmoving realism and throughput thresholds |
| Scale throughput | 287.91 episodes/s | Randomized batch evaluation speed |
| Best terrain match | shallow_blade_slip | RMSE 0.01090 |
| Mean deposit progress | 0.510 m | Centroid displacement from cut region to deposit region |
| Largest sim-to-field gap | baseline_push | Prioritize field measurement and calibration of `cohesion` because it strongly drives `terrain_profile_rmse`. |

## Scenario Results

| scenario | moved_volume | deposit_progress_m | terrain_rmse | volume_error | runtime_s |
| --- | ---: | ---: | ---: | ---: | ---: |
| shallow_blade_slip | 0.000587 | 0.5029 | 0.010896 | 0.000000 | 0.00236 |
| baseline_push | 0.001113 | 0.5147 | 0.011767 | 0.000000 | 0.00246 |
| cohesive_soil | 0.000871 | 0.5120 | 0.014993 | 0.000000 | 0.00255 |

## Top Sensitivities

| soil_parameter | metric | correlation |
| --- | --- | ---: |
| blade_coupling | moved_volume | 0.9667 |
| cohesion | terrain_profile_rmse | 0.9408 |
| compaction_rate | terrain_profile_rmse | 0.8594 |
| spillover_rate | terrain_profile_rmse | -0.7478 |
| friction_angle_deg | terrain_profile_rmse | 0.7109 |
| spillover_rate | moved_volume | -0.4914 |
| compaction_rate | moved_volume | 0.2805 |
| cohesion | runtime_s | -0.2298 |

## Sim-to-Field Gap Actions

| scenario | dominant_gap | recommendation |
| --- | --- | --- |
| baseline_push | terrain_profile_rmse | Prioritize field measurement and calibration of `cohesion` because it strongly drives `terrain_profile_rmse`. |
| cohesive_soil | terrain_profile_rmse | Prioritize field measurement and calibration of `cohesion` because it strongly drives `terrain_profile_rmse`. |