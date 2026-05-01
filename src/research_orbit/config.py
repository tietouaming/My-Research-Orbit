"""Project paths and environment helpers."""

from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = Path(__file__).resolve().parent
WORKFLOWS_DIR = PROJECT_ROOT / "workflows"
EXAMPLES_DIR = PROJECT_ROOT / "examples"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
PRIVATE_DIR = PROJECT_ROOT / ".local_private"
DEFAULT_APPLICATION_PACK_DIR = PRIVATE_DIR / "application_pack"


def getenv(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    return value


def configured(name: str) -> bool:
    return bool(getenv(name))


def ensure_output_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
