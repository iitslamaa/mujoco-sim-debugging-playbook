# Earthmoving Benchmark Guide

This project track demonstrates construction-style robotics simulation work: a MuJoCo dozer/blade asset, a terrain deformation model, soil parameter calibration, and batch evaluation for scale.

## Commands

```bash
make earthmoving-benchmark
make earthmoving-calibration
make earthmoving-scale
make earthmoving-sensitivity
make earthmoving-gate
make earthmoving-gap
make earthmoving-review-packet
make earthmoving-replay
make earthmoving-dashboard
make earthmoving-dataset
make earthmoving-surrogate
make earthmoving-plan-search
make earthmoving-failure-modes
make earthmoving-role-brief
make jobsite-autonomy-eval
make multipass-plan-eval
make task-plan-robustness
make robustness-sensitivity
make field-trial-visuals
make field-trial-case-study
make hiring-manager-packet
make application-packet
make application-bundle
make application-readiness
make application-stack
make interview-assets
make terrain-kernel-smoke
```

## What It Measures

- `moved_volume`: soil volume removed by the blade footprint
- `target_zone_volume`: material delivered into the desired berm region
- `deposit_forward_progress`: centroid displacement from cut material to deposited material
- `terrain_profile_rmse`: final terrain error against the target terrain
- `volume_conservation_error`: conservation residual after compaction
- `runtime_s`: wall-clock runtime per scenario
- `episodes_per_second`: batch throughput for randomized scale studies
- `cycle_time_s`: estimated cut, return, turnaround, and dump-settle time for a blade cycle
- `productivity_m3_per_hr`: scaled volume moved per estimated operating hour
- `target_capture_ratio`: share of moved material deposited inside the target zone
- `rework_risk_score`: composite placement, profile-error, and volume-accounting risk signal
- `pearson_correlation`: sensitivity estimate between soil parameters and output metrics
- `calibration_error`: weighted relative error between simulated and observed field-log metrics

## Why It Exists

The reacher benchmark shows controller debugging and ML evaluation. The earthmoving benchmark adds the physical-world concerns that matter for autonomous construction machines:

- contact-heavy task content
- deformable terrain approximation
- carried-load blade transport, where excavated material spills gradually and dumps near the pass endpoint
- soil parameter uncertainty
- sim-to-field calibration
- deterministic replay
- batch evaluation for many scenario variants
- a C++ terrain kernel smoke path for lower-level implementation practice
- release-style quality gates for realism and throughput thresholds
- gap reports that turn sensitivity and calibration outputs into next measurement priorities
- review packets that summarize readiness, scale, calibration, and scenario results
- replay bundles that capture one scenario's metrics, terrain stats, blade path, and debug hypotheses
- a static dashboard for quick portfolio review
- ML-ready datasets for surrogate modeling or learned evaluator experiments
- a deterministic surrogate evaluator over randomized terrain outcomes
- simulator-in-the-loop blade plan search for simple autonomy/content generation loops
- jobsite autonomy scoring that maps sim results to cycle productivity, placement, bottlenecks, and field-trial readiness
- failure-mode reports that turn metrics into ranked debug actions
- a role brief that summarizes the work for autonomy simulation hiring loops

## Artifact Map

- Benchmark summary: `outputs/earthmoving_benchmark/earthmoving_summary.json`
- Benchmark report: `outputs/earthmoving_benchmark/report.md`
- Calibration summary: `outputs/earthmoving_calibration/calibration_summary.json`
- Calibration report: `outputs/earthmoving_calibration/report.md`
- Scale summary: `outputs/earthmoving_scale/scale_summary.json`
- Scale report: `outputs/earthmoving_scale/report.md`
- Sensitivity summary: `outputs/earthmoving_sensitivity/sensitivity_summary.json`
- Sensitivity report: `outputs/earthmoving_sensitivity/report.md`
- Quality gate: `outputs/earthmoving_gate/earthmoving_gate.md`
- Gap report: `outputs/earthmoving_gap/report.md`
- Review packet: `outputs/earthmoving_review_packet/review_packet.md`
- Replay bundle: `outputs/earthmoving_replay/cohesive_soil_replay.md`
- Dashboard: `outputs/earthmoving_dashboard/index.html`
- Dataset report: `outputs/earthmoving_dataset/report.md`
- Surrogate report: `outputs/earthmoving_surrogate/report.md`
- Plan search report: `outputs/earthmoving_plan_search/report.md`
- Failure modes: `outputs/earthmoving_failure_modes/report.md`
- Role brief: `outputs/earthmoving_role_brief/role_brief.md`
- Jobsite autonomy evaluation: `outputs/jobsite_autonomy_eval/report.md`
- Field trial visuals: `outputs/field_trial_visuals/field_trial_visuals.md`
- Field trial case study: `outputs/field_trial_case_study/field_trial_case_study.md`
- Multi-pass plan evaluation: `outputs/multipass_plan_eval/multipass_plan_eval.md`
- Task plan robustness sweep: `outputs/task_plan_robustness/task_plan_robustness.md`
- Robustness sensitivity: `outputs/robustness_sensitivity/robustness_sensitivity.md`
- Hiring manager packet: `outputs/hiring_manager_packet/hiring_manager_packet.md`
- Application packet: `outputs/application_packet/application_packet.md`
- Application bundle: `outputs/application_bundle/application_bundle.md`
- Application readiness: `outputs/application_readiness/application_readiness.md`
- Interview assets: `outputs/interview_assets/interview_assets.md`
