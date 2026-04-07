# Container Smoke Guide

Use the container smoke script to verify that the Docker workflow can build the image and execute the repo smoke test end to end.

```bash
bash scripts/run_container_smoke.sh
```

This is useful when validating container setup before asking another engineer to reproduce a problem in the same environment.
