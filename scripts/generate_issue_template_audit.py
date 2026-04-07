from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.issue_template_audit import build_issue_template_audit


def main() -> None:
    payload = build_issue_template_audit(
        template_dir=ROOT / ".github" / "ISSUE_TEMPLATE",
        output_dir=ROOT / "outputs" / "issue_template_audit",
    )
    print(
        "Wrote issue template audit with "
        f"{payload['summary']['template_count']} templates to {ROOT / 'outputs' / 'issue_template_audit'}"
    )


if __name__ == "__main__":
    main()
