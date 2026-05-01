"""Provider registry and environment configuration."""

from __future__ import annotations

from dataclasses import dataclass

from research_orbit.config import getenv
from research_orbit.providers.anthropic_provider import AnthropicProvider
from research_orbit.providers.base import BaseProvider
from research_orbit.providers.dry_run import DryRunProvider
from research_orbit.providers.gemini_provider import GeminiProvider
from research_orbit.providers.openai_compatible import OpenAICompatibleProvider
from research_orbit.providers.openai_provider import OpenAIProvider
from research_orbit.schemas import ProviderConfig


@dataclass(frozen=True)
class ProviderEnv:
    name: str
    required_env: tuple[str, ...]
    optional_env: tuple[str, ...]
    capability: str
    notes: str
    kind: str
    base_env: str | None = None
    key_env: str | None = None
    model_env: str | None = None


PROVIDER_ENVS: dict[str, ProviderEnv] = {
    "dry-run": ProviderEnv(
        name="dry-run",
        required_env=(),
        optional_env=("RESEARCH_ORBIT_PROVIDER",),
        capability="Deterministic local template generation.",
        notes="Default mode for tests, CI, and no-key environments.",
        kind="dry-run",
    ),
    "openai": ProviderEnv(
        name="openai",
        required_env=("OPENAI_API_KEY", "OPENAI_MODEL"),
        optional_env=("OPENAI_API_BASE_URL",),
        capability="OpenAI Chat Completions transport.",
        notes="Uses the official API base by default; no key is printed.",
        kind="openai",
        base_env="OPENAI_API_BASE_URL",
        key_env="OPENAI_API_KEY",
        model_env="OPENAI_MODEL",
    ),
    "openai-compatible": ProviderEnv(
        name="openai-compatible",
        required_env=(
            "RESEARCH_ORBIT_API_BASE_URL",
            "RESEARCH_ORBIT_API_KEY",
            "RESEARCH_ORBIT_MODEL",
        ),
        optional_env=(),
        capability="Generic OpenAI-compatible Chat Completions transport.",
        notes="Use for gateways and compatible providers when base URL is known.",
        kind="compatible",
        base_env="RESEARCH_ORBIT_API_BASE_URL",
        key_env="RESEARCH_ORBIT_API_KEY",
        model_env="RESEARCH_ORBIT_MODEL",
    ),
    "anthropic": ProviderEnv(
        name="anthropic",
        required_env=("ANTHROPIC_API_KEY", "ANTHROPIC_MODEL"),
        optional_env=(),
        capability="Claude adapter interface.",
        notes="Live transport is intentionally not implemented yet.",
        kind="anthropic",
        key_env="ANTHROPIC_API_KEY",
        model_env="ANTHROPIC_MODEL",
    ),
    "gemini": ProviderEnv(
        name="gemini",
        required_env=("GEMINI_API_KEY", "GEMINI_MODEL"),
        optional_env=(),
        capability="Gemini adapter interface.",
        notes="Live transport is intentionally not implemented yet.",
        kind="gemini",
        key_env="GEMINI_API_KEY",
        model_env="GEMINI_MODEL",
    ),
    "zhipu": ProviderEnv(
        name="zhipu",
        required_env=("ZHIPU_API_KEY", "ZHIPU_MODEL"),
        optional_env=("ZHIPU_API_BASE_URL", "RESEARCH_ORBIT_API_BASE_URL"),
        capability="GLM via OpenAI-compatible endpoint when configured.",
        notes="Requires a user supplied compatible base URL; no unverified endpoint is hardcoded.",
        kind="compatible",
        base_env="ZHIPU_API_BASE_URL",
        key_env="ZHIPU_API_KEY",
        model_env="ZHIPU_MODEL",
    ),
    "minimax": ProviderEnv(
        name="minimax",
        required_env=("MINIMAX_API_KEY", "MINIMAX_MODEL"),
        optional_env=("MINIMAX_API_BASE_URL", "RESEARCH_ORBIT_API_BASE_URL"),
        capability="MiniMax via OpenAI-compatible endpoint when configured.",
        notes="Requires a user supplied compatible base URL; no unverified endpoint is hardcoded.",
        kind="compatible",
        base_env="MINIMAX_API_BASE_URL",
        key_env="MINIMAX_API_KEY",
        model_env="MINIMAX_MODEL",
    ),
    "kimi": ProviderEnv(
        name="kimi",
        required_env=("KIMI_API_KEY", "KIMI_MODEL"),
        optional_env=("KIMI_API_BASE_URL", "RESEARCH_ORBIT_API_BASE_URL"),
        capability="Moonshot Kimi via OpenAI-compatible endpoint when configured.",
        notes="Requires a user supplied compatible base URL; no unverified endpoint is hardcoded.",
        kind="compatible",
        base_env="KIMI_API_BASE_URL",
        key_env="KIMI_API_KEY",
        model_env="KIMI_MODEL",
    ),
    "mimo": ProviderEnv(
        name="mimo",
        required_env=("MIMO_API_BASE_URL", "MIMO_API_KEY", "MIMO_MODEL"),
        optional_env=(),
        capability="Xiaomi MiMo via OpenAI-compatible endpoint when configured.",
        notes="Listed as one provider option, not as the public project focus.",
        kind="compatible",
        base_env="MIMO_API_BASE_URL",
        key_env="MIMO_API_KEY",
        model_env="MIMO_MODEL",
    ),
    "deepseek": ProviderEnv(
        name="deepseek",
        required_env=("DEEPSEEK_API_KEY", "DEEPSEEK_MODEL"),
        optional_env=("DEEPSEEK_API_BASE_URL", "RESEARCH_ORBIT_API_BASE_URL"),
        capability="DeepSeek via OpenAI-compatible endpoint when configured.",
        notes=(
            "Requires a user supplied compatible base URL if the environment does not "
            "define one."
        ),
        kind="compatible",
        base_env="DEEPSEEK_API_BASE_URL",
        key_env="DEEPSEEK_API_KEY",
        model_env="DEEPSEEK_MODEL",
    ),
}


def list_provider_configs() -> list[ProviderConfig]:
    return [provider_config(name) for name in PROVIDER_ENVS]


def provider_config(name: str) -> ProviderConfig:
    spec = PROVIDER_ENVS[name]
    api_key_present = bool(spec.key_env and getenv(spec.key_env))
    model_present = bool(spec.model_env and getenv(spec.model_env))
    base_present = bool(_base_url_for(spec))
    if name == "dry-run":
        configured = True
    elif spec.kind in {"compatible", "openai"}:
        if name == "openai":
            configured = api_key_present and model_present
        else:
            configured = api_key_present and model_present and base_present
    else:
        configured = all(getenv(env) for env in spec.required_env)
    return ProviderConfig(
        name=name,
        configured=configured,
        required_env=list(spec.required_env),
        optional_env=list(spec.optional_env),
        api_key_present=api_key_present,
        api_base_url_present=base_present,
        model_present=model_present,
        capability=spec.capability,
        notes=spec.notes,
    )


def get_provider_from_env(name: str | None = None) -> BaseProvider:
    selected = name or getenv("RESEARCH_ORBIT_PROVIDER", "dry-run") or "dry-run"
    if selected not in PROVIDER_ENVS:
        known = ", ".join(PROVIDER_ENVS)
        raise ValueError(f"Unknown provider `{selected}`. Known providers: {known}")
    config = provider_config(selected)
    spec = PROVIDER_ENVS[selected]
    if selected == "dry-run":
        return DryRunProvider(config)
    if selected == "openai":
        return OpenAIProvider(
            name="openai",
            api_base_url=getenv("OPENAI_API_BASE_URL", "https://api.openai.com/v1"),
            api_key=getenv("OPENAI_API_KEY"),
            model=getenv("OPENAI_MODEL"),
            config=config,
        )
    if spec.kind == "compatible":
        return OpenAICompatibleProvider(
            name=selected,
            api_base_url=_base_url_for(spec),
            api_key=getenv(spec.key_env or ""),
            model=getenv(spec.model_env or ""),
            config=config,
        )
    if selected == "anthropic":
        return AnthropicProvider(config)
    if selected == "gemini":
        return GeminiProvider(config)
    raise ValueError(f"Provider `{selected}` is registered but has no adapter.")


def _base_url_for(spec: ProviderEnv) -> str | None:
    if spec.base_env:
        return getenv(spec.base_env) or getenv("RESEARCH_ORBIT_API_BASE_URL")
    return getenv("RESEARCH_ORBIT_API_BASE_URL")
