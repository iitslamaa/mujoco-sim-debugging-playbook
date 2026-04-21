# Earthmoving Benchmark

Construction-machine blade scenarios evaluated against terrain deformation, target berm, material displacement, conservation, and runtime metrics.

| scenario | moved_volume | target_zone_volume | deposit_progress_m | terrain_rmse | volume_error | runtime_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| shallow_blade_slip | 0.000587 | 0.000189 | 0.5029 | 0.010896 | 0.000000 | 0.0024 |
| baseline_push | 0.001113 | 0.000382 | 0.5147 | 0.011767 | 0.000000 | 0.0025 |
| cohesive_soil | 0.000871 | 0.000311 | 0.5120 | 0.014993 | 0.000000 | 0.0026 |

Best terrain-profile match: `shallow_blade_slip` with `0.010896` RMSE.
