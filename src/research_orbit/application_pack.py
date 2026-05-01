"""Local private application pack generator."""

from __future__ import annotations

from pathlib import Path

from research_orbit.config import DEFAULT_APPLICATION_PACK_DIR
from research_orbit.schemas import ApplicationPack

SUPPORTED_TARGETS = {"mimo-orbit", "general-creator-program", "research-tool-grant"}


def generate_application_pack(
    target: str = "general-creator-program",
    output_dir: Path | None = None,
) -> ApplicationPack:
    if target not in SUPPORTED_TARGETS:
        known = ", ".join(sorted(SUPPORTED_TARGETS))
        raise ValueError(f"Unknown target `{target}`. Known targets: {known}")
    destination = output_dir or DEFAULT_APPLICATION_PACK_DIR
    destination.mkdir(parents=True, exist_ok=True)
    files = []
    for filename, content in _pack_files(target).items():
        path = destination / filename
        path.write_text(content, encoding="utf-8")
        files.append(path)
    return ApplicationPack(target=target, output_dir=destination, files=files)


def _pack_files(target: str) -> dict[str, str]:
    target_label = {
        "mimo-orbit": "Xiaomi MiMo Orbit creator program",
        "general-creator-program": "general AI creator program",
        "research-tool-grant": "research tool grant",
    }[target]
    private_notice = (
        "> Private local draft. Do not commit this file to GitHub. Review manually before use.\n"
    )
    return {
        "01_project_summary.md": private_notice
        + f"""
# Research Orbit Project Summary

Target: {target_label}

Research Orbit is an Agentic Research OS for turning daily scientific AI collaboration
into reusable workflows. It focuses on long-context research memory, document editing
safety, COMSOL model audit, simulation migration review, run-log diagnosis, provider
adaptation, redaction, and local evidence packaging.

This draft is intentionally local and should be edited before submission.
""".lstrip(),
        "02_technical_architecture.md": private_notice
        + """
# Technical Architecture

The public project contains a Python package, Typer CLI, Pydantic schemas, YAML workflow
specifications, local redaction checks, deterministic dry-run execution, and a provider
registry for OpenAI, OpenAI-compatible endpoints, Claude, Gemini, GLM, MiniMax, Kimi,
MiMo, and DeepSeek configuration paths.

The architecture separates public reusable workflow code from private application drafts.
""".lstrip(),
        "03_context_and_token_usage_plan.md": private_notice
        + """
# Context And Token Usage Plan

Long-context use cases include reading multi-document research memory, planning safe
Word/MathType edits, comparing COMSOL-derived model summaries, reviewing solver migration
evidence, diagnosing logs, merging multi-machine notes, and drafting local-only application
materials.

The public repository keeps this provider-neutral. Any target-specific claim should be
checked against the target program's current application rules before submission.
""".lstrip(),
        "04_github_proof_materials.md": private_notice
        + """
# GitHub Proof Materials

Suggested public proof points:

- runnable package under `projects/research-orbit/`
- CLI smoke commands in the README
- workflow YAML files
- tests and CI
- provider abstraction with dry-run default
- local private application pack generator
- security and redaction documentation

Do not include raw private logs, unredacted paths, secrets, `.mph` files, or generated
application pack contents.
""".lstrip(),
        "05_roadmap.md": private_notice
        + """
# Roadmap

Near-term work: add more workflow examples, improve memory-card extraction, add verified
provider transports, and expand evaluation fixtures.

Medium-term work: add structured COMSOL intermediate schema readers, richer Word/MathType
planning checks, and multi-machine memory merge reports.

Long-term work: create a full local research operations dashboard and reproducible
evaluation suite.
""".lstrip(),
        "06_application_form_draft.md": private_notice
        + f"""
# Application Form Draft

Target: {target_label}

Applicant should manually complete:

- project motivation
- personal eligibility
- model/provider usage claims
- evidence links
- privacy review
- authorization and consent statements

This file is a drafting scaffold, not a final application.
""".lstrip(),
    }
