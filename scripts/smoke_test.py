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

    payload = json.loads((ROOT / "outputs" / "baseline" / "summary.json").read_text())
    print("Baseline success rate:", payload["summary"]["success_rate"])
    print("Smoke test complete.")


if __name__ == "__main__":
    main()
