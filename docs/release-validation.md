# Release Validation Checklist

This checklist is written from a user-support perspective for sanity-checking a new simulator or environment release.

## Environment and install

- fresh virtualenv install succeeds
- Docker build succeeds
- smoke test runs without manual fixes
- baseline experiment produces outputs in the documented locations
- diagnostics bundle generation succeeds

## Behavior validation

- baseline success rate is within an expected band
- key sweep configs finish without crashing
- output plots and reports generate successfully
- no change silently breaks support-case scripts
- trace plots are produced for per-episode inspection

## User-facing artifacts

- README commands still match actual behavior
- troubleshooting guide reflects current failure modes
- issue templates still ask for enough context to reproduce problems
- support case outputs still point to valid files and metrics
