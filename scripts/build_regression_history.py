from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.regression import build_regression_history


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> None:
    parser = argparse.ArgumentParser(description="Build regression history artifacts from saved snapshots.")
    parser.add_argument(
        "--snapshot-dir",
        default=str(ROOT / "outputs" / "regression" / "snapshots"),
        help="Directory containing snapshot JSON files.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "outputs" / "regression" / "history"),
        help="Directory for history outputs.",
    )
    parser.add_argument(
        "--gate-report",
        action="append",
        default=[],
        help="Optional gate report path to associate with one or more snapshots.",
    )
    args = parser.parse_args()

    snapshot_dir = Path(args.snapshot_dir)
    snapshot_paths = sorted(snapshot_dir.glob("*.json"))
    if not snapshot_paths:
        raise SystemExit(f"No snapshots found in {snapshot_dir}")

    gate_reports = {}
    for gate_path_str in args.gate_report:
        gate_path = Path(gate_path_str)
        payload = _read_json(gate_path)
        gate_reports[payload["right"]] = payload

    result = build_regression_history(snapshot_paths, gate_reports, args.output_dir)
    print(f"Regression history written to {args.output_dir}")
    print(f"Snapshots tracked: {len(result['snapshots'])}")


if __name__ == "__main__":
    main()
