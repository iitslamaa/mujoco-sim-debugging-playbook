from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.bedrock_packet import build_bedrock_packet


if __name__ == "__main__":
    payload = build_bedrock_packet(
        repo_root=ROOT,
        output_dir=ROOT / "outputs" / "bedrock_packet",
        root_packet_path=ROOT / "BEDROCK_SIMULATION_PACKET.md",
    )
    print(f"Wrote Bedrock packet with {payload['metrics']['scale_episode_count']} scale episodes")
