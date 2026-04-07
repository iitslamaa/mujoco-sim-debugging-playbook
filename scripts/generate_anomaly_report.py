from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.anomaly import build_anomaly_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate anomaly analysis from benchmark and randomization outputs.")
    parser.add_argument(
        "--benchmark",
        default=str(ROOT / "outputs" / "controller_benchmark" / "benchmark_summary.json"),
    )
    parser.add_argument(
        "--randomization",
        default=str(ROOT / "outputs" / "domain_randomization" / "evaluation_rows.json"),
    )
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "outputs" / "anomalies"),
    )
    args = parser.parse_args()

    payload = build_anomaly_report(
        benchmark_summary_path=args.benchmark,
        randomization_rows_path=args.randomization,
        output_dir=args.output_dir,
    )
    print(f"Anomaly report written to {args.output_dir}")
    print(f"Benchmark cases ranked: {len(payload['benchmark_anomalies']['top_cases'])}")


if __name__ == "__main__":
    main()
