"""Anthropic provider placeholder with explicit non-fake behavior."""

from __future__ import annotations

from research_orbit.providers.base import BaseProvider, ProviderUnsupportedError
from research_orbit.schemas import ProviderRequest, ProviderResponse


class AnthropicProvider(BaseProvider):
    name = "anthropic"

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        raise ProviderUnsupportedError(
            "Anthropic live transport is not implemented yet. Configure dry-run for CI, "
            "or add a tested Anthropic Messages API transport before enabling live calls."
        )
