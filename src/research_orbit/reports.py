"""Report rendering helpers."""

from __future__ import annotations

from research_orbit.schemas import ProviderResponse, WorkflowSpec


def render_workflow_report(
    *,
    spec: WorkflowSpec,
    input_name: str,
    provider_response: ProviderResponse,
) -> str:
    lines = [
        f"# Workflow Report: {spec.name}",
        "",
        f"- version: `{spec.version}`",
        f"- input: `{input_name}`",
        f"- provider: `{provider_response.provider}`",
        f"- model: `{provider_response.model}`",
        f"- dry_run: `{provider_response.used_dry_run}`",
        "",
        "## Description",
        spec.description,
        "",
        "## Steps",
    ]
    for step in spec.steps:
        lines.extend(
            [
                f"### {step.id}: {step.title}",
                step.instruction,
                "",
                "Expected evidence: " + ", ".join(step.expected_evidence or ["not specified"]),
                "",
            ]
        )
    lines.extend(["## Safety Rules", ""])
    lines.extend(f"- {rule}" for rule in spec.safety_rules)
    lines.extend(["", "## Success Criteria", ""])
    lines.extend(f"- {criterion}" for criterion in spec.success_criteria)
    lines.extend(["", "## Provider Output", "", provider_response.content, ""])
    if provider_response.warnings:
        lines.extend(["## Warnings", ""])
        lines.extend(f"- {warning}" for warning in provider_response.warnings)
        lines.append("")
    return "\n".join(lines)
