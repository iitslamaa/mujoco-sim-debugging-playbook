from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.support import run_support_case


def test_run_support_case_generates_markdown(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    cases_dir = repo / "cases" / "issue_cases"
    outputs_dir = repo / "outputs" / "interesting_sweeps"
    cases_dir.mkdir(parents=True)
    outputs_dir.mkdir(parents=True)

    (cases_dir / "demo.json").write_text(
        json.dumps(
            {
                "slug": "demo",
                "title": "Demo",
                "summary": "Demo summary",
                "user_report": "Demo report",
                "reproduction_command": "python demo.py",
                "parameter_of_interest": "actuator_gain",
                "recommended_checks": ["check one"],
                "recommended_response_points": ["reply one"]
            }
        )
    )
    (outputs_dir / "combined_summary.json").write_text(
        json.dumps(
            [
                {
                    "parameter": "actuator_gain",
                    "value": 10,
                    "success_rate": 0.9,
                    "final_error_mean": 0.01,
                    "max_overshoot_mean": 0.02,
                    "oscillation_index_mean": 0.1
                },
                {
                    "parameter": "actuator_gain",
                    "value": 20,
                    "success_rate": 0.4,
                    "final_error_mean": 0.05,
                    "max_overshoot_mean": 0.3,
                    "oscillation_index_mean": 0.7
                }
            ]
        )
    )

    output_path = run_support_case("demo", repo)
    content = output_path.read_text()
    assert "Suggested support response" in content
    assert "Best success rate" in content
