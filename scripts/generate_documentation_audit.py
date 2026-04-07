from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.documentation_audit import build_documentation_audit


def _render_markdown(payload: dict) -> str:
    lines = [
        "# Documentation Audit",
        "",
        f"- Knowledge-base coverage: `{payload['summary']['knowledge_base_coverage'] * 100:.1f}%`",
        f"- Knowledge-base entries: `{payload['summary']['entry_count']}`",
        f"- Uncovered targets: `{payload['summary']['uncovered_count']}`",
        "",
        "## Uncovered Targets",
        "",
    ]
    for target in payload["uncovered_targets"]:
        lines.append(f"- {target}")
    return "\n".join(lines)


def main() -> None:
    payload = build_documentation_audit(
        support_ops_path=ROOT / "outputs" / "support_ops" / "support_ops.json",
        support_gaps_path=ROOT / "outputs" / "support_gaps" / "support_gaps.json",
        knowledge_base_path=ROOT / "outputs" / "knowledge_base" / "index.json",
    )
    output_dir = ROOT / "outputs" / "documentation_audit"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "documentation_audit.json").write_text(json.dumps(payload, indent=2))
    (output_dir / "documentation_audit.md").write_text(_render_markdown(payload))
    print(f"Documentation audit written to {output_dir}")


if __name__ == "__main__":
    main()
