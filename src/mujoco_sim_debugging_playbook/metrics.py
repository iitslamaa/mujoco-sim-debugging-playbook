from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class EpisodeMetrics:
    success: bool
    final_error: float
    min_error: float
    mean_error: float
    max_overshoot: float
    settling_time_s: float | None
    oscillation_index: float
    control_energy: float


def compute_episode_metrics(
    errors: np.ndarray,
    torques: np.ndarray,
    control_dt: float,
    target_radius: float,
) -> EpisodeMetrics:
    errors = np.asarray(errors, dtype=float)
    torques = np.asarray(torques, dtype=float)
    final_error = float(errors[-1])
    min_error = float(np.min(errors))
    mean_error = float(np.mean(errors))
    success = final_error <= target_radius

    overshoot_reference = max(target_radius, float(errors[0]))
    max_overshoot = float(np.max(errors) - overshoot_reference)
    max_overshoot = max(0.0, max_overshoot)

    settling_time_s: float | None = None
    within_band = errors <= target_radius
    for index in range(len(errors)):
        if np.all(within_band[index:]):
            settling_time_s = index * control_dt
            break

    diffs = np.diff(errors)
    sign_changes = int(np.sum(np.sign(diffs[1:]) != np.sign(diffs[:-1]))) if len(diffs) >= 2 else 0
    oscillation_index = sign_changes / max(len(errors) - 1, 1)

    control_energy = float(np.sum(np.sum(torques * torques, axis=1)) * control_dt)

    return EpisodeMetrics(
        success=success,
        final_error=final_error,
        min_error=min_error,
        mean_error=mean_error,
        max_overshoot=max_overshoot,
        settling_time_s=settling_time_s,
        oscillation_index=float(oscillation_index),
        control_energy=control_energy,
    )


def aggregate_metrics(metric_rows: list[EpisodeMetrics]) -> dict[str, float]:
    success_rate = float(np.mean([row.success for row in metric_rows])) if metric_rows else 0.0

    def mean(name: str) -> float:
        values = [getattr(row, name) for row in metric_rows]
        return float(np.mean(values)) if values else 0.0

    settling_values = [row.settling_time_s for row in metric_rows if row.settling_time_s is not None]

    return {
        "success_rate": success_rate,
        "final_error_mean": mean("final_error"),
        "min_error_mean": mean("min_error"),
        "mean_error_mean": mean("mean_error"),
        "max_overshoot_mean": mean("max_overshoot"),
        "oscillation_index_mean": mean("oscillation_index"),
        "control_energy_mean": mean("control_energy"),
        "settling_time_mean": float(np.mean(settling_values)) if settling_values else float("nan"),
    }

