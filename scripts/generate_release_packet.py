from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.release_packet import build_release_packet


def _render_markdown(payload: dict) -> str:
    lines = [
        "# Release Packet",
        "",
        f"- Range: `{payload['summary']['base_ref']} -> {payload['summary']['head_ref']}`",
        f"- Commits: `{payload['summary']['commit_count']}`",
        f"- Support status: `{payload['summary']['support_status']}`",
        f"- Breaches: `{payload['summary']['breach_count']}`",
        "",
        "## Highlights",
        "",
    ]
    for item in payload["highlights"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Risks", ""])
    for item in payload["risks"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


def main() -> None:
    payload = build_release_packet(
        release_notes_path=ROOT / "outputs" / "releases" / "latest" / "release_notes.json",
        support_readiness_path=ROOT / "outputs" / "support_readiness" / "support_readiness.json",
        ops_review_path=ROOT / "outputs" / "ops_review" / "ops_review.json",
    )
    output_dir = ROOT / "outputs" / "release_packet"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "release_packet.json").write_text(json.dumps(payload, indent=2))
    (output_dir / "release_packet.md").write_text(_render_markdown(payload))
    print(f"Release packet written to {output_dir}")


if __name__ == "__main__":
    main()
