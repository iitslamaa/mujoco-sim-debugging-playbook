# Earthmoving Sensitivity

Episodes: `72`
Mean moved volume: `0.001123`
Mean terrain RMSE: `0.014111`

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
| friction_angle_deg | moved_volume | 0.1371 |
| blade_coupling | runtime_s | 0.1027 |