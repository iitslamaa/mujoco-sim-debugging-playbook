# Earthmoving Sim-to-Field Gap Report

Scenarios: `2`
Mean calibration error: `0.4378`

## Scenario gaps

| scenario | calibration_error | dominant_gap | gap_error | recommended_action |
| --- | ---: | --- | ---: | --- |
| baseline_push | 0.4419 | target_zone_volume | 1.0000 | Improve delivered-material measurement around the target berm region. |
| cohesive_soil | 0.4338 | target_zone_volume | 1.0000 | Improve delivered-material measurement around the target berm region. |

## Top sensitivity signals

| soil_parameter | metric | correlation |
| --- | --- | ---: |
| blade_coupling | moved_volume | 0.9453 |
| cohesion | terrain_profile_rmse | 0.9287 |
| compaction_rate | terrain_profile_rmse | 0.9002 |
| spillover_rate | terrain_profile_rmse | -0.8478 |
| friction_angle_deg | terrain_profile_rmse | 0.7353 |