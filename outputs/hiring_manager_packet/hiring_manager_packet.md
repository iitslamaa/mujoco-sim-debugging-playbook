# Hiring Manager Packet

Autonomous earthmoving simulation validation packet

A MuJoCo-based construction autonomy simulation track that connects deformable-terrain experiments to calibration, release gating, jobsite productivity, and native-kernel performance.

## Manager Summary

- The earthmoving gate is `pass` across `3` scenarios, with deterministic generated artifacts for review.
- The jobsite scorecard converts sim outputs into a deployment decision: `needs_calibration_before_field_trial` with mean productivity `5.16` m3/hr.
- The current bottleneck is `cycle_productivity`, which creates a concrete next engineering loop instead of a vague demo.
- The sim-to-field gap report identifies `blade_coupling` as the top global calibration signal for `moved_volume`.
- The blade-plan search evaluates `45` candidates and selects `baseline_push_d0.008_w0.24_y+0.00` under the current score.
- The multi-pass evaluator compares `4` task sequences; best is `single_pass_wide_cut` at `7.65` m3/hr.
- The robustness sweep runs `36` uncertainty episodes for `single_pass_wide_cut` with pass rate `50%`.
- The field-trial case study traces `cohesive_soil` from replay metrics to root-cause hypotheses and the next experiment.
- The surrogate model reports mean MAE `0.000040`, showing how the generated dataset can support learned evaluators.
- The C++ terrain kernel benchmark shows `7.65x` speedup over Python for the terrain update workload.

## Architecture

- MuJoCo machine scene defines the blade/dozer kinematic path used for deterministic replay.
- A heightmap terrain layer applies blade passes with soil cohesion, friction, compaction, coupling, spillover, and volume accounting.
- Benchmark, scale, sensitivity, calibration, and gap-report stages turn raw runs into validation evidence.
- Jobsite evaluation translates physical metrics into cycle time, productivity, target capture, bottleneck, and rework risk.
- Dataset, surrogate, and plan-search stages connect the simulator to ML autonomy evaluation and planner tuning.
- Native-kernel smoke and benchmark paths show where hot terrain operations could move from Python to C++ or Rust.

## Evidence To Inspect

| area | artifact | why it matters |
| --- | --- | --- |
| Hiring overview | [Earthmoving role brief](../earthmoving_role_brief/role_brief.md) | Fastest proof that the project maps to autonomy simulation work. |
| Release evidence | [Earthmoving review packet](../earthmoving_review_packet/review_packet.md) | Rolls up scenario results, readiness signals, sensitivities, and sim-to-field gaps. |
| Deployment relevance | [Jobsite autonomy evaluation](../jobsite_autonomy_eval/report.md) | Shows cycle-time, productivity, placement, and bottleneck thinking. |
| Debug narrative | [Field trial case study](../field_trial_case_study/field_trial_case_study.md) | Connects one replay to observations, hypotheses, and a next experiment. |
| Visual review | [Field trial visuals](../field_trial_visuals/field_trial_visuals.md) | Shows terrain delta, blade path, and productivity bottleneck plots. |
| Calibration | [Sim-to-field gap report](../earthmoving_gap/report.md) | Demonstrates how field observations would drive the next simulation updates. |
| Autonomy loop | [Blade plan search](../earthmoving_plan_search/report.md) | Uses the simulator to evaluate candidate task parameters. |
| Task planning | [Multi-pass plan evaluation](../multipass_plan_eval/multipass_plan_eval.md) | Compares single-pass and multi-pass task sequences against productivity and placement gates. |
| Robustness | [Task plan robustness sweep](../task_plan_robustness/task_plan_robustness.md) | Stress-tests the selected task plan under soil and cycle-time uncertainty. |
| ML evaluation | [Surrogate evaluator](../earthmoving_surrogate/report.md) | Shows generated labels and learned evaluator scaffolding. |
| Performance | [Terrain kernel benchmark](../terrain_kernel_benchmark/report.md) | Shows native implementation and benchmark instinct for simulation hot paths. |

## Suggested Review Path

1. Start with the role brief for a two-minute overview.
2. Open the review packet to see the scenario table, readiness signals, and jobsite scorecard.
3. Open the jobsite autonomy evaluation to see how sim outputs become deployment decisions.
4. Open the field-trial case study to see one scenario traced from replay to next experiment.
5. Open the field-trial visuals to quickly inspect terrain delta, blade path, and productivity bottleneck.
6. Open the multi-pass plan evaluation to see whether changing task structure improves the bottleneck.
7. Open the task-plan robustness sweep to see uncertainty sensitivity around the selected candidate.
8. Open the gap report to see calibration priorities and limitations.
9. Skim the terrain kernel and benchmark if evaluating low-level implementation ability.

## Technical Judgment Signals

- The project does not claim production soil mechanics; it frames the heightmap model as a validation scaffold with explicit limitations.
- The scorecard chooses `needs_calibration_before_field_trial` rather than forcing a pass, because productivity is below the configured field-trial target.
- The review packet separates sim quality gates from jobsite readiness, avoiding one metric pretending to answer every deployment question.
- The largest gap is `terrain_profile_rmse`, and the report turns that into a concrete measurement request instead of a vague tuning note.
- The current top sensitivity is `blade_coupling` to `moved_volume`, which makes calibration inspectable.

## Limitations

- The terrain deformation is a lightweight heightmap approximation, not DEM/FEM soil mechanics.
- The field logs are synthetic placeholders used to exercise the calibration workflow.
- The machine profile uses proxy cycle-time parameters and should be replaced with real excavator/dozer telemetry.
- The planner is a grid search over single-pass blade parameters; multi-pass task planning is the natural next step.
- The native terrain kernel is benchmarked as a standalone path; deeper integration would require Python bindings and profiling inside the full evaluation loop.

## Next 30 Days With Real Machine Data

- Replace synthetic field logs with before/after terrain scans, machine pose, blade state, and cycle-time telemetry.
- Fit soil parameters per site condition and report confidence intervals across repeated passes.
- Extend plan search to multi-pass cut, carry, dump, and return sequences with productivity and target-placement objectives.
- Add scenario replay media that overlays blade trajectory, terrain delta, and target-zone capture for fast engineering review.
- Move the terrain update hot path behind a native binding and measure end-to-end throughput impact in batch evaluation.

## Short Note To Send

```text
Hi [Name], I built a focused autonomous earthmoving simulation packet that I think is relevant to Bedrock's Simulation role. It uses MuJoCo plus a heightmap terrain model to evaluate blade passes, soil calibration, randomized scale runs, sim-to-field gaps, jobsite productivity, and native terrain-kernel performance. The most manager-friendly entry point is `outputs/hiring_manager_packet/hiring_manager_packet.md`; the project is explicit about limitations and current bottlenecks rather than presenting it as a production soil solver. I would be grateful if you would be open to taking a look or pointing me toward the right engineering manager.
```