from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.provenance import write_manifest


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def _write_if_summary_exists(summary_path: Path, run_type: str, outputs: list[Path], config: dict | None = None, inputs: list[Path] | None = None, metadata: dict | None = None) -> None:
    if not summary_path.exists():
        return
    write_manifest(
        repo_root=ROOT,
        output_dir=summary_path.parent,
        run_type=run_type,
        config=config or {},
        inputs=inputs or [],
        outputs=outputs,
        metadata=metadata or {},
    )


def main() -> None:
    baseline_dir = ROOT / "outputs" / "baseline"
    baseline_summary = baseline_dir / "summary.json"
    if baseline_summary.exists():
        payload = _read_json(baseline_summary)
        _write_if_summary_exists(
            baseline_summary,
            "experiment",
            [baseline_summary, baseline_dir / "episodes.csv", *sorted((baseline_dir / "traces").glob("*.json")), *sorted((baseline_dir / "trace_plots").glob("*.png"))],
            config=payload.get("config", {}),
            metadata={"summary": payload.get("summary", {})},
        )

    sweep_dir = ROOT / "outputs" / "interesting_sweeps"
    combined_json = sweep_dir / "combined_summary.json"
    if combined_json.exists():
        rows = _read_json(combined_json)
        _write_if_summary_exists(
            combined_json,
            "sweep_suite",
            [combined_json, sweep_dir / "combined_summary.csv", sweep_dir / "report.md", *sorted(sweep_dir.glob("*.png"))],
            config={"suite_name": "interesting_sweeps"},
            metadata={"scenario_count": len(rows)},
        )

    dataset_dir = ROOT / "outputs" / "learning" / "dataset"
    dataset_summary = dataset_dir / "dataset_summary.json"
    if dataset_summary.exists():
        payload = _read_json(dataset_summary)
        dataset_path = dataset_dir / "imitation_dataset.npz"
        _write_if_summary_exists(
            dataset_summary,
            "imitation_dataset",
            [dataset_summary, dataset_path, *sorted((dataset_dir / "expert_traces").glob("*.json")), *sorted((dataset_dir / "expert_trace_plots").glob("*.png"))],
            config={"episodes": payload.get("episodes")},
            metadata={"num_samples": payload.get("num_samples")},
        )

    training_dir = ROOT / "outputs" / "learning" / "training"
    training_summary = training_dir / "training_summary.json"
    if training_summary.exists():
        payload = _read_json(training_summary)
        _write_if_summary_exists(
            training_summary,
            "imitation_training",
            [training_summary, training_dir / "policy.pt", training_dir / "training_curve.png"],
            metadata={"best_val_loss": payload.get("best_val_loss")},
        )

    eval_dir = ROOT / "outputs" / "learning" / "evaluation"
    eval_summary = eval_dir / "summary.json"
    if eval_summary.exists():
        payload = _read_json(eval_summary)
        _write_if_summary_exists(
            eval_summary,
            "imitation_evaluation",
            [eval_summary, *sorted((eval_dir / "traces").glob("*.json")), *sorted((eval_dir / "trace_plots").glob("*.png"))],
            inputs=[Path(payload["checkpoint_path"])] if payload.get("checkpoint_path") else [],
            metadata={"summary": payload.get("summary", {})},
        )

    rl_train_dir = ROOT / "outputs" / "rl" / "training"
    rl_train_summary = rl_train_dir / "training_summary.json"
    if rl_train_summary.exists():
        payload = _read_json(rl_train_summary)
        _write_if_summary_exists(
            rl_train_summary,
            "rl_training",
            [rl_train_summary, rl_train_dir / "reinforce_policy.pt", rl_train_dir / "training_curve.png"],
            metadata={"iterations": payload.get("iterations")},
        )

    rl_eval_dir = ROOT / "outputs" / "rl" / "evaluation"
    rl_eval_summary = rl_eval_dir / "summary.json"
    if rl_eval_summary.exists():
        payload = _read_json(rl_eval_summary)
        _write_if_summary_exists(
            rl_eval_summary,
            "rl_evaluation",
            [rl_eval_summary, *sorted((rl_eval_dir / "traces").glob("*.json")), *sorted((rl_eval_dir / "trace_plots").glob("*.png"))],
            inputs=[Path(payload["checkpoint_path"])] if payload.get("checkpoint_path") else [],
            metadata={"summary": payload.get("summary", {})},
        )

    benchmark_dir = ROOT / "outputs" / "controller_benchmark"
    benchmark_summary = benchmark_dir / "benchmark_summary.json"
    if benchmark_summary.exists():
        payload = _read_json(benchmark_summary)
        inputs = [ROOT / "configs" / "controller_benchmark.json"]
        if payload.get("checkpoint_path"):
            inputs.append(Path(payload["checkpoint_path"]))
        _write_if_summary_exists(
            benchmark_summary,
            "controller_benchmark",
            [benchmark_summary, benchmark_dir / "report.md", *sorted(benchmark_dir.glob("*.png"))],
            inputs=inputs,
            metadata={"row_count": len(payload.get("benchmark_rows", []))},
        )

    random_dir = ROOT / "outputs" / "domain_randomization"
    random_summary = random_dir / "evaluation_rows.json"
    if random_summary.exists():
        payload = _read_json(random_summary)
        inputs = [ROOT / "configs" / "domain_randomization.json"]
        if payload.get("torch_checkpoint"):
            inputs.append(Path(payload["torch_checkpoint"]))
        if payload.get("rl_checkpoint"):
            inputs.append(Path(payload["rl_checkpoint"]))
        _write_if_summary_exists(
            random_summary,
            "domain_randomization",
            [random_summary, random_dir / "report.md", *sorted(random_dir.glob("*.png"))],
            inputs=inputs,
            metadata={"row_count": len(payload.get("rows", []))},
        )

    print("Backfilled provenance manifests for available outputs.")


if __name__ == "__main__":
    main()
