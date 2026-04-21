# Earthmoving Benchmark

Construction-machine blade scenarios evaluated against terrain deformation, target berm, material displacement, conservation, and runtime metrics.

| scenario | moved_volume | target_zone_volume | deposit_progress_m | terrain_rmse | volume_error | runtime_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| shallow_blade_slip | 0.000687 | 0.000000 | 0.0622 | 0.011930 | 0.000000 | 0.0026 |
| baseline_push | 0.001599 | 0.000000 | 0.0690 | 0.013620 | 0.000000 | 0.0024 |
| cohesive_soil | 0.001111 | 0.000000 | 0.0673 | 0.016632 | 0.000000 | 0.0025 |

Best terrain-profile match: `shallow_blade_slip` with `0.011930` RMSE.
