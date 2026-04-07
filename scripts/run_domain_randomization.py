from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.generalization import run_domain_randomization


def main() -> None:
    parser = argparse.ArgumentParser(description="Run domain-randomization robustness evaluation across controllers.")
    parser.add_argument("--config", default=str(ROOT / "configs" / "domain_randomization.json"))
    parser.add_argument("--torch-checkpoint", default=str(ROOT / "outputs" / "learning" / "training" / "policy.pt"))
    parser.add_argument("--rl-checkpoint", default=str(ROOT / "outputs" / "rl" / "training" / "reinforce_policy.pt"))
    args = parser.parse_args()

    result = run_domain_randomization(args.config, args.torch_checkpoint, args.rl_checkpoint)
    print(f"Domain randomization report written to {result['output_dir']}")


if __name__ == "__main__":
    main()

