import json

from mujoco_sim_debugging_playbook.bundle_coverage import build_bundle_coverage


def test_bundle_coverage_uses_quality_and_repro_index(tmp_path):
    quality = tmp_path / "quality.json"
    repro_index = tmp_path / "repro.json"
    quality.write_text(json.dumps({"summary": {"status": "pass", "evidence_hit_count": 3}}))
    repro_index.write_text(json.dumps({"summary": {"entry_count": 2}, "entries": [{"case_id": "a"}, {"case_id": "b"}]}))
    payload = build_bundle_coverage(
        bundle_quality_path=quality,
        repro_bundle_index_path=repro_index,
        output_dir=tmp_path,
    )
    assert payload["summary"]["entry_count"] == 2
