from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_gate import evaluate_earthmoving_gate, write_earthmoving_gate_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate earthmoving benchmark realism and throughput gates.")
    parser.add_argument("--benchmark-summary", default=str(ROOT / "outputs" / "earthmoving_benchmark" / "earthmoving_summary.json"))
    parser.add_argument("--scale-summary", default=str(ROOT / "outputs" / "earthmoving_scale" / "scale_summary.json"))
    parser.add_argument("--thresholds", default=str(ROOT / "configs" / "earthmoving_thresholds.json"))
    parser.add_argument("--output-dir", default=str(ROOT / "outputs" / "earthmoving_gate"))
    parser.add_argument("--allow-failures", action="store_true")
    args = parser.parse_args()

    report = evaluate_earthmoving_gate(
        benchmark_summary_path=args.benchmark_summary,
        thresholds_path=args.thresholds,
        scale_summary_path=args.scale_summary,
    )
    write_earthmoving_gate_report(report, args.output_dir)
    print(f"Earthmoving gate status: {report['status']}")
    print(f"Violations: {report['violation_count']}")
    if report["status"] != "pass" and not args.allow_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
