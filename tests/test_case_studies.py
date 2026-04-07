from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mujoco_sim_debugging_playbook.case_studies import generate_case_studies


def test_generate_case_studies_from_minimal_inputs(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "outputs" / "controller_benchmark").mkdir(parents=True)
    (repo / "outputs" / "domain_randomization").mkdir(parents=True)
    (repo / "outputs" / "controller_benchmark" / "benchmark_summary.json").write_text(
        json.dumps(
            {
                "benchmark_rows": [
                    {"scenario": "baseline", "controller": "expert_pd", "success_rate": 0.8, "final_error_mean": 0.04},
                    {"scenario": "baseline", "controller": "torch_policy", "success_rate": 0.6, "final_error_mean": 0.05},
                ]
            }
        )
    )
    (repo / "outputs" / "domain_randomization" / "evaluation_rows.json").write_text(
        json.dumps(
            {
                "rows": [
                    {"controller": "expert_pd", "success": 1, "final_error": 0.04, "control_energy": 10.0},
                    {"controller": "torch_policy", "success": 0, "final_error": 0.07, "control_energy": 8.0},
                ]
            }
        )
    )
    outputs = generate_case_studies(repo)
    assert Path(outputs["markdown"]).exists()
    assert Path(outputs["image"]).exists()
