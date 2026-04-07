import json

from mujoco_sim_debugging_playbook.bundle_quality import build_bundle_quality


def test_bundle_quality_counts_high_value_files(tmp_path):
    manifest = tmp_path / "manifest.json"
    verifier = tmp_path / "verifier.json"
    manifest.write_text(
        json.dumps(
            {
                "summary": {"file_count": 4},
                "files": ["environment.json", "diagnostics.md", "baseline_summary.json", "notes.txt"],
            }
        )
    )
    verifier.write_text(json.dumps({"summary": {"status": "pass"}}))
    payload = build_bundle_quality(
        bundle_manifest_path=manifest,
        bundle_verifier_path=verifier,
        output_dir=tmp_path,
    )
    assert payload["summary"]["evidence_hit_count"] == 3
