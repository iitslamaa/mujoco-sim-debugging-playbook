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
make terrain-kernel-smoke
```

## What It Measures

- `moved_volume`: soil volume removed by the blade footprint
- `target_zone_volume`: material delivered into the desired berm region
- `terrain_profile_rmse`: final terrain error against the target terrain
- `volume_conservation_error`: conservation residual after compaction
- `runtime_s`: wall-clock runtime per scenario
- `episodes_per_second`: batch throughput for randomized scale studies
- `pearson_correlation`: sensitivity estimate between soil parameters and output metrics
- `calibration_error`: weighted relative error between simulated and observed field-log metrics

## Why It Exists

The reacher benchmark shows controller debugging and ML evaluation. The earthmoving benchmark adds the physical-world concerns that matter for autonomous construction machines:

- contact-heavy task content
- deformable terrain approximation
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
