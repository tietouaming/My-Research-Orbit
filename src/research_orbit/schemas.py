"""Typed data models used by Research Orbit."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field


def default_created_at() -> datetime:
    fixed = os.environ.get("RESEARCH_ORBIT_FIXED_CREATED_AT")
    if fixed:
        normalized = fixed.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized)
    return datetime.now(timezone.utc)


class MemoryCard(BaseModel):
    title: str
    source_path: str
    category: str
    problem: str
    solution: str
    reusable_rule: str
    risk_level: Literal["low", "medium", "high"]
    verification_status: str
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=default_created_at)


class WorkflowStep(BaseModel):
    id: str
    title: str
    instruction: str
    expected_evidence: list[str] = Field(default_factory=list)


class WorkflowSpec(BaseModel):
    name: str
    version: str
    description: str
    intended_user: str
    inputs: list[str]
    outputs: list[str]
    tools: list[str]
    steps: list[WorkflowStep]
    safety_rules: list[str]
    success_criteria: list[str]
    context_usage_pattern: str
    provider_requirements: list[str]
    evidence_materials: list[str]


class ApplicationPack(BaseModel):
    target: str
    output_dir: Path
    files: list[Path]
    created_at: datetime = Field(default_factory=default_created_at)


class RedactionFinding(BaseModel):
    source_path: str
    line_number: int
    finding_type: str
    severity: Literal["low", "medium", "high"]
    message: str
    excerpt: str


class ProviderCapability(BaseModel):
    name: str
    description: str
    requires_network: bool = False


class ProviderConfig(BaseModel):
    name: str
    configured: bool
    required_env: list[str] = Field(default_factory=list)
    optional_env: list[str] = Field(default_factory=list)
    api_key_present: bool = False
    api_base_url_present: bool = False
    model_present: bool = False
    capability: str
    notes: str = ""


class ProviderRequest(BaseModel):
    system_prompt: str
    user_prompt: str
    temperature: float = 0.2
    max_tokens: int = 1200
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProviderResponse(BaseModel):
    provider: str
    model: str
    content: str
    used_dry_run: bool = False
    warnings: list[str] = Field(default_factory=list)
    raw: dict[str, Any] | None = None
