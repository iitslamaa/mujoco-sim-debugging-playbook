# Field Trial Case Study: cohesive_soil

Decision: `tune_before_field`

## Executive Readout

- The scenario is marked `tune_before_field` because `cycle_productivity` is the current deployment bottleneck.
- Simulated productivity is `5.25` m3/hr with cycle time `10.75` s.
- Target capture is `0.357`, while terrain RMSE is `0.014993`.
- The dominant sim-to-field gap is `terrain_profile_rmse`; recommended action: Prioritize field measurement and calibration of `cohesion` because it strongly drives `terrain_profile_rmse`.
- The current blade-plan search suggests `baseline_push_d0.008_w0.24_y+0.00` as the best single-pass candidate.

## Observations

- Soil settings use cohesion `0.42`, friction angle `36.0` deg, and blade coupling `0.72`.
- Moved volume is `0.000871` with deposit forward progress `0.5120` m.
- Volume conservation error is `0.000000`, so the immediate concern is not volume accounting.
- Rework risk is `0.15` and target-zone volume is `0.000311`.

## Root-Cause Hypotheses

- Cohesive soil scenario: expect reduced cutting efficiency and stronger calibration dependence.
- `cycle_productivity` is likely a task-design issue: one pass is too conservative for the configured productivity target.
- `terrain_profile_rmse` should be checked against richer before/after terrain measurements before changing model structure.

## Multi-Pass Evaluation

- Best evaluated sequence: `single_pass_wide_cut`
- Decision: `release_candidate`
- Productivity: `7.65` m3/hr
- Target capture: `0.350`
- Terrain RMSE: `0.013881`

## Next Experiment

- Run `single_pass_wide_cut` as a replay bundle and compare it against the current scenario baseline.
- Use `single_pass_wide_cut` as the evaluated task-plan baseline and replay it with robustness sweeps.
- Collect or synthesize richer observations for `terrain_profile_rmse` and rerun calibration.
- Promote the experiment only if productivity improves without increasing terrain RMSE or volume residuals beyond gate thresholds.

## Visual Review

![Terrain delta and blade path](../field_trial_visuals/cohesive_soil_terrain_delta.png)

![Jobsite productivity bottleneck](../field_trial_visuals/jobsite_productivity_bottleneck.png)

## Acceptance Criteria

- Productivity at or above `7.50` m3/hr.
- Target capture ratio at or above `0.22`.
- Terrain RMSE at or below `0.075`.
- Volume conservation error at or below `0.003`.
- Deposit forward progress at or above `0.20` m.

## Review Links

- `multipass_plan_eval`: [../multipass_plan_eval/multipass_plan_eval.md](../multipass_plan_eval/multipass_plan_eval.md)
- `field_trial_visuals`: [../field_trial_visuals/field_trial_visuals.md](../field_trial_visuals/field_trial_visuals.md)
- `jobsite_eval`: [../jobsite_autonomy_eval/report.md](../jobsite_autonomy_eval/report.md)
- `review_packet`: [../earthmoving_review_packet/review_packet.md](../earthmoving_review_packet/review_packet.md)
- `replay_bundle`: [../earthmoving_replay/cohesive_soil_replay.md](../earthmoving_replay/cohesive_soil_replay.md)
- `gap_report`: [../earthmoving_gap/report.md](../earthmoving_gap/report.md)
- `plan_search`: [../earthmoving_plan_search/report.md](../earthmoving_plan_search/report.md)