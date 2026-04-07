from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.recommendations import build_recommendation_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate mitigation recommendations from anomalies and sweeps.")
    parser.add_argument(
        "--anomalies",
        default=str(ROOT / "outputs" / "anomalies" / "anomaly_report.json"),
    )
    parser.add_argument(
        "--sweeps",
        default=str(ROOT / "outputs" / "interesting_sweeps" / "combined_summary.json"),
    )
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "outputs" / "recommendations"),
    )
    args = parser.parse_args()

    payload = build_recommendation_report(
        anomaly_report_path=args.anomalies,
        sweep_summary_path=args.sweeps,
        output_dir=args.output_dir,
    )
    print(f"Recommendation report written to {args.output_dir}")
    print(f"Recommendations generated: {len(payload['recommendations'])}")


if __name__ == "__main__":
    main()
