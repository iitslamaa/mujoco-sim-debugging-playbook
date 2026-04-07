from __future__ import annotations

import platform
import subprocess
import sys
from pathlib import Path

import mujoco
import numpy as np


def _safe_command(command: list[str]) -> str | None:
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True)
    except FileNotFoundError:
        return None
    output = (completed.stdout or completed.stderr).strip()
    return output or None


def capture_environment_report(repo_root: str | Path) -> dict[str, object]:
    root = Path(repo_root).resolve()
    python_executable = sys.executable
    pip_freeze = _safe_command([python_executable, "-m", "pip", "freeze"])
    git_head = _safe_command(["git", "rev-parse", "HEAD"])
    git_branch = _safe_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    git_status = _safe_command(["git", "status", "--short"])

    return {
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python_version": platform.python_version(),
        },
        "runtime": {
            "python_executable": python_executable,
            "numpy_version": np.__version__,
            "mujoco_version": mujoco.__version__,
        },
        "tooling": {
            "git_head": git_head,
            "git_branch": git_branch,
            "git_is_dirty": bool(git_status),
            "git_status": git_status.splitlines() if git_status else [],
            "docker_version": _safe_command(["docker", "--version"]),
            "gh_version": _safe_command(["gh", "--version"]),
        },
        "workspace": {
            "repo_root": str(root),
            "pip_freeze": pip_freeze.splitlines() if pip_freeze else [],
        },
    }
