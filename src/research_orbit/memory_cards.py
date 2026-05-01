"""Memory card generation for scientific operation notes."""

from __future__ import annotations

import json
import re
from pathlib import Path

from research_orbit.schemas import MemoryCard

SUPPORTED_INPUT_SUFFIXES = {".md", ".txt", ".log"}

CATEGORY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "word_mathtype": ("word", "mathtype", "equation", "formula", "revision", "ooxml"),
    "comsol_mph": ("comsol", ".mph", "dmodel.xml", "weak form", "mesh", "xmesh"),
    "simulation_porting": ("fenicsx", "moose", "porting", "migration", "solver", "t=0"),
    "run_log_diagnosis": ("traceback", "error", "failed", "log", "exception", "ci"),
    "multi_machine_memory": ("multi-machine", "another computer", "archive", "merge", "machine"),
    "security_redaction": ("redaction", "secret", "token", "password", "private", "sensitive"),
    "application_pack": ("application", "creator program", "grant", "proof material", "pack"),
}


def collect_input_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if _is_ignored(child):
                    continue
                if child.is_file() and child.suffix.lower() in SUPPORTED_INPUT_SUFFIXES:
                    files.append(child)
        elif path.is_file() and path.suffix.lower() in SUPPORTED_INPUT_SUFFIXES:
            files.append(path)
    return files


def build_memory_cards(paths: list[Path]) -> list[MemoryCard]:
    cards: list[MemoryCard] = []
    for path in collect_input_files(paths):
        text = path.read_text(encoding="utf-8")
        cards.append(build_memory_card(path, text))
    return cards


def build_memory_card(path: Path, text: str) -> MemoryCard:
    category = infer_category(text, path)
    return MemoryCard(
        title=extract_title(text, path),
        source_path=path.as_posix(),
        category=category,
        problem=extract_problem(text),
        solution=extract_solution(text, category),
        reusable_rule=extract_reusable_rule(text, category),
        risk_level=infer_risk_level(text),
        verification_status=infer_verification_status(text),
        tags=infer_tags(text, category),
    )


def write_cards(cards: list[MemoryCard], output: Path, output_format: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output_format == "jsonl":
        with output.open("w", encoding="utf-8") as handle:
            for card in cards:
                handle.write(card.model_dump_json() + "\n")
        return
    if output_format == "md":
        output.write_text(render_cards_markdown(cards), encoding="utf-8")
        return
    raise ValueError("format must be one of: jsonl, md")


def render_cards_markdown(cards: list[MemoryCard]) -> str:
    lines = ["# Research Orbit Memory Cards", ""]
    for card in cards:
        lines.extend(
            [
                f"## {card.title}",
                "",
                f"- source_path: `{card.source_path}`",
                f"- category: `{card.category}`",
                f"- risk_level: `{card.risk_level}`",
                f"- verification_status: `{card.verification_status}`",
                f"- tags: {', '.join(card.tags)}",
                "",
                "### Problem",
                card.problem,
                "",
                "### Solution",
                card.solution,
                "",
                "### Reusable Rule",
                card.reusable_rule,
                "",
            ]
        )
    return "\n".join(lines)


def infer_category(text: str, path: Path) -> str:
    lowered = f"{path.name}\n{text}".lower()
    scores = {
        category: sum(1 for keyword in keywords if keyword in lowered)
        for category, keywords in CATEGORY_KEYWORDS.items()
    }
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "multi_machine_memory"


def extract_title(text: str, path: Path) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()[:120]
        if stripped:
            return stripped[:120]
    return path.stem.replace("_", " ").replace("-", " ").title()


def extract_problem(text: str) -> str:
    return _extract_labeled_block(
        text,
        ("problem", "issue", "risk", "error"),
    ) or _first_sentences(text)


def extract_solution(text: str, category: str) -> str:
    explicit = _extract_labeled_block(text, ("solution", "action", "fix", "resolution"))
    if explicit:
        return explicit
    defaults = {
        "word_mathtype": (
            "Back up the document, use tracked revisions for prose, and preserve formula "
            "object boundaries."
        ),
        "comsol_mph": (
            "Use structured extraction and preserve original expressions before making "
            "any model claim."
        ),
        "simulation_porting": (
            "Validate t=0 fields first, then run short smoke tests before long transient "
            "analysis."
        ),
        "run_log_diagnosis": (
            "Separate evidence from hypotheses and rank the next checks by reversibility "
            "and impact."
        ),
        "security_redaction": (
            "Audit locally, remove secrets and large/private files, then review before "
            "publishing."
        ),
        "application_pack": (
            "Generate application material locally and manually review it before any "
            "external submission."
        ),
    }
    return defaults.get(
        category,
        "Convert the observed operation into a small, auditable, reusable workflow rule.",
    )


def extract_reusable_rule(text: str, category: str) -> str:
    explicit = _extract_labeled_block(text, ("rule", "reusable rule", "lesson"))
    if explicit:
        return explicit
    rules = {
        "word_mathtype": (
            "Never treat MathType or equation objects as normal text; require backup "
            "and revision audit."
        ),
        "comsol_mph": (
            "Do not hand-copy COMSOL formulas from memory; route through a structured "
            "intermediate layer."
        ),
        "simulation_porting": "Make t=0 whole-field agreement the first migration gate.",
        "run_log_diagnosis": (
            "Every diagnosis must list evidence, likely causes, check order, and unknowns."
        ),
        "multi_machine_memory": (
            "Each machine writes additive notes; consolidation happens by review, "
            "not overwrite."
        ),
        "security_redaction": (
            "Public visibility is not permission, and sensitive files stay outside Git."
        ),
        "application_pack": "Application packs are generated into ignored local directories only.",
    }
    return rules.get(category, "Keep the operation reproducible, reversible, and source-linked.")


def infer_risk_level(text: str) -> str:
    lowered = text.lower()
    high_risk_words = ("secret", "token", "password", ".mph", "overwrite", "api key")
    if any(word in lowered for word in high_risk_words):
        return "high"
    if any(word in lowered for word in ("error", "failed", "warning", "risk", "unstable")):
        return "medium"
    return "low"


def infer_verification_status(text: str) -> str:
    lowered = text.lower()
    if any(word in lowered for word in ("verified", "validated", "passed", "confirmed")):
        return "verified"
    if any(word in lowered for word in ("todo", "open", "unverified", "unknown")):
        return "needs_review"
    return "draft"


def infer_tags(text: str, category: str) -> list[str]:
    lowered = text.lower()
    tags = {category}
    for keyword in (
        "backup",
        "revision",
        "mathtype",
        "comsol",
        "workflow",
        "solver",
        "redaction",
        "provider",
        "dry-run",
        "multi-machine",
    ):
        if keyword in lowered:
            tags.add(keyword)
    return sorted(tags)


def _extract_labeled_block(text: str, labels: tuple[str, ...]) -> str:
    pattern = re.compile(
        rf"(?im)^\s*(?:#+\s*)?(?:{'|'.join(re.escape(label) for label in labels)})\s*:?\s*(.+)$"
    )
    match = pattern.search(text)
    if match:
        return match.group(1).strip()[:700]
    return ""


def _first_sentences(text: str) -> str:
    clean = " ".join(_clean_markup_prefix(line) for line in text.splitlines() if line.strip())
    return clean[:700] if clean else "No problem statement was found in the source note."


def _clean_markup_prefix(line: str) -> str:
    stripped = line.rstrip()
    while stripped[:1] in {"#", "-", " ", "*", "`"}:
        stripped = stripped[1:]
    return stripped


def _is_ignored(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}
    return bool(parts & {".git", ".local_private", "__pycache__", ".pytest_cache", ".ruff_cache"})


def cards_to_json(cards: list[MemoryCard]) -> str:
    return json.dumps([card.model_dump(mode="json") for card in cards], indent=2)
