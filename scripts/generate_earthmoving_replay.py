from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.earthmoving_replay import build_earthmoving_replay_bundle


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a replay/debug bundle for one earthmoving scenario.")
    parser.add_argument("--scenario", default="cohesive_soil")
    parser.add_argument("--config", default=str(ROOT / "configs" / "earthmoving_benchmark.json"))
    parser.add_argument("--output-dir", default=str(ROOT / "outputs" / "earthmoving_replay"))
    args = parser.parse_args()

    bundle = build_earthmoving_replay_bundle(
        config_path=args.config,
        scenario_name=args.scenario,
        output_dir=args.output_dir,
    )
    print(f"Wrote earthmoving replay for {bundle['scenario']} with {len(bundle['debug_hypotheses'])} hypotheses")


if __name__ == "__main__":
    main()
