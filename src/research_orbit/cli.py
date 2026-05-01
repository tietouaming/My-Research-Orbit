"""Research Orbit command line interface."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from research_orbit import __version__
from research_orbit.application_pack import SUPPORTED_TARGETS, generate_application_pack
from research_orbit.config import (
    DEFAULT_APPLICATION_PACK_DIR,
    OUTPUTS_DIR,
    PRIVATE_DIR,
    PROJECT_ROOT,
)
from research_orbit.ingest import ingest_notes as ingest_notes_impl
from research_orbit.memory_cards import build_memory_cards, write_cards
from research_orbit.providers.provider_registry import list_provider_configs
from research_orbit.redaction import render_redaction_report, scan_paths
from research_orbit.ui_server import serve_ui
from research_orbit.validators import validate_project
from research_orbit.workflows import list_workflows, run_workflow, validate_workflow_files

app = typer.Typer(help="Research Orbit: agentic research workflow CLI.")
console = Console()


@app.command()
def inspect() -> None:
    """Show project information, paths, provider, and workflow count."""
    table = Table(title="Research Orbit")
    table.add_column("Key")
    table.add_column("Value")
    table.add_row("version", __version__)
    table.add_row("project_root", str(PROJECT_ROOT))
    table.add_row("public_outputs", str(OUTPUTS_DIR))
    table.add_row("private_outputs", str(PRIVATE_DIR))
    table.add_row("default_application_pack", str(DEFAULT_APPLICATION_PACK_DIR))
    table.add_row("workflows", str(len(list_workflows())))
    configured = [cfg.name for cfg in list_provider_configs() if cfg.configured]
    table.add_row("configured_providers", ", ".join(configured))
    console.print(table)


@app.command()
def providers() -> None:
    """List provider adapters and masked configuration status."""
    table = Table(title="Research Orbit Providers")
    for column in ("Provider", "Configured", "Required env", "Optional env", "Capability", "Notes"):
        table.add_column(column)
    for cfg in list_provider_configs():
        table.add_row(
            cfg.name,
            "yes" if cfg.configured else "no",
            ", ".join(cfg.required_env) or "-",
            ", ".join(cfg.optional_env) or "-",
            cfg.capability,
            cfg.notes,
        )
    console.print(table)


@app.command("ingest-notes")
def ingest_notes(
    input_paths: Annotated[list[Path], typer.Option("--input", "-i", exists=True)],
    output: Annotated[Path, typer.Option("--output", "-o")],
    output_format: Annotated[str, typer.Option("--format")] = "jsonl",
) -> None:
    """Read Markdown/TXT notes and write memory cards."""
    cards = ingest_notes_impl(input_paths, output, output_format)
    console.print(f"Wrote {len(cards)} memory cards to {output}")


@app.command("build-memory-cards")
def build_memory_cards_command(
    input_paths: Annotated[list[Path], typer.Option("--input", "-i", exists=True)],
    output: Annotated[Path, typer.Option("--output", "-o")],
    output_format: Annotated[str, typer.Option("--format")] = "jsonl",
) -> None:
    """Build reusable operation memory cards from files or directories."""
    cards = build_memory_cards(input_paths)
    write_cards(cards, output, output_format)
    console.print(f"Wrote {len(cards)} memory cards to {output}")


@app.command("list-workflows")
def list_workflows_command() -> None:
    """List and validate workflow YAML files."""
    issues = validate_workflow_files()
    table = Table(title="Research Orbit Workflows")
    for column in ("Name", "Version", "Steps", "Description"):
        table.add_column(column)
    for spec in list_workflows():
        table.add_row(spec.name, spec.version, str(len(spec.steps)), spec.description)
    console.print(table)
    if issues:
        for issue in issues:
            console.print(f"[red]{issue}[/red]")
        raise typer.Exit(1)


@app.command("run-workflow")
def run_workflow_command(
    workflow: Annotated[str, typer.Option("--workflow", "-w")],
    input_path: Annotated[Path, typer.Option("--input", "-i", exists=True)],
    output: Annotated[Path, typer.Option("--output", "-o")],
    provider: Annotated[str | None, typer.Option("--provider")] = None,
) -> None:
    """Run a workflow against an input file and write a report."""
    run_workflow(
        workflow=workflow,
        input_path=input_path,
        output_path=output,
        provider_name=provider,
    )
    console.print(f"Wrote workflow report to {output}")


@app.command("generate-application-pack")
def generate_application_pack_command(
    target: Annotated[str, typer.Option("--target")] = "general-creator-program",
    output: Annotated[Path | None, typer.Option("--output")] = None,
) -> None:
    """Generate local-only private application materials."""
    if target not in SUPPORTED_TARGETS:
        known = ", ".join(sorted(SUPPORTED_TARGETS))
        console.print(f"[red]Unknown target `{target}`. Known targets: {known}[/red]")
        raise typer.Exit(1)
    pack = generate_application_pack(target=target, output_dir=output)
    console.print(f"Generated private application pack in {pack.output_dir}")
    for path in pack.files:
        console.print(f"- {path.name}")
    console.print("Do not commit this directory to GitHub.")


@app.command("audit-redaction")
def audit_redaction(
    input_paths: Annotated[list[Path], typer.Option("--input", "-i", exists=True)],
    output: Annotated[Path, typer.Option("--output", "-o")],
) -> None:
    """Audit local files for sensitive patterns and write a Markdown report."""
    findings = scan_paths(input_paths)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_redaction_report(findings), encoding="utf-8")
    console.print(f"Wrote redaction report with {len(findings)} findings to {output}")


@app.command()
def validate() -> None:
    """Validate project structure, workflow specs, docs, examples, and ignore rules."""
    issues = validate_project()
    if issues:
        console.print("[red]Validation failed[/red]")
        for issue in issues:
            console.print(f"- {issue}")
        raise typer.Exit(1)
    console.print("[green]Research Orbit validation passed.[/green]")


@app.command()
def ui(
    host: Annotated[str, typer.Option("--host")] = "127.0.0.1",
    port: Annotated[int, typer.Option("--port")] = 8765,
    open_browser: Annotated[bool, typer.Option("--open-browser")] = False,
) -> None:
    """Start the local Research Orbit web workbench."""
    serve_ui(host=host, port=port, open_browser=open_browser)


if __name__ == "__main__":
    app()
