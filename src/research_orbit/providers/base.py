"""Provider interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from research_orbit.schemas import ProviderConfig, ProviderRequest, ProviderResponse


class ProviderError(RuntimeError):
    """Base class for provider failures."""


class ProviderNotConfiguredError(ProviderError):
    """Raised when a real provider is requested without required environment."""


class ProviderUnsupportedError(ProviderError):
    """Raised when a provider adapter is intentionally not wired for live calls."""


class BaseProvider(ABC):
    name: str

    def __init__(self, config: ProviderConfig) -> None:
        self.config = config

    @abstractmethod
    def generate(self, request: ProviderRequest) -> ProviderResponse:
        """Generate a response for a workflow prompt."""
