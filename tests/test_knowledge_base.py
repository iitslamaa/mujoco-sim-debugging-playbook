from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.knowledge_base import build_knowledge_base


def test_build_knowledge_base(tmp_path: Path) -> None:
    incidents = tmp_path / "index.json"
    incidents.write_text(json.dumps({
        "bundles": [
            {
                "id": "INC-001",
                "target": "episode 1",
                "kind": "randomized_episode",
                "summary": "Hard randomized episode.",
                "evidence": "delay 5",
                "next_action": "Reduce delay."
            }
        ]
    }))
    recommendations = tmp_path / "recommendations.json"
    recommendations.write_text(json.dumps({
        "recommendations": [
            {"target": "episode 1", "recommendation": "Reduce delay.", "tradeoff": "More compute.", "evidence": "delay evidence"}
        ]
    }))
    output_dir = tmp_path / "kb"
    payload = build_knowledge_base(
        incidents_index_path=incidents,
        recommendations_path=recommendations,
        output_dir=output_dir,
    )
    assert payload["summary"]["count"] == 1
    assert (output_dir / "index.md").exists()
