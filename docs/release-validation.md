# Release Validation Checklist

This checklist is written from a user-support perspective, mirroring how a technical solutions engineer would sanity-check a new simulator or environment release.

## Environment and install

- fresh virtualenv install succeeds
- Docker build succeeds
- smoke test runs without manual fixes
- baseline experiment produces outputs in the documented locations

## Behavior validation

- baseline success rate is within an expected band
- key sweep configs finish without crashing
- output plots and reports generate successfully
- no change silently breaks support-case scripts

## User-facing artifacts

- README commands still match actual behavior
- troubleshooting guide reflects current failure modes
- issue templates still ask for enough context to reproduce problems
- support case outputs still point to valid files and metrics

