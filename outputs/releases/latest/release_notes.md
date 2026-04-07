# Release Notes

Comparison: `9947b32` -> `HEAD`

Commits included: `1`

Diffstat: 31 files changed, 4413 insertions(+), 20 deletions(-)

## Regression status

- Gate status: `pass`
- Gate violations: `0`

## Provenance coverage

- Manifest count: `9`
- Run types: `controller_benchmark, domain_randomization, experiment, imitation_dataset, imitation_evaluation, imitation_training, rl_evaluation, rl_training, sweep_suite`

## Changed areas

- `docs`: 2 files
- `dashboard`: 3 files
- `scripts`: 4 files
- `core_python`: 8 files
- `tests`: 1 files
- `outputs`: 11 files
- `ci`: 2 files

## Commits

- `e5ed38a` Add artifact provenance manifests and index

## Trend summary

- `baseline_success_rate`: flat (0.0000), latest `0.1000`
- `baseline_final_error_mean`: flat (0.0000), latest `0.0943`
- `imitation_success_rate`: flat (0.0000), latest `0.3750`
- `imitation_final_error_mean`: flat (0.0000), latest `0.0728`
- `rl_success_rate`: flat (0.0000), latest `0.2500`
- `rl_final_error_mean`: flat (0.0000), latest `0.0869`

## Changed files

- `.github/workflows/ci.yml`
- `Makefile`
- `README.md`
- `dashboard/app.js`
- `dashboard/data.json`
- `dashboard/index.html`
- `docs/provenance-guide.md`
- `outputs/baseline/manifest.json`
- `outputs/controller_benchmark/manifest.json`
- `outputs/domain_randomization/manifest.json`
- `outputs/interesting_sweeps/manifest.json`
- `outputs/learning/dataset/manifest.json`
- `outputs/learning/evaluation/manifest.json`
- `outputs/learning/training/manifest.json`
- `outputs/provenance/index.json`
- `outputs/provenance/index.md`
- `outputs/rl/evaluation/manifest.json`
- `outputs/rl/training/manifest.json`
- `scripts/backfill_provenance_manifests.py`
- `scripts/build_provenance_index.py`
- `scripts/generate_dashboard.py`
- `scripts/smoke_test.py`
- `src/mujoco_sim_debugging_playbook/__init__.py`
- `src/mujoco_sim_debugging_playbook/benchmark.py`
- `src/mujoco_sim_debugging_playbook/environment.py`
- `src/mujoco_sim_debugging_playbook/experiment.py`
- `src/mujoco_sim_debugging_playbook/generalization.py`
- `src/mujoco_sim_debugging_playbook/learning.py`
- `src/mujoco_sim_debugging_playbook/provenance.py`
- `src/mujoco_sim_debugging_playbook/rl.py`
- `tests/test_provenance.py`