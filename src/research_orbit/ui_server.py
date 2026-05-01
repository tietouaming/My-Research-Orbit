"""Local web UI for Research Orbit."""

from __future__ import annotations

import json
import mimetypes
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from research_orbit import __version__
from research_orbit.config import (
    DEFAULT_APPLICATION_PACK_DIR,
    EXAMPLES_DIR,
    OUTPUTS_DIR,
    PACKAGE_ROOT,
    PRIVATE_DIR,
    PROJECT_ROOT,
)
from research_orbit.memory_cards import build_memory_cards
from research_orbit.providers.provider_registry import list_provider_configs
from research_orbit.redaction import scan_paths
from research_orbit.workflows import list_workflows

UI_ASSET_DIR = PACKAGE_ROOT / "ui_assets"


def build_ui_state() -> dict[str, object]:
    """Build a local-only UI state snapshot without reading private generated material."""
    workflows = list_workflows()
    providers = list_provider_configs()
    memory_cards = build_memory_cards([EXAMPLES_DIR])
    redaction_findings = scan_paths([EXAMPLES_DIR])

    return {
        "project": {
            "name": "Research Orbit",
            "version": __version__,
            "description": "Agentic Research OS for reusable scientific AI workflows.",
        },
        "paths": {
            "project_root": _display_path(PROJECT_ROOT),
            "examples": _display_path(EXAMPLES_DIR),
            "public_outputs": _display_path(OUTPUTS_DIR),
            "private_outputs": _display_path(PRIVATE_DIR),
            "default_application_pack": _display_path(DEFAULT_APPLICATION_PACK_DIR),
        },
        "summary": {
            "workflow_count": len(workflows),
            "provider_count": len(providers),
            "configured_provider_count": sum(1 for provider in providers if provider.configured),
            "memory_card_count": len(memory_cards),
            "redaction_finding_count": len(redaction_findings),
        },
        "providers": [provider.model_dump(mode="json") for provider in providers],
        "workflows": [
            {
                "name": workflow.name,
                "version": workflow.version,
                "description": workflow.description,
                "steps": [step.model_dump(mode="json") for step in workflow.steps],
                "safety_rules": workflow.safety_rules,
                "success_criteria": workflow.success_criteria,
                "context_usage_pattern": workflow.context_usage_pattern,
                "provider_requirements": workflow.provider_requirements,
                "evidence_materials": workflow.evidence_materials,
            }
            for workflow in workflows
        ],
        "memory_cards": [card.model_dump(mode="json") for card in memory_cards],
        "redaction_findings": [finding.model_dump(mode="json") for finding in redaction_findings],
    }


def serve_ui(host: str = "127.0.0.1", port: int = 8765, open_browser: bool = False) -> None:
    """Start the local Research Orbit web UI."""
    server = ThreadingHTTPServer((host, port), ResearchOrbitUiHandler)
    url = f"http://{host}:{port}"
    print(f"Research Orbit UI running at {url}")
    print("Press Ctrl+C to stop.")
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nResearch Orbit UI stopped.")
    finally:
        server.server_close()


class ResearchOrbitUiHandler(BaseHTTPRequestHandler):
    server_version = "ResearchOrbitUI/0.1"

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler.
        parsed = urlparse(self.path)
        if parsed.path == "/api/state":
            self._send_json(build_ui_state())
            return
        if parsed.path == "/healthz":
            self._send_json({"status": "ok"})
            return
        asset = _resolve_asset(parsed.path)
        if asset is None:
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return
        self._send_file(asset)

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_json(self, payload: dict[str, object]) -> None:
        encoded = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_file(self, path: Path) -> None:
        content = path.read_bytes()
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if path.suffix == ".js":
            content_type = "application/javascript; charset=utf-8"
        if path.suffix in {".html", ".css"}:
            content_type = f"text/{path.suffix[1:]}; charset=utf-8"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def _resolve_asset(request_path: str) -> Path | None:
    route = unquote(request_path)
    if route in {"", "/"}:
        route = "/index.html"
    relative = route.lstrip("/")
    candidate = (UI_ASSET_DIR / relative).resolve()
    root = UI_ASSET_DIR.resolve()
    if candidate != root and root not in candidate.parents:
        return None
    if not candidate.is_file():
        return None
    return candidate


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(PROJECT_ROOT).as_posix() or "."
    except ValueError:
        return path.as_posix()
