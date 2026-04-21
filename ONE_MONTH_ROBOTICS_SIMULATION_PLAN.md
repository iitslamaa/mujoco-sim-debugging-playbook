# One-Month Robotics Simulation Plan

Goal: use this repository as a full-time, four-week simulation apprenticeship. By the end, the project should demonstrate useful robotics simulation skill, not just interview preparation.

The north star is: build, measure, debug, calibrate, optimize, and explain an earthmoving simulator like someone who can contribute to an autonomy simulation team.

## What This Plan Trains

- physics and geometry reasoning for terrain/contact simulation
- MuJoCo simulation content and scenario design
- sim-to-real calibration and validation thinking
- batch evaluation, regression gates, deterministic replay, and failure triage
- Python tooling for experiments and reports
- C++ and Rust native kernel paths for performance-sensitive terrain updates
- ML/autonomy support through datasets, surrogate evaluators, and planning search
- crisp technical communication for robotics/simulation engineers

## Weekly Outcomes

| week | theme | by Friday you should have |
| --- | --- | --- |
| 1 | Physics content and measurement | a clear mental model of the terrain update, metrics, failure modes, and MuJoCo scene |
| 2 | Performance and native kernels | profiled Python/C++/Rust terrain kernels and explained their tradeoffs |
| 3 | Calibration and sim-to-real | a stronger field-log workflow with parameter fitting and gap analysis |
| 4 | Autonomy evaluation and polish | a final review packet, dashboard, demo, and confident interview talk track |

## Week 1: Understand And Tighten The Simulator

### Day 1: Repo Orientation

Run:

```bash
make test
make earthmoving-benchmark
make earthmoving-review-packet
make simulation-packet
```

Read:

- `EARTHMOVING_SIMULATION_PACKET.md`
- `docs/earthmoving-benchmark-guide.md`
- `src/mujoco_sim_debugging_playbook/terrain.py`
- `src/mujoco_sim_debugging_playbook/earthmoving.py`

Be able to explain:

- what state the terrain grid stores
- how the blade removes and deposits material
- which parts are real physics versus heuristic approximation
- why volume conservation matters

### Day 2: Metric Audit

Deliverable:

- add or refine one metric that catches an unrealistic behavior
- add a test for it

Candidate metrics:

- peak terrain height
- cut-zone depletion
- deposit centroid
- volume outside target corridor
- blade path coverage

Be able to explain:

- why the metric matters for construction autonomy
- what failure it would catch in CI

### Day 3: Scenario Audit

Deliverable:

- add one new scenario to `configs/earthmoving_benchmark.json`
- regenerate benchmark and review packet

Candidate scenario:

- off-center pile
- deeper blade cut
- high-spillover dry soil
- high-cohesion sticky soil
- narrow target corridor

Be able to explain:

- what real-world condition the scenario approximates
- why an autonomy stack would need to test it

### Day 4: Replay And Debug

Run:

```bash
make earthmoving-replay
make earthmoving-failure-modes
```

Deliverable:

- improve one replay hypothesis or failure-mode rule

Be able to explain:

- how deterministic replay helps robotics teams debug field issues
- what you would attach to an engineer handoff

### Day 5: Week 1 Review

Deliverable:

- update `EARTHMOVING_SIMULATION_PACKET.md`
- write a short note in `OUTREACH_NOTE.md` if the project story changed

Checkpoint:

- explain the simulator in five minutes without reading code
- name three limitations honestly
- name three next data sources that would improve realism

## Week 2: Performance And Native Kernels

### Day 6: Python Profiling

Run:

```bash
make terrain-kernel-benchmark
make native-kernel-matrix
```

Deliverable:

- identify the hottest terrain operation
- document one optimization hypothesis

Be able to explain:

- why Python is useful for orchestration but weak for tight kernels
- what data layout choices matter for terrain grids

### Day 7: C++ Kernel Deep Dive

Read:

- `cpp/terrain_kernel.cpp`
- `src/mujoco_sim_debugging_playbook/terrain_kernel_benchmark.py`

Deliverable:

- add one C++ edge-case test or benchmark check

Be able to explain:

- memory layout of the height grid
- where allocations happen
- why the C++ result matches Python

### Day 8: Rust FFI Deep Dive

Read:

- `rust/terrain_kernel.rs`
- `rust/terrain_kernel_ffi.rs`
- `docs/rust-simulation-kernel-note.md`

Run:

```bash
make rust-terrain-kernel-smoke
make rust-terrain-kernel-benchmark
make native-kernel-matrix
```

Deliverable:

- add one safety or error-handling improvement to the Rust FFI path

Be able to explain:

- why Rust is useful for safe native simulation infrastructure
- what the FFI boundary does
- why Python still remains valuable

### Day 9: Kernel Comparison

Deliverable:

- improve `outputs/native_kernel_matrix/report.md` or its generator so the report is more decision-useful

Be able to explain:

- when you would choose Python, C++, or Rust
- why benchmark results can vary run to run
- what would be needed for a fair production benchmark

### Day 10: Week 2 Review

Checkpoint:

- explain the performance architecture in five minutes
- show the native kernel matrix
- explain exactly what Rust adds here without buzzwords

## Week 3: Calibration And Sim-To-Real

### Day 11: Field Log Schema

Read:

- `configs/earthmoving_field_logs.json`
- `src/mujoco_sim_debugging_playbook/earthmoving_calibration.py`

Deliverable:

- add a richer field-log schema field, such as profile samples, cut depth, or measured final berm centroid

Be able to explain:

- what real machine/site data you would ask for
- how it would reduce uncertainty

### Day 12: Parameter Fitting

Deliverable:

- improve calibration search beyond the current small grid

Candidate improvements:

- two-stage coarse-to-fine search
- weighted metrics per scenario
- uncertainty range around best parameters

Be able to explain:

- what parameter identification means
- how to avoid overfitting synthetic logs

### Day 13: Sensitivity Analysis

Run:

```bash
make earthmoving-sensitivity
make earthmoving-gap
```

Deliverable:

- improve gap recommendations using sensitivity results

Be able to explain:

- why sensitivity analysis helps decide what to measure next
- what `blade_coupling` or `cohesion` means in this simplified model

### Day 14: Quality Gates

Run:

```bash
make earthmoving-gate
```

Deliverable:

- add one new threshold or gate rule

Be able to explain:

- how regression gates protect autonomy development
- why gates must be realistic, not aspirational

### Day 15: Week 3 Review

Checkpoint:

- tell the sim-to-real story clearly
- explain the calibration limitations honestly
- show one concrete next measurement priority

## Week 4: Autonomy Evaluation And Final Polish

### Day 16: Dataset Review

Run:

```bash
make earthmoving-dataset
make earthmoving-surrogate
```

Deliverable:

- improve dataset features or labels

Be able to explain:

- what the surrogate predicts
- how learned evaluators can support autonomy testing
- why this is not a replacement for physics

### Day 17: Planner Review

Run:

```bash
make earthmoving-plan-search
```

Deliverable:

- improve the plan score function or add a second scenario search

Be able to explain:

- what the planner optimizes
- what constraints are missing
- how this could evolve toward autonomy scenario generation

### Day 18: Dashboard And Demo

Run:

```bash
make earthmoving-dashboard
```

Deliverable:

- add one visual artifact or dashboard section that helps a reviewer understand the terrain result faster

Best possible extra:

- short screen recording or GIF showing the benchmark, dashboard, and packet

### Day 19: Interview Simulation

Prepare answers for:

- how the terrain model works
- where it is physically wrong
- how you would validate it
- how you would make it faster
- how you would integrate field logs
- why C++ and Rust both appear in the project
- how this supports ML-based autonomy

Deliverable:

- add notes to `OUTREACH_NOTE.md` or a private prep note

### Day 20: Final Review

Run:

```bash
make test
make simulation-packet
make native-kernel-matrix
```

Deliverable:

- final `EARTHMOVING_SIMULATION_PACKET.md`
- final dashboard
- final outreach message

Checkpoint:

- you can walk through the project in 10 minutes
- you can answer technical questions for 30 minutes
- you can state limitations without sounding defensive
- you know the next three things you would build if hired

## What To Build If You Have Extra Time

- Python binding for the C++ or Rust terrain kernel
- multi-pass blade trajectory planner
- terrain profile observation schema and calibration against profile samples
- generated replay video or GIF
- CI job that runs the earthmoving quality gate
- side-by-side terrain visual diff in the dashboard

## Weekly Commit Rhythm

Use clean commits:

- `Add terrain deposit centroid metric`
- `Add sticky soil benchmark scenario`
- `Improve rust terrain kernel error handling`
- `Add coarse-to-fine soil calibration`
- `Add terrain profile field-log schema`
- `Add multi-scenario blade plan search`
- `Polish simulation packet for recruiter review`

Every Friday, run:

```bash
make test
make simulation-packet
git status --short
```
