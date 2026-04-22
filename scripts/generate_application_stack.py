from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

COMMANDS = [
    "generate_jobsite_autonomy_eval.py",
    "generate_earthmoving_review_packet.py",
    "generate_earthmoving_dashboard.py",
    "generate_earthmoving_role_brief.py",
    "generate_earthmoving_replay.py",
    "generate_multipass_plan_eval.py",
    "generate_task_plan_robustness.py",
    "generate_robustness_sensitivity.py",
    "generate_field_trial_visuals.py",
    "generate_field_trial_case_study.py",
    "generate_hiring_manager_packet.py",
    "generate_simulation_packet.py",
    "generate_application_packet.py",
    "generate_interview_assets.py",
    "generate_application_bundle.py",
    "generate_application_readiness.py",
]


def main() -> int:
    python = ROOT / ".venv" / "bin" / "python"
    executable = str(python if python.exists() else Path(sys.executable))
    for script in COMMANDS:
        print(f"running {script}", flush=True)
        subprocess.run([executable, str(ROOT / "scripts" / script)], cwd=ROOT, check=True)
    print(f"rebuilt application stack with {len(COMMANDS)} steps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
