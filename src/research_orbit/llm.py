"""LLM facade used by workflow runners."""

from __future__ import annotations

from research_orbit.providers.provider_registry import get_provider_from_env
from research_orbit.schemas import ProviderRequest, ProviderResponse


def generate_with_provider(
    *,
    provider_name: str | None,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 1200,
) -> ProviderResponse:
    provider = get_provider_from_env(provider_name)
    request = ProviderRequest(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=max_tokens,
    )
    return provider.generate(request)
