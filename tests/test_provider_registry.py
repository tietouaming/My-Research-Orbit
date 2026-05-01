from research_orbit.providers.provider_registry import get_provider_from_env, list_provider_configs
from research_orbit.schemas import ProviderRequest


def test_dry_run_provider_is_default(monkeypatch) -> None:
    monkeypatch.delenv("RESEARCH_ORBIT_PROVIDER", raising=False)
    provider = get_provider_from_env()
    response = provider.generate(ProviderRequest(system_prompt="sys", user_prompt="user"))
    assert response.used_dry_run is True
    assert response.provider == "dry-run"


def test_provider_configs_do_not_expose_key_values(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "placeholder-provider-value")
    monkeypatch.setenv("OPENAI_MODEL", "configured-model")
    configs = {config.name: config for config in list_provider_configs()}
    assert configs["openai"].api_key_present is True
    rendered = "\n".join(config.model_dump_json() for config in configs.values())
    assert "placeholder-provider-value" not in rendered
