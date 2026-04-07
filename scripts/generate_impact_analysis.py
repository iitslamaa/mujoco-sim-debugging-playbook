from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.impact_analysis import write_impact_analysis


def main() -> None:
    payload = write_impact_analysis(
        dependency_map_path=ROOT / "outputs" / "dependency_map" / "dependency_map.json",
        output_dir=ROOT / "outputs" / "impact_analysis",
    )
    print(f"Impact analysis written to {ROOT / 'outputs' / 'impact_analysis'}")
    print("Dependencies tracked:", payload["summary"]["dependency_count"])


if __name__ == "__main__":
    main()
