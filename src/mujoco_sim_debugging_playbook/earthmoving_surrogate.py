from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from mujoco_sim_debugging_playbook.provenance import write_manifest


def train_earthmoving_surrogate(
    *,
    dataset_path: str | Path,
    output_dir: str | Path,
    seed: int,
    test_fraction: float = 0.25,
    ridge_alpha: float = 1e-3,
) -> dict[str, Any]:
    dataset = np.load(dataset_path)
    features = np.asarray(dataset["features"], dtype=np.float64)
    labels = np.asarray(dataset["labels"], dtype=np.float64)
    feature_names = [str(item) for item in dataset["feature_names"]]
    label_names = [str(item) for item in dataset["label_names"]]
    train_idx, test_idx = _split_indices(len(features), seed, test_fraction)

    x_train = features[train_idx]
    y_train = labels[train_idx]
    x_test = features[test_idx]
    y_test = labels[test_idx]
    x_mean = x_train.mean(axis=0)
    x_std = np.maximum(x_train.std(axis=0), 1e-9)
    y_mean = y_train.mean(axis=0)
    y_std = np.maximum(y_train.std(axis=0), 1e-9)
    x_train_n = (x_train - x_mean) / x_std
    y_train_n = (y_train - y_mean) / y_std
    weights = _ridge_fit(x_train_n, y_train_n, ridge_alpha)

    predictions = _predict(x_test, weights, x_mean, x_std, y_mean, y_std)
    mae = np.mean(np.abs(predictions - y_test), axis=0)
    rmse = np.sqrt(np.mean((predictions - y_test) ** 2, axis=0))
    baseline = np.repeat(y_train.mean(axis=0, keepdims=True), len(y_test), axis=0)
    baseline_mae = np.mean(np.abs(baseline - y_test), axis=0)
    rows = [
        {
            "label": label,
            "mae": float(mae[index]),
            "rmse": float(rmse[index]),
            "baseline_mae": float(baseline_mae[index]),
            "mae_improvement": float(baseline_mae[index] - mae[index]),
        }
        for index, label in enumerate(label_names)
    ]
    payload = {
        "summary": {
            "train_rows": int(len(train_idx)),
            "test_rows": int(len(test_idx)),
            "feature_count": len(feature_names),
            "label_count": len(label_names),
            "ridge_alpha": ridge_alpha,
            "mean_mae": float(np.mean(mae)),
            "mean_baseline_mae": float(np.mean(baseline_mae)),
        },
        "feature_names": feature_names,
        "label_names": label_names,
        "metrics": rows,
        "model": {
            "weights": weights.tolist(),
            "feature_mean": x_mean.tolist(),
            "feature_std": x_std.tolist(),
            "label_mean": y_mean.tolist(),
            "label_std": y_std.tolist(),
        },
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    model_path = output / "surrogate_model.json"
    report_path = output / "report.md"
    model_path.write_text(json.dumps(payload, indent=2))
    _write_report(payload, report_path)
    write_manifest(
        repo_root=Path.cwd(),
        output_dir=output,
        run_type="earthmoving_surrogate",
        config={"dataset_path": str(dataset_path), "seed": seed, "test_fraction": test_fraction, "ridge_alpha": ridge_alpha},
        inputs=[dataset_path],
        outputs=[model_path, report_path],
        metadata=payload["summary"],
    )
    return payload


def _split_indices(row_count: int, seed: int, test_fraction: float) -> tuple[np.ndarray, np.ndarray]:
    if row_count < 4:
        raise ValueError("at least four rows are required to train the surrogate")
    rng = np.random.default_rng(seed)
    indices = np.arange(row_count)
    rng.shuffle(indices)
    test_count = max(1, int(round(row_count * test_fraction)))
    return indices[test_count:], indices[:test_count]


def _ridge_fit(features: np.ndarray, labels: np.ndarray, alpha: float) -> np.ndarray:
    design = np.column_stack([np.ones(len(features)), features])
    penalty = np.eye(design.shape[1]) * np.sqrt(alpha)
    penalty[0, 0] = 0.0
    augmented_design = np.vstack([design, penalty])
    augmented_labels = np.vstack([labels, np.zeros((design.shape[1], labels.shape[1]))])
    weights, *_ = np.linalg.lstsq(augmented_design, augmented_labels, rcond=None)
    return weights


def _predict(features: np.ndarray, weights: np.ndarray, x_mean: np.ndarray, x_std: np.ndarray, y_mean: np.ndarray, y_std: np.ndarray) -> np.ndarray:
    normalized = (features - x_mean) / x_std
    design = np.column_stack([np.ones(len(normalized)), normalized])
    return (design @ weights) * y_std + y_mean


def _write_report(payload: dict[str, Any], output_path: Path) -> None:
    lines = [
        "# Earthmoving Surrogate",
        "",
        f"Train rows: `{payload['summary']['train_rows']}`",
        f"Test rows: `{payload['summary']['test_rows']}`",
        f"Mean MAE: `{payload['summary']['mean_mae']:.6f}`",
        f"Mean baseline MAE: `{payload['summary']['mean_baseline_mae']:.6f}`",
        "",
        "| label | mae | baseline_mae | improvement | rmse |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in payload["metrics"]:
        lines.append(
            f"| {row['label']} | {row['mae']:.6f} | {row['baseline_mae']:.6f} | "
            f"{row['mae_improvement']:.6f} | {row['rmse']:.6f} |"
        )
    output_path.write_text("\n".join(lines))
