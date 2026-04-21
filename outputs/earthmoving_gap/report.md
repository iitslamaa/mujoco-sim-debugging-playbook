# Earthmoving Sim-to-Field Gap Report

Scenarios: `2`
Mean calibration error: `0.3474`

## Scenario gaps

| scenario | calibration_error | dominant_gap | gap_error | recommended_action |
| --- | ---: | --- | ---: | --- |
| baseline_push | 0.4325 | terrain_profile_rmse | 0.5469 | Prioritize field measurement and calibration of `cohesion` because it strongly drives `terrain_profile_rmse`. |
| cohesive_soil | 0.2624 | terrain_profile_rmse | 0.4994 | Prioritize field measurement and calibration of `cohesion` because it strongly drives `terrain_profile_rmse`. |

## Top sensitivity signals

| soil_parameter | metric | correlation |
| --- | --- | ---: |
| blade_coupling | moved_volume | 0.9667 |
| cohesion | terrain_profile_rmse | 0.9408 |
| compaction_rate | terrain_profile_rmse | 0.8594 |
| spillover_rate | terrain_profile_rmse | -0.7478 |
| friction_angle_deg | terrain_profile_rmse | 0.7109 |