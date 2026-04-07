from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.release_notes import build_release_notes


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate release notes between two Git refs.")
    parser.add_argument("--base", required=True, help="Base Git ref.")
    parser.add_argument("--head", default="HEAD", help="Head Git ref.")
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "outputs" / "releases" / "latest"),
        help="Directory for release note artifacts.",
    )
    args = parser.parse_args()

    payload = build_release_notes(
        repo_root=ROOT,
        base_ref=args.base,
        head_ref=args.head,
        output_dir=args.output_dir,
    )
    print(f"Release notes written to {args.output_dir}")
    print(f"Commits included: {payload['commit_count']}")


if __name__ == "__main__":
    main()
