from pathlib import Path

from research_orbit.memory_cards import build_memory_card, build_memory_cards


def test_build_memory_card_classifies_word_mathtype() -> None:
    card = build_memory_card(
        Path("note.md"),
        "# Word Note\nProblem: MathType formula edit.\nAction: backup and tracked revision.",
    )
    assert card.category == "word_mathtype"
    assert "MathType" in card.problem
    assert "word_mathtype" in card.tags


def test_build_memory_cards_reads_directory(tmp_path: Path) -> None:
    note = tmp_path / "run.log"
    note.write_text("Error: solver failed\nAction: inspect first failing line", encoding="utf-8")
    cards = build_memory_cards([tmp_path])
    assert len(cards) == 1
    assert cards[0].category == "run_log_diagnosis"


def test_memory_card_created_at_can_be_fixed(monkeypatch) -> None:
    monkeypatch.setenv("RESEARCH_ORBIT_FIXED_CREATED_AT", "2026-05-01T00:00:00Z")
    card = build_memory_card(Path("note.md"), "Problem: stable output")
    assert card.created_at.isoformat() == "2026-05-01T00:00:00+00:00"


def test_memory_card_source_path_uses_posix_style() -> None:
    card = build_memory_card(Path("examples") / "sample_operation_log.md", "Problem: path")
    assert card.source_path == "examples/sample_operation_log.md"
