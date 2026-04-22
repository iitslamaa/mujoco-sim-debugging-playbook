from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

sys.path.insert(0, str(SCRIPTS))

from generate_application_stack import COMMANDS


def test_application_stack_scripts_exist_in_order() -> None:
    assert COMMANDS[0] == "generate_jobsite_autonomy_eval.py"
    assert COMMANDS[-1] == "generate_application_readiness.py"
    missing = [script for script in COMMANDS if not (SCRIPTS / script).exists()]
    assert missing == []
