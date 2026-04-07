from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.knowledge_base import build_knowledge_base


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a support knowledge base from incident bundles.")
    parser.add_argument("--incidents", default=str(ROOT / "outputs" / "incidents" / "index.json"))
    parser.add_argument("--recommendations", default=str(ROOT / "outputs" / "recommendations" / "recommendations.json"))
    parser.add_argument("--output-dir", default=str(ROOT / "outputs" / "knowledge_base"))
    args = parser.parse_args()

    payload = build_knowledge_base(
        incidents_index_path=args.incidents,
        recommendations_path=args.recommendations,
        output_dir=args.output_dir,
    )
    print(f"Knowledge base written to {args.output_dir}")
    print(f"Entries created: {payload['summary']['count']}")


if __name__ == "__main__":
    main()
