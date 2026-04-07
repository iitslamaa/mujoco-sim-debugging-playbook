import json

from mujoco_sim_debugging_playbook.impact_analysis import build_impact_analysis


def test_impact_analysis_builds_reverse_dependency_view(tmp_path):
    dependency_map = tmp_path / "dependency_map.json"
    dependency_map.write_text(
        json.dumps(
            {
                "rows": [
                    {"artifact": "a", "dependencies": ["x", "y"]},
                    {"artifact": "b", "dependencies": ["x"]},
                ]
            }
        )
    )
    payload = build_impact_analysis(dependency_map_path=dependency_map)
    assert payload["summary"]["most_impactful_dependency"] == "x"
    assert payload["summary"]["max_impact_count"] == 2
