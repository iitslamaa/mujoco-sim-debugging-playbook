import json

from mujoco_sim_debugging_playbook.repro_bundle_index import build_repro_bundle_index


def test_repro_bundle_index_maps_cases_to_bundle(tmp_path):
    repro = tmp_path / "repro.json"
    bundle = tmp_path / "bundle.json"
    repro.write_text(json.dumps({"cases": [{"case_id": "delay_instability", "title": "delay instability"}]}))
    bundle.write_text(json.dumps({"summary": {"bundle": "abc123", "file_count": 6}}))
    payload = build_repro_bundle_index(
        repro_inventory_path=repro,
        debug_bundle_manifest_path=bundle,
        output_dir=tmp_path,
    )
    assert payload["summary"]["entry_count"] == 1
