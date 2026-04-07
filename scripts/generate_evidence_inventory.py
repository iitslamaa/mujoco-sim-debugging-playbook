from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.evidence_inventory import build_evidence_inventory


def _render_markdown(payload: dict) -> str:
    lines = [
        "# Evidence Inventory",
        "",
        f"- Files indexed: `{payload['summary']['file_count']}`",
        f"- Output areas: `{payload['summary']['area_count']}`",
        "",
        "| area | path | suffix |",
        "| --- | --- | --- |",
    ]
    for row in payload["rows"][:80]:
        lines.append(f"| {row['area']} | {row['path']} | {row['suffix']} |")
    return "\n".join(lines)


def main() -> None:
    payload = build_evidence_inventory(root=ROOT)
    output_dir = ROOT / "outputs" / "evidence_inventory"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "evidence_inventory.json").write_text(json.dumps(payload, indent=2))
    (output_dir / "evidence_inventory.md").write_text(_render_markdown(payload))
    print(f"Evidence inventory written to {output_dir}")


if __name__ == "__main__":
    main()
