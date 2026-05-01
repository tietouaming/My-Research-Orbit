from pathlib import Path

from typer.testing import CliRunner

from research_orbit.cli import app

runner = CliRunner()


def test_cli_smoke_commands() -> None:
    for command in (["inspect"], ["providers"], ["list-workflows"], ["validate"], ["ui", "--help"]):
        result = runner.invoke(app, command)
        assert result.exit_code == 0, result.output


def test_cli_build_run_audit_and_pack(tmp_path: Path) -> None:
    cards = tmp_path / "cards.jsonl"
    result = runner.invoke(
        app,
        [
            "build-memory-cards",
            "--input",
            "examples",
            "--output",
            str(cards),
            "--format",
            "jsonl",
        ],
    )
    assert result.exit_code == 0, result.output
    assert cards.exists()

    report = tmp_path / "workflow.md"
    result = runner.invoke(
        app,
        [
            "run-workflow",
            "--workflow",
            "research_memory_compactor",
            "--input",
            "examples/sample_operation_log.md",
            "--output",
            str(report),
        ],
    )
    assert result.exit_code == 0, result.output
    assert "Workflow Report" in report.read_text(encoding="utf-8")

    redaction_report = tmp_path / "redaction.md"
    result = runner.invoke(
        app,
        ["audit-redaction", "--input", "examples", "--output", str(redaction_report)],
    )
    assert result.exit_code == 0, result.output
    assert redaction_report.exists()

    private_pack = tmp_path / "application_pack"
    result = runner.invoke(
        app,
        ["generate-application-pack", "--target", "mimo-orbit", "--output", str(private_pack)],
    )
    assert result.exit_code == 0, result.output
    assert (private_pack / "01_project_summary.md").exists()
