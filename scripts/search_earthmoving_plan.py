from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_plan_search import search_earthmoving_blade_plan


def main() -> None:
    parser = argparse.ArgumentParser(description="Search simple blade plans for an earthmoving scenario.")
    parser.add_argument("--scenario", default="baseline_push")
    parser.add_argument("--output-dir", default=str(ROOT / "outputs" / "earthmoving_plan_search"))
    args = parser.parse_args()
    payload = search_earthmoving_blade_plan(
        config_path=ROOT / "configs" / "earthmoving_benchmark.json",
        scenario_name=args.scenario,
        output_dir=args.output_dir,
    )
    best = payload["summary"]["best_candidate"]
    print(f"Best earthmoving plan: {best['candidate']} score={best['score']:.6f}")


if __name__ == "__main__":
    main()
