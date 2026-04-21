# Earthmoving Review Packet

- Gate status: `pass`
- Scenarios: `3`
- Scale episodes: `60`
- Throughput: `323.79` episodes/s
- Best scenario: `shallow_blade_slip`
- Hardest scenario: `cohesive_soil`
- Mean calibration error: `0.4378`

## Readiness Signals

| signal | value | detail |
| --- | --- | --- |
| Quality gate | pass | Earthmoving realism and throughput thresholds |
| Scale throughput | 323.79 episodes/s | Randomized batch evaluation speed |
| Best terrain match | shallow_blade_slip | RMSE 0.01193 |
| Largest sim-to-field gap | baseline_push | Improve delivered-material measurement around the target berm region. |

## Scenario Results

| scenario | moved_volume | terrain_rmse | volume_error | runtime_s |
| --- | ---: | ---: | ---: | ---: |
| shallow_blade_slip | 0.000687 | 0.011930 | 0.000000 | 0.00257 |
| baseline_push | 0.001599 | 0.013620 | 0.000000 | 0.00527 |
| cohesive_soil | 0.001111 | 0.016632 | 0.000000 | 0.00247 |

## Top Sensitivities

| soil_parameter | metric | correlation |
| --- | --- | ---: |
| blade_coupling | moved_volume | 0.9453 |
| cohesion | terrain_profile_rmse | 0.9287 |
| compaction_rate | terrain_profile_rmse | 0.9002 |
| spillover_rate | terrain_profile_rmse | -0.8478 |
| friction_angle_deg | terrain_profile_rmse | 0.7353 |
| spillover_rate | moved_volume | -0.4573 |
| blade_coupling | terrain_profile_rmse | 0.3426 |
| compaction_rate | moved_volume | 0.2192 |

## Sim-to-Field Gap Actions

| scenario | dominant_gap | recommendation |
| --- | --- | --- |
| baseline_push | target_zone_volume | Improve delivered-material measurement around the target berm region. |
| cohesive_soil | target_zone_volume | Improve delivered-material measurement around the target berm region. |