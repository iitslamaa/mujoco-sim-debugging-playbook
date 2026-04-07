from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def _read_json(path: Path):
    return json.loads(path.read_text()) if path.exists() else None


def main() -> None:
    dashboard_dir = ROOT / "dashboard"
    dashboard_dir.mkdir(parents=True, exist_ok=True)

    baseline = _read_json(ROOT / "outputs" / "baseline" / "summary.json")
    diagnostics = _read_json(ROOT / "outputs" / "diagnostics" / "environment.json")
    learning_training = _read_json(ROOT / "outputs" / "learning" / "training" / "training_summary.json")
    learning_eval = _read_json(ROOT / "outputs" / "learning" / "evaluation" / "summary.json")
    support_cases = []
    for case_path in sorted((ROOT / "outputs" / "support_cases").glob("*.md")):
        support_cases.append(
            {
                "name": case_path.stem,
                "path": str(case_path.relative_to(ROOT)),
            }
        )

    payload = {
        "repo": "mujoco-sim-debugging-playbook",
        "baseline_summary": baseline["summary"] if baseline else None,
        "environment": {
            "platform": diagnostics["platform"] if diagnostics else None,
            "runtime": diagnostics["runtime"] if diagnostics else None,
            "tooling": diagnostics["tooling"] if diagnostics else None,
        } if diagnostics else None,
        "learning_training": {
            "epochs": learning_training["epochs"],
            "best_val_loss": learning_training["best_val_loss"],
            "batch_size": learning_training["batch_size"],
            "learning_rate": learning_training["learning_rate"],
            "final_train_loss": learning_training["history"][-1]["train_loss"],
            "final_val_loss": learning_training["history"][-1]["val_loss"],
        } if learning_training else None,
        "learning_evaluation": learning_eval,
        "support_cases": support_cases,
        "artifacts": {
            "demo_gif": "outputs/media/reacher_demo.gif",
            "training_curve": "outputs/learning/training/training_curve.png",
            "diagnostics_markdown": "outputs/diagnostics/diagnostics.md",
            "support_case_markdown": "outputs/support_cases/actuator_gain_overshoot.md",
        },
    }
    (dashboard_dir / "data.json").write_text(json.dumps(payload, indent=2))
    print(f"Dashboard data written to {dashboard_dir / 'data.json'}")


if __name__ == "__main__":
    main()
