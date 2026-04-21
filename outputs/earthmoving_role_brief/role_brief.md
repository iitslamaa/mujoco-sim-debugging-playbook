# Earthmoving Simulation Role Brief

Construction-machine simulation track with deformable terrain, calibration, scale, and debug artifacts.

## Fit Signals

- Built a MuJoCo dozer/blade task instead of only toy robot control.
- Implemented heightmap terrain deformation with soil parameters and volume accounting.
- Added sim-to-field calibration against observed construction-style logs.
- Generated randomized scale runs and throughput metrics for batch evaluation.
- Created ML-ready feature/label datasets for learned evaluators or surrogate models.
- Added C++ terrain-kernel smoke coverage for low-level geometry/physics implementation.
- Packaged failure replay, quality gates, dashboards, and review packets like production simulation infrastructure.

## Metrics

- Gate status: `pass`
- Scenarios: `3`
- Scale episodes: `60`
- Throughput: `323.79` episodes/s
- Dataset rows: `54`
- Failure-mode items: `2`
- Mean calibration error: `0.4378`

## Talking Points

- The current earthmoving gate is `pass`, so the track has release-style pass/fail semantics.
- The scale harness ran `60` randomized episodes at `323.79` episodes/s.
- The generated dataset has `54` rows with `10` features and `4` labels.
- The failure-mode queue currently prioritizes `under_excavation` as the highest-ranked debugging theme.