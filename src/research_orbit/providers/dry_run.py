"""Deterministic provider for tests, CI, and offline use."""

from __future__ import annotations

import hashlib

from research_orbit.providers.base import BaseProvider
from research_orbit.schemas import ProviderRequest, ProviderResponse


class DryRunProvider(BaseProvider):
    name = "dry-run"

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        digest = hashlib.sha256(
            f"{request.system_prompt}\n---\n{request.user_prompt}".encode()
        ).hexdigest()[:12]
        content = (
            "Dry-run provider response\n\n"
            f"- fingerprint: `{digest}`\n"
            "- external_api_call: false\n"
            "- result: The workflow prompt was rendered and can be inspected safely.\n"
            "- next_step: Replace `RESEARCH_ORBIT_PROVIDER` only when a real provider is "
            "explicitly configured."
        )
        return ProviderResponse(
            provider=self.name,
            model="deterministic-template",
            content=content,
            used_dry_run=True,
        )
