from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
from mujoco_sim_debugging_playbook.support_intake_checklist import build_support_intake_checklist

def main() -> None:
    build_support_intake_checklist(
        issue_template_audit_path=ROOT / "outputs" / "issue_template_audit" / "issue_template_audit.json",
        response_rubric_path=ROOT / "outputs" / "response_rubric" / "response_rubric.json",
        output_dir=ROOT / "outputs" / "support_intake_checklist",
    )

if __name__ == "__main__":
    main()
