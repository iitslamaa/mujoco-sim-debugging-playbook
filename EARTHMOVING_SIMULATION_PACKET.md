# Earthmoving Simulation Packet

Construction-machine simulation track with deformable terrain, calibration, scale, and debug artifacts.

Repo strategy: Keep this repo as the full engineering record, and link this packet as the recruiter-facing entry point.

## Why This Maps To The Role

- High-fidelity simulation content: MuJoCo dozer/blade scene plus terrain before/after artifacts.
- Physics and geometry reasoning: heightmap terrain deformation, soil parameters, volume accounting, and target-berm metrics.
- Sim-to-real workflow: calibration against observed field-log metrics and gap reports with next measurement priorities.
- Scale and evaluation: randomized batch studies, quality gates, deterministic replay, and throughput reporting.
- ML/autonomy support: feature/label dataset, surrogate evaluator, and simulator-in-the-loop blade plan search.
- Production instincts: C++ terrain kernel smoke path, tests, provenance manifests, generated reports, and review packets.

## Current Metrics

- Gate status: `pass`
- Earthmoving scenarios: `3`
- Randomized scale episodes: `60`
- Throughput: `323.79` episodes/s
- Dataset rows: `54`
- Surrogate mean MAE: `0.000040`
- Best blade-plan score: `0.012396`
- Top failure mode: `under_excavation`
- C++ terrain-kernel speedup: `7.65x`

## Best Review Links

- `dashboard`: [outputs/earthmoving_dashboard/index.html](outputs/earthmoving_dashboard/index.html)
- `role_brief`: [outputs/earthmoving_role_brief/role_brief.md](outputs/earthmoving_role_brief/role_brief.md)
- `review_packet`: [outputs/earthmoving_review_packet/review_packet.md](outputs/earthmoving_review_packet/review_packet.md)
- `benchmark_report`: [outputs/earthmoving_benchmark/report.md](outputs/earthmoving_benchmark/report.md)
- `gap_report`: [outputs/earthmoving_gap/report.md](outputs/earthmoving_gap/report.md)
- `surrogate_report`: [outputs/earthmoving_surrogate/report.md](outputs/earthmoving_surrogate/report.md)
- `plan_search_report`: [outputs/earthmoving_plan_search/report.md](outputs/earthmoving_plan_search/report.md)
- `kernel_benchmark`: [outputs/terrain_kernel_benchmark/report.md](outputs/terrain_kernel_benchmark/report.md)
- `cxx_kernel`: [cpp/terrain_kernel.cpp](cpp/terrain_kernel.cpp)

## Interview Talk Track

- I started with a MuJoCo support/debugging project, then added an earthmoving simulation track specifically for autonomous construction.
- The strongest sensitivity signal is `blade_coupling` driving `moved_volume`, which gives a concrete calibration target.
- The batch evaluator currently runs `60` randomized earthmoving episodes at `323.79` episodes/s.
- The surrogate evaluator predicts `moved_volume` and related metrics from soil/blade features, with mean MAE `0.000040`.
- The planner selected `baseline_push_d0.008_w0.24_y+0.00` as the best blade candidate under the current score function.
- The C++ terrain kernel matches the Python terrain output and runs `7.65x` faster in the current benchmark.
- The failure queue surfaces `under_excavation` as the top debug theme, with next actions attached.

## Limitations I Would State Clearly

- The terrain model is an intentionally lightweight heightmap approximation, not a production soil mechanics solver.
- Field logs are synthetic placeholders for demonstrating calibration workflow and should be replaced with real machine/site data.
- The C++ path is currently a standalone kernel smoke path; a stronger next step is binding it into the Python benchmark and profiling it against the Python update.

## Next Technical Steps

- Bind the C++ terrain kernel into the Python simulator and benchmark speedup.
- Add real or richer synthetic field traces with terrain-profile observations before and after earthmoving passes.
- Expand the blade planner from grid search to constrained optimization over multi-pass trajectories.
- Add visual replay/video generation for the dashboard so reviewers can inspect motion and terrain evolution quickly.