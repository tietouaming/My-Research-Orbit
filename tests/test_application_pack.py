from pathlib import Path

from research_orbit.application_pack import generate_application_pack


def test_generate_application_pack_writes_expected_files(tmp_path: Path) -> None:
    pack = generate_application_pack(target="mimo-orbit", output_dir=tmp_path)
    names = {path.name for path in pack.files}
    assert "01_project_summary.md" in names
    assert "06_application_form_draft.md" in names
    assert all(path.exists() for path in pack.files)
    content = (tmp_path / "01_project_summary.md").read_text(encoding="utf-8")
    assert "不得提交 GitHub" in content
