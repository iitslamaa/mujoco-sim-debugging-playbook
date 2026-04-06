from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.plot import plot_sweep_results


def main() -> None:
    summary_path = ROOT / "outputs" / "interesting_sweeps" / "combined_summary.json"
    rows = json.loads(summary_path.read_text())
    plot_sweep_results(rows, summary_path.parent)
    print(f"Plots refreshed in {summary_path.parent}")


if __name__ == "__main__":
    main()

