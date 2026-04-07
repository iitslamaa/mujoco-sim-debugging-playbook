import json

from mujoco_sim_debugging_playbook.dependency_snapshot import build_dependency_snapshot


def test_dependency_snapshot_reads_pip_freeze(tmp_path):
    environment_path = tmp_path / "environment.json"
    environment_path.write_text(
        json.dumps(
            {
                "platform": {"python_version": "3.10.14"},
                "workspace": {"pip_freeze": ["numpy==1.0.0", "mujoco==3.2.7"]},
            }
        )
    )

    payload = build_dependency_snapshot(
        environment_report_path=environment_path,
        output_dir=tmp_path,
    )

    assert payload["summary"]["package_count"] == 2
    assert payload["packages"][0] == "numpy==1.0.0"
