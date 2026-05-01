from research_orbit.ui_server import UI_ASSET_DIR, _resolve_asset, build_ui_state


def test_build_ui_state_contains_public_project_data() -> None:
    state = build_ui_state()
    assert state["project"]["name"] == "Research Orbit"
    assert state["summary"]["workflow_count"] >= 6
    assert state["summary"]["provider_count"] >= 8
    assert state["summary"]["memory_card_count"] >= 1


def test_ui_assets_are_served_safely() -> None:
    assert (UI_ASSET_DIR / "index.html").exists()
    assert _resolve_asset("/") == UI_ASSET_DIR / "index.html"
    assert _resolve_asset("/../pyproject.toml") is None
