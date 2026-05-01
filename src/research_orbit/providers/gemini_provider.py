"""Gemini provider placeholder with explicit non-fake behavior."""

from __future__ import annotations

from research_orbit.providers.base import BaseProvider, ProviderUnsupportedError
from research_orbit.schemas import ProviderRequest, ProviderResponse


class GeminiProvider(BaseProvider):
    name = "gemini"

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        raise ProviderUnsupportedError(
            "Gemini live transport is not implemented yet. Configure dry-run for CI, "
            "or add a tested Gemini transport before enabling live calls."
        )
