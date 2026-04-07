from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.triage import build_triage_queue


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a support triage queue from repo artifacts.")
    parser.add_argument("--anomalies", default=str(ROOT / "outputs" / "anomalies" / "anomaly_report.json"))
    parser.add_argument("--recommendations", default=str(ROOT / "outputs" / "recommendations" / "recommendations.json"))
    parser.add_argument("--regression-gate", default=str(ROOT / "outputs" / "regression" / "gate" / "regression_gate.json"))
    parser.add_argument("--release-notes", default=str(ROOT / "outputs" / "releases" / "latest" / "release_notes.json"))
    parser.add_argument("--output-dir", default=str(ROOT / "outputs" / "triage"))
    args = parser.parse_args()

    payload = build_triage_queue(
        anomaly_report_path=args.anomalies,
        recommendation_report_path=args.recommendations,
        regression_gate_path=args.regression_gate,
        release_notes_path=args.release_notes,
        output_dir=args.output_dir,
    )
    print(f"Triage queue written to {args.output_dir}")
    print(f"Queue items: {payload['summary']['count']}")


if __name__ == "__main__":
    main()
