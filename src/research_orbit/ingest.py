"""Note ingestion facade."""

from __future__ import annotations

from pathlib import Path

from research_orbit.memory_cards import build_memory_cards, write_cards
from research_orbit.schemas import MemoryCard


def ingest_notes(paths: list[Path], output: Path, output_format: str) -> list[MemoryCard]:
    cards = build_memory_cards(paths)
    write_cards(cards, output, output_format)
    return cards
