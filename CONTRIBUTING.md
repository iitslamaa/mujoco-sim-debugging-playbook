# Contributing

This repository is intentionally structured like a small simulation support project. Contributions should optimize for reproducibility, debuggability, and clarity for the next user.

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e . --no-build-isolation
```

## Common commands

```bash
make test
make baseline
make sweep
make smoke
```

## Contribution expectations

- Keep experiments config-driven and reproducible.
- Prefer small, reviewable changes with a clear motivation.
- If you change behavior, update docs and at least one test.
- When fixing a support-style issue, add or update a case under `cases/issue_cases/`.
- Include exact commands in docs so others can reproduce your results.

## Debugging workflow

1. Reproduce with a known config and fixed seed.
2. Reduce the problem to one changed parameter when possible.
3. Save outputs under `outputs/`.
4. Document the finding in plain language, not only in code.

