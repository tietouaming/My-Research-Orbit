"""Project validation used by the CLI and CI."""

from __future__ import annotations

from pathlib import Path

from research_orbit.config import EXAMPLES_DIR, PROJECT_ROOT, WORKFLOWS_DIR
from research_orbit.workflows import validate_workflow_files

REQUIRED_PATHS = [
    "README.md",
    "USAGE_NOTICE.md",
    "LICENSE",
    "NOTICE",
    "NOTICE.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "PRIVACY.md",
    "DISCLAIMER.md",
    "SUPPORT.md",
    "GOVERNANCE.md",
    "AUTHORS.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "pyproject.toml",
    ".gitignore",
    "src/research_orbit/cli.py",
    "src/research_orbit/schemas.py",
    "src/research_orbit/redaction.py",
    "src/research_orbit/workflows.py",
    "src/research_orbit/application_pack.py",
    "src/research_orbit/ui_server.py",
    "src/research_orbit/ui_assets/index.html",
    "src/research_orbit/ui_assets/styles.css",
    "src/research_orbit/ui_assets/app.js",
    "examples/sample_operation_log.md",
    "examples/sample_comsol_audit_note.md",
    "examples/sample_word_revision_note.md",
    "examples/sample_run_log.txt",
    "examples/sample_config.yaml",
    "docs/PROJECT_PROPOSAL.md",
    "docs/ARCHITECTURE.md",
    "docs/AGENT_WORKFLOWS.md",
    "docs/PROVIDER_ADAPTERS.md",
    "docs/ROADMAP.md",
    "docs/SECURITY_AND_REDACTION.md",
    "docs/EVALUATION_PLAN.md",
    "docs/CONTEXT_USAGE_SCENARIOS.md",
    "docs/GITHUB_PROOF_MATERIALS_GUIDE.md",
    "docs/LOCAL_APPLICATION_PACK_GUIDE.md",
]

REQUIRED_GITIGNORE_PATTERNS = [
    ".local_private/",
    "outputs/private/",
    "outputs/application_pack/",
    "*.key",
    "*.pem",
    "*.token",
    ".env",
    ".env.*",
]


def validate_project() -> list[str]:
    issues: list[str] = []
    for relative in REQUIRED_PATHS:
        path = PROJECT_ROOT / relative
        if not path.exists():
            issues.append(f"Missing required path: {relative}")
    issues.extend(validate_workflow_files())
    issues.extend(_validate_gitignore())
    issues.extend(_validate_workflow_count())
    issues.extend(_validate_public_naming())
    if not any(EXAMPLES_DIR.glob("*")):
        issues.append("Examples directory is empty.")
    return issues


def _validate_gitignore() -> list[str]:
    path = PROJECT_ROOT / ".gitignore"
    if not path.exists():
        return ["Missing project .gitignore."]
    content = path.read_text(encoding="utf-8").splitlines()
    missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in content]
    return [f".gitignore missing pattern: {pattern}" for pattern in missing]


def _validate_workflow_count() -> list[str]:
    count = len(list(WORKFLOWS_DIR.glob("*.yaml")))
    if count < 6:
        return [f"Expected at least 6 workflow YAML files, found {count}."]
    return []


def _validate_public_naming() -> list[str]:
    issues: list[str] = []
    public_docs = [PROJECT_ROOT / "README.md", *Path(PROJECT_ROOT / "docs").glob("*.md")]
    forbidden = ("MiMo Research Orbit", "MIMO Research Orbit")
    for path in public_docs:
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in content:
                issues.append(f"Forbidden public project naming `{phrase}` in {path}.")
    return issues
