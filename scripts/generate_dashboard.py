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
    rl_training = _read_json(ROOT / "outputs" / "rl" / "training" / "training_summary.json")
    rl_evaluation = _read_json(ROOT / "outputs" / "rl" / "evaluation" / "summary.json")
    benchmark_summary = _read_json(ROOT / "outputs" / "controller_benchmark" / "benchmark_summary.json")
    randomization_summary = _read_json(ROOT / "outputs" / "domain_randomization" / "evaluation_rows.json")
    regression_diff = _read_json(ROOT / "outputs" / "regression" / "latest_diff" / "regression_diff.json")
    regression_gate = _read_json(ROOT / "outputs" / "regression" / "gate" / "regression_gate.json")
    regression_history = _read_json(ROOT / "outputs" / "regression" / "history" / "history.json")
    provenance_index = _read_json(ROOT / "outputs" / "provenance" / "index.json")
    release_notes = _read_json(ROOT / "outputs" / "releases" / "latest" / "release_notes.json")
    anomalies = _read_json(ROOT / "outputs" / "anomalies" / "anomaly_report.json")
    recommendations = _read_json(ROOT / "outputs" / "recommendations" / "recommendations.json")
    triage = _read_json(ROOT / "outputs" / "triage" / "triage_queue.json")
    incidents = _read_json(ROOT / "outputs" / "incidents" / "index.json")
    knowledge_base = _read_json(ROOT / "outputs" / "knowledge_base" / "index.json")
    escalation = _read_json(ROOT / "outputs" / "escalation" / "escalation_matrix.json")
    support_ops = _read_json(ROOT / "outputs" / "support_ops" / "support_ops.json")
    support_gaps = _read_json(ROOT / "outputs" / "support_gaps" / "support_gaps.json")
    workstreams = _read_json(ROOT / "outputs" / "workstreams" / "workstream_plan.json")
    sla = _read_json(ROOT / "outputs" / "sla" / "sla_report.json")
    case_study_exists = (ROOT / "outputs" / "case_studies" / "controller_robustness_story.md").exists()
    support_cases = []
    for case_path in sorted((ROOT / "outputs" / "support_cases").glob("*.md")):
        support_cases.append(
            {
                "name": case_path.stem,
                "path": str(case_path.relative_to(ROOT)),
            }
        )

    provenance_summary = None
    if provenance_index:
        provenance_summary = {
            "summary": provenance_index["summary"],
            "recent_manifests": [
                {
                    "run_type": entry["run_type"],
                    "created_at": entry["created_at"],
                    "manifest_path": entry["manifest_path"],
                    "git_head": entry["environment"]["tooling"].get("git_head"),
                    "git_is_dirty": entry["environment"]["tooling"].get("git_is_dirty"),
                }
                for entry in provenance_index.get("manifests", [])[:5]
            ],
        }

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
        "rl_training": {
            "iterations": rl_training["iterations"],
            "episodes_per_iteration": rl_training["episodes_per_iteration"],
            "final_return": rl_training["history"][-1]["mean_episode_return"],
            "final_success_rate": rl_training["history"][-1]["success_rate"],
            "policy_std": rl_training["history"][-1]["policy_std"],
        } if rl_training else None,
        "rl_evaluation": rl_evaluation,
        "benchmark_summary": benchmark_summary,
        "randomization_summary": randomization_summary,
        "regression_diff": regression_diff,
        "regression_gate": regression_gate,
        "regression_history": regression_history,
        "provenance_index": provenance_summary,
        "release_notes": release_notes,
        "anomalies": anomalies,
        "recommendations": recommendations,
        "triage": triage,
        "incidents": incidents,
        "knowledge_base": knowledge_base,
        "escalation": escalation,
        "support_ops": support_ops,
        "support_gaps": support_gaps,
        "workstreams": workstreams,
        "sla": sla,
        "case_studies": {
            "controller_robustness_story": "outputs/case_studies/controller_robustness_story.md"
        } if case_study_exists else None,
        "support_cases": support_cases,
        "artifacts": {
            "demo_gif": "outputs/media/reacher_demo.gif",
            "training_curve": "outputs/learning/training/training_curve.png",
            "rl_training_curve": "outputs/rl/training/training_curve.png",
            "diagnostics_markdown": "outputs/diagnostics/diagnostics.md",
            "support_case_markdown": "outputs/support_cases/actuator_gain_overshoot.md",
            "benchmark_report": "outputs/controller_benchmark/report.md",
            "randomization_report": "outputs/domain_randomization/report.md",
            "case_study_image": "outputs/case_studies/controller_robustness_story.png",
            "regression_diff_markdown": "outputs/regression/latest_diff/regression_diff.md",
            "regression_diff_image": "outputs/regression/latest_diff/regression_diff.png",
            "regression_gate_markdown": "outputs/regression/gate/regression_gate.md",
            "regression_history_markdown": "outputs/regression/history/history.md",
            "regression_history_image": "outputs/regression/history/history.png",
            "provenance_index_markdown": "outputs/provenance/index.md",
            "release_notes_markdown": "outputs/releases/latest/release_notes.md",
            "anomaly_report_markdown": "outputs/anomalies/anomaly_report.md",
            "anomaly_benchmark_image": "outputs/anomalies/benchmark_risk_heatmap.png",
            "anomaly_difficulty_image": "outputs/anomalies/randomization_difficulty.png",
            "recommendations_markdown": "outputs/recommendations/recommendations.md",
            "triage_markdown": "outputs/triage/triage_queue.md",
            "incident_index_markdown": "outputs/incidents/index.md",
            "knowledge_base_markdown": "outputs/knowledge_base/index.md",
            "escalation_markdown": "outputs/escalation/escalation_matrix.md",
            "support_ops_markdown": "outputs/support_ops/support_ops.md",
            "support_gaps_markdown": "outputs/support_gaps/support_gaps.md",
            "workstream_plan_markdown": "outputs/workstreams/workstream_plan.md",
            "sla_markdown": "outputs/sla/sla_report.md",
        },
    }
    (dashboard_dir / "data.json").write_text(json.dumps(payload, indent=2))
    print(f"Dashboard data written to {dashboard_dir / 'data.json'}")


if __name__ == "__main__":
    main()
