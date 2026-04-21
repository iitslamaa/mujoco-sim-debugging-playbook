# Earthmoving Benchmark Guide

This project track demonstrates construction-style robotics simulation work: a MuJoCo dozer/blade asset, a terrain deformation model, soil parameter calibration, and batch evaluation for scale.

## Commands

```bash
make earthmoving-benchmark
make earthmoving-calibration
make earthmoving-scale
make terrain-kernel-smoke
```

## What It Measures

- `moved_volume`: soil volume removed by the blade footprint
- `target_zone_volume`: material delivered into the desired berm region
- `terrain_profile_rmse`: final terrain error against the target terrain
- `volume_conservation_error`: conservation residual after compaction
- `runtime_s`: wall-clock runtime per scenario
- `episodes_per_second`: batch throughput for randomized scale studies

## Why It Exists

The reacher benchmark shows controller debugging and ML evaluation. The earthmoving benchmark adds the physical-world concerns that matter for autonomous construction machines:

- contact-heavy task content
- deformable terrain approximation
- soil parameter uncertainty
- sim-to-field calibration
- deterministic replay
- batch evaluation for many scenario variants
- a C++ terrain kernel smoke path for lower-level implementation practice

## Artifact Map

- Benchmark summary: `outputs/earthmoving_benchmark/earthmoving_summary.json`
- Benchmark report: `outputs/earthmoving_benchmark/report.md`
- Calibration summary: `outputs/earthmoving_calibration/calibration_summary.json`
- Calibration report: `outputs/earthmoving_calibration/report.md`
- Scale summary: `outputs/earthmoving_scale/scale_summary.json`
- Scale report: `outputs/earthmoving_scale/report.md`
