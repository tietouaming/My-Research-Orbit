"""OpenAI-compatible chat completions provider."""

from __future__ import annotations

import httpx

from research_orbit.providers.base import (
    BaseProvider,
    ProviderNotConfiguredError,
)
from research_orbit.schemas import ProviderRequest, ProviderResponse


class OpenAICompatibleProvider(BaseProvider):
    name = "openai-compatible"

    def __init__(
        self,
        *,
        name: str,
        api_base_url: str | None,
        api_key: str | None,
        model: str | None,
        config,
    ) -> None:
        super().__init__(config)
        self.name = name
        self.api_base_url = api_base_url
        self.api_key = api_key
        self.model = model

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        if not self.api_base_url or not self.api_key or not self.model:
            raise ProviderNotConfiguredError(
                f"{self.name} requires api base URL, API key, and model environment variables."
            )
        endpoint = self._chat_completions_url(self.api_base_url)
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_prompt},
            ],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        with httpx.Client(timeout=60) as client:
            response = client.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return ProviderResponse(
            provider=self.name,
            model=self.model,
            content=content,
            raw={"id": data.get("id"), "usage": data.get("usage")},
        )

    @staticmethod
    def _chat_completions_url(base_url: str) -> str:
        clean = base_url.rstrip("/")
        if clean.endswith("/chat/completions"):
            return clean
        return f"{clean}/chat/completions"
