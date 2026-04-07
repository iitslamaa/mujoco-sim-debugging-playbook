from pathlib import Path
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], env: dict[str, str] | None = None) -> None:
    print(f"$ {' '.join(command)}")
    subprocess.run(command, cwd=ROOT, check=True, env=env)


def main() -> None:
    env = dict(os.environ)
    env.setdefault("MPLCONFIGDIR", "/tmp/mpl")

    run([sys.executable, "scripts/run_baseline.py", "--episodes", "2"], env=env)
    run([sys.executable, "scripts/run_issue_case.py", "--case", "actuator_gain_overshoot"], env=env)
    run(
        [
            sys.executable,
            "scripts/generate_diagnostics_bundle.py",
            "--summary",
            "outputs/baseline/summary.json",
            "--label",
            "baseline",
            "--summary",
            "outputs/interesting_sweeps/actuator_gain_18p0/summary.json",
            "--label",
            "actuator_gain_18",
        ],
        env=env,
    )
    run(
        [
            sys.executable,
            "scripts/train_torch_policy.py",
            "--dataset-episodes",
            "4",
            "--epochs",
            "3",
        ],
        env=env,
    )
    run(
        [
            sys.executable,
            "scripts/evaluate_torch_policy.py",
            "--episodes",
            "2",
        ],
        env=env,
    )
    run(
        [
            sys.executable,
            "scripts/generate_demo_gif.py",
            "--trace",
            "outputs/learning/evaluation/traces/episode_000.json",
            "--output",
            "outputs/media/reacher_demo.gif",
            "--title",
            "PyTorch policy rollout",
        ],
        env=env,
    )
    run([sys.executable, "scripts/backfill_provenance_manifests.py"], env=env)
    run([sys.executable, "scripts/build_provenance_index.py"], env=env)
    run([sys.executable, "scripts/generate_anomaly_report.py"], env=env)
    run([sys.executable, "scripts/generate_recommendations.py"], env=env)
    run([sys.executable, "scripts/generate_triage_queue.py"], env=env)
    run([sys.executable, "scripts/generate_incident_bundles.py"], env=env)
    run([sys.executable, "scripts/generate_knowledge_base.py"], env=env)
    run([sys.executable, "scripts/generate_escalation_matrix.py"], env=env)
    run([sys.executable, "scripts/generate_support_ops_report.py"], env=env)
    run([sys.executable, "scripts/generate_support_gap_report.py"], env=env)
    run(
        [
            sys.executable,
            "scripts/generate_release_notes.py",
            "--base",
            "9947b32",
            "--head",
            "HEAD",
            "--output-dir",
            "outputs/releases/latest",
        ],
        env=env,
    )
    run([sys.executable, "scripts/generate_dashboard.py"], env=env)

    summary_path = ROOT / "outputs" / "support_cases" / "actuator_gain_overshoot.md"
    if not summary_path.exists():
        raise SystemExit(f"Expected support case output at {summary_path}")
    diagnostics_path = ROOT / "outputs" / "diagnostics" / "diagnostics.md"
    if not diagnostics_path.exists():
        raise SystemExit(f"Expected diagnostics bundle at {diagnostics_path}")
    learning_checkpoint = ROOT / "outputs" / "learning" / "training" / "policy.pt"
    if not learning_checkpoint.exists():
        raise SystemExit(f"Expected policy checkpoint at {learning_checkpoint}")
    demo_gif = ROOT / "outputs" / "media" / "reacher_demo.gif"
    if not demo_gif.exists():
        raise SystemExit(f"Expected demo GIF at {demo_gif}")
    dashboard_data = ROOT / "dashboard" / "data.json"
    if not dashboard_data.exists():
        raise SystemExit(f"Expected dashboard data at {dashboard_data}")
    provenance_index = ROOT / "outputs" / "provenance" / "index.json"
    if not provenance_index.exists():
        raise SystemExit(f"Expected provenance index at {provenance_index}")
    release_notes = ROOT / "outputs" / "releases" / "latest" / "release_notes.json"
    if not release_notes.exists():
        raise SystemExit(f"Expected release notes at {release_notes}")
    anomaly_report = ROOT / "outputs" / "anomalies" / "anomaly_report.json"
    if not anomaly_report.exists():
        raise SystemExit(f"Expected anomaly report at {anomaly_report}")
    recommendation_report = ROOT / "outputs" / "recommendations" / "recommendations.json"
    if not recommendation_report.exists():
        raise SystemExit(f"Expected recommendations at {recommendation_report}")
    triage_queue = ROOT / "outputs" / "triage" / "triage_queue.json"
    if not triage_queue.exists():
        raise SystemExit(f"Expected triage queue at {triage_queue}")
    incidents_index = ROOT / "outputs" / "incidents" / "index.json"
    if not incidents_index.exists():
        raise SystemExit(f"Expected incident bundles at {incidents_index}")
    knowledge_base = ROOT / "outputs" / "knowledge_base" / "index.json"
    if not knowledge_base.exists():
        raise SystemExit(f"Expected knowledge base at {knowledge_base}")
    escalation = ROOT / "outputs" / "escalation" / "escalation_matrix.json"
    if not escalation.exists():
        raise SystemExit(f"Expected escalation matrix at {escalation}")
    support_ops = ROOT / "outputs" / "support_ops" / "support_ops.json"
    if not support_ops.exists():
        raise SystemExit(f"Expected support ops report at {support_ops}")
    support_gaps = ROOT / "outputs" / "support_gaps" / "support_gaps.json"
    if not support_gaps.exists():
        raise SystemExit(f"Expected support gap report at {support_gaps}")

    payload = json.loads((ROOT / "outputs" / "baseline" / "summary.json").read_text())
    print("Baseline success rate:", payload["summary"]["success_rate"])
    print("Smoke test complete.")


if __name__ == "__main__":
    main()
