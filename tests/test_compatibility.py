import json

from mujoco_sim_debugging_playbook.compatibility import build_compatibility_report


def test_compatibility_report_warns_when_optional_tools_missing(tmp_path):
    environment_path = tmp_path / "environment.json"
    environment_path.write_text(
        json.dumps(
            {
                "platform": {"python_version": "3.10.14"},
                "runtime": {"mujoco_version": "3.2.7"},
                "tooling": {"docker_version": None, "gh_version": None},
            }
        )
    )

    payload = build_compatibility_report(
        environment_report_path=environment_path,
        output_dir=tmp_path,
    )

    assert payload["summary"]["status"] == "warn"
    assert payload["summary"]["warn_count"] == 2
