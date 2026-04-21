# Earthmoving Sensitivity

Episodes: `72`
Mean moved volume: `0.000838`
Mean terrain RMSE: `0.012629`

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
| friction_angle_deg | moved_volume | 0.1904 |
| blade_coupling | runtime_s | 0.1891 |