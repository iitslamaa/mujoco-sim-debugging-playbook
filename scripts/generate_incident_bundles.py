from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.incidents import build_incident_bundles


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate incident bundles from the support triage queue.")
    parser.add_argument("--triage", default=str(ROOT / "outputs" / "triage" / "triage_queue.json"))
    parser.add_argument("--anomalies", default=str(ROOT / "outputs" / "anomalies" / "anomaly_report.json"))
    parser.add_argument("--recommendations", default=str(ROOT / "outputs" / "recommendations" / "recommendations.json"))
    parser.add_argument("--output-dir", default=str(ROOT / "outputs" / "incidents"))
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    payload = build_incident_bundles(
        triage_queue_path=args.triage,
        anomaly_report_path=args.anomalies,
        recommendation_report_path=args.recommendations,
        output_dir=args.output_dir,
        limit=args.limit,
    )
    print(f"Incident bundles written to {args.output_dir}")
    print(f"Bundles created: {payload['summary']['count']}")


if __name__ == "__main__":
    main()
