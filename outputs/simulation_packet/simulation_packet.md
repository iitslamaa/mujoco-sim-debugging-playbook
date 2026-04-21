# Earthmoving Simulation Packet

Construction-machine simulation track with deformable terrain, calibration, scale, and debug artifacts.

Repo strategy: Keep this repo as the full engineering record, and link this packet as the recruiter-facing entry point.

## Why This Maps To The Role

- High-fidelity simulation content: MuJoCo dozer/blade scene plus terrain before/after artifacts.
- Physics and geometry reasoning: heightmap terrain deformation, soil parameters, volume accounting, and target-berm metrics.
- Sim-to-real workflow: calibration against observed field-log metrics and gap reports with next measurement priorities.
- Scale and evaluation: randomized batch studies, quality gates, deterministic replay, and throughput reporting.
- Deployment relevance: cycle-time, productivity, target-capture, bottleneck, and rework-risk scoring from simulation outputs.
- ML/autonomy support: feature/label dataset, surrogate evaluator, and simulator-in-the-loop blade plan search.
- Production instincts: C++ terrain kernel smoke path, tests, provenance manifests, generated reports, and review packets.

## Current Metrics

- Gate status: `pass`
- Earthmoving scenarios: `3`
- Randomized scale episodes: `60`
- Throughput: `287.91` episodes/s
- Dataset rows: `54`
- Surrogate mean MAE: `0.000040`
- Best blade-plan score: `0.012396`
- Jobsite decision: `needs_calibration_before_field_trial`
- Mean scaled productivity: `5.16` m3/hr
- Top jobsite bottleneck: `cycle_productivity`
- Best evaluated task plan: `single_pass_wide_cut`
- Best task-plan productivity: `7.65` m3/hr
- Best task-plan decision: `release_candidate`
- Task-plan robustness pass rate: `50%`
- Task-plan robustness P10 productivity: `6.45` m3/hr
- Top robustness driver: `soil.blade_coupling`
- Top failure mode: `under_excavation`
- C++ terrain-kernel speedup: `7.65x`
- Fastest native terrain kernel: `rust_ffi`
- Rust FFI terrain-kernel speedup: `5.76x`

## Best Review Links

- `hiring_manager_packet`: [outputs/hiring_manager_packet/hiring_manager_packet.md](outputs/hiring_manager_packet/hiring_manager_packet.md)
- `dashboard`: [outputs/earthmoving_dashboard/index.html](outputs/earthmoving_dashboard/index.html)
- `role_brief`: [outputs/earthmoving_role_brief/role_brief.md](outputs/earthmoving_role_brief/role_brief.md)
- `review_packet`: [outputs/earthmoving_review_packet/review_packet.md](outputs/earthmoving_review_packet/review_packet.md)
- `benchmark_report`: [outputs/earthmoving_benchmark/report.md](outputs/earthmoving_benchmark/report.md)
- `gap_report`: [outputs/earthmoving_gap/report.md](outputs/earthmoving_gap/report.md)
- `jobsite_eval`: [outputs/jobsite_autonomy_eval/report.md](outputs/jobsite_autonomy_eval/report.md)
- `field_trial_visuals`: [outputs/field_trial_visuals/field_trial_visuals.md](outputs/field_trial_visuals/field_trial_visuals.md)
- `field_trial_case_study`: [outputs/field_trial_case_study/field_trial_case_study.md](outputs/field_trial_case_study/field_trial_case_study.md)
- `multipass_plan_eval`: [outputs/multipass_plan_eval/multipass_plan_eval.md](outputs/multipass_plan_eval/multipass_plan_eval.md)
- `task_plan_robustness`: [outputs/task_plan_robustness/task_plan_robustness.md](outputs/task_plan_robustness/task_plan_robustness.md)
- `robustness_sensitivity`: [outputs/robustness_sensitivity/robustness_sensitivity.md](outputs/robustness_sensitivity/robustness_sensitivity.md)
- `surrogate_report`: [outputs/earthmoving_surrogate/report.md](outputs/earthmoving_surrogate/report.md)
- `plan_search_report`: [outputs/earthmoving_plan_search/report.md](outputs/earthmoving_plan_search/report.md)
- `kernel_benchmark`: [outputs/terrain_kernel_benchmark/report.md](outputs/terrain_kernel_benchmark/report.md)
- `native_kernel_matrix`: [outputs/native_kernel_matrix/report.md](outputs/native_kernel_matrix/report.md)
- `cxx_kernel`: [cpp/terrain_kernel.cpp](cpp/terrain_kernel.cpp)
- `rust_kernel_note`: [docs/rust-simulation-kernel-note.md](docs/rust-simulation-kernel-note.md)

## Interview Talk Track

- I started with a MuJoCo support/debugging project, then added an earthmoving simulation track specifically for autonomous construction.
- The strongest sensitivity signal is `blade_coupling` driving `moved_volume`, which gives a concrete calibration target.
- The batch evaluator currently runs `60` randomized earthmoving episodes at `287.91` episodes/s.
- The surrogate evaluator predicts `moved_volume` and related metrics from soil/blade features, with mean MAE `0.000040`.
- The planner selected `baseline_push_d0.008_w0.24_y+0.00` as the best blade candidate under the current score function.
- The jobsite scorecard translates sim outputs into cycle-time, productivity, target-capture, and rework-risk signals; the current decision is `needs_calibration_before_field_trial`, mainly because `cycle_productivity` is below target.
- The C++ terrain kernel matches the Python terrain output and runs `7.65x` faster in its benchmark.
- The native kernel matrix currently reports `rust_ffi` as the fastest available terrain kernel.
- The Rust FFI terrain kernel shows how this workload can move toward memory-safe native kernels called from Python simulation tooling.
- The failure queue surfaces `under_excavation` as the top debug theme, with next actions attached.

## Limitations I Would State Clearly

- The terrain model is an intentionally lightweight heightmap approximation, not a production soil mechanics solver.
- Field logs are synthetic placeholders for demonstrating calibration workflow and should be replaced with real machine/site data.
- The jobsite productivity model uses proxy cycle-time assumptions until real machine telemetry is available.
- The C++ path is currently a standalone kernel smoke path; a stronger next step is binding it into the Python benchmark and profiling it against the Python update.

## Next Technical Steps

- Bind the C++ terrain kernel into the Python simulator and benchmark speedup.
- Expand task-plan evaluation into robustness sweeps across soil, blade-width, cut-depth, and cycle-time uncertainty.
- Add real or richer synthetic field traces with terrain-profile observations before and after earthmoving passes.
- Expand the blade planner from grid search to constrained optimization over multi-pass trajectories.
- Add visual replay/video generation for the dashboard so reviewers can inspect motion and terrain evolution quickly.