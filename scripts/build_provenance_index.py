from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.provenance import build_provenance_index


def main() -> None:
    manifest_paths = sorted((ROOT / "outputs").glob("**/manifest.json"))
    payload = build_provenance_index(
        repo_root=ROOT,
        manifest_paths=manifest_paths,
        output_dir=ROOT / "outputs" / "provenance",
    )
    print(f"Provenance index written with {payload['summary']['manifest_count']} manifests")


if __name__ == "__main__":
    main()
