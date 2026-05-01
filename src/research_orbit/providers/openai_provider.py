"""OpenAI provider adapter."""

from __future__ import annotations

from research_orbit.providers.openai_compatible import OpenAICompatibleProvider


class OpenAIProvider(OpenAICompatibleProvider):
    """OpenAI Chat Completions adapter using OPENAI_* environment variables."""
