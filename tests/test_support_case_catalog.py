from mujoco_sim_debugging_playbook.support_case_catalog import build_support_case_catalog


def test_support_case_catalog_extracts_titles(tmp_path):
    d = tmp_path / "cases"
    d.mkdir()
    (d / "alpha.md").write_text("# Alpha\nbody")
    payload = build_support_case_catalog(support_cases_dir=d, output_dir=tmp_path)
    assert payload["cases"][0]["title"] == "Alpha"
