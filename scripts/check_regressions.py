from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.regression import (
    compare_snapshots,
    evaluate_regression_diff,
    load_regression_thresholds,
    write_regression_gate_report,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate regression diff against configured thresholds.")
    parser.add_argument("--left", required=True, help="Reference snapshot path.")
    parser.add_argument("--right", required=True, help="Candidate snapshot path.")
    parser.add_argument(
        "--thresholds",
        default=str(ROOT / "configs" / "regression_thresholds.json"),
        help="Threshold configuration JSON.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "outputs" / "regression" / "gate"),
        help="Directory for gate outputs.",
    )
    parser.add_argument(
        "--allow-failures",
        action="store_true",
        help="Exit successfully even when a threshold is violated.",
    )
    args = parser.parse_args()

    diff_payload = compare_snapshots(args.left, args.right, args.output_dir)
    thresholds = load_regression_thresholds(args.thresholds)
    report = evaluate_regression_diff(diff_payload, thresholds)
    write_regression_gate_report(report, args.output_dir)

    print(f"Regression gate status: {report['status']}")
    print(f"Violations: {report['violation_count']}")

    if report["status"] != "pass" and not args.allow_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
