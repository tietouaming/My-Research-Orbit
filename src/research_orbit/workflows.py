"""Workflow loading, validation, and dry-run execution."""

from __future__ import annotations

from pathlib import Path

import yaml

from research_orbit.config import WORKFLOWS_DIR, ensure_output_parent
from research_orbit.llm import generate_with_provider
from research_orbit.reports import render_workflow_report
from research_orbit.schemas import WorkflowSpec


def workflow_path(name_or_path: str | Path) -> Path:
    path = Path(name_or_path)
    if path.exists():
        return path
    if path.suffix:
        candidate = WORKFLOWS_DIR / path.name
    else:
        candidate = WORKFLOWS_DIR / f"{path.name}.yaml"
    return candidate


def load_workflow(name_or_path: str | Path) -> WorkflowSpec:
    path = workflow_path(name_or_path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return WorkflowSpec.model_validate(data)


def list_workflows() -> list[WorkflowSpec]:
    specs: list[WorkflowSpec] = []
    for path in sorted(WORKFLOWS_DIR.glob("*.yaml")):
        specs.append(load_workflow(path))
    return specs


def validate_workflow_files() -> list[str]:
    issues: list[str] = []
    for path in sorted(WORKFLOWS_DIR.glob("*.yaml")):
        try:
            load_workflow(path)
        except Exception as exc:  # noqa: BLE001 - validation command should report all files.
            issues.append(f"{path}: {exc}")
    if not list(WORKFLOWS_DIR.glob("*.yaml")):
        issues.append(f"No workflow YAML files found in {WORKFLOWS_DIR}.")
    return issues


def run_workflow(
    *,
    workflow: str,
    input_path: Path,
    output_path: Path,
    provider_name: str | None = None,
) -> str:
    spec = load_workflow(workflow)
    input_text = input_path.read_text(encoding="utf-8")
    system_prompt = render_system_prompt(spec)
    user_prompt = render_user_prompt(spec, input_text)
    provider_response = generate_with_provider(
        provider_name=provider_name,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )
    report = render_workflow_report(
        spec=spec,
        input_name=input_path.as_posix(),
        provider_response=provider_response,
    )
    ensure_output_parent(output_path)
    output_path.write_text(report, encoding="utf-8")
    return report


def render_system_prompt(spec: WorkflowSpec) -> str:
    return (
        f"You are running the Research Orbit workflow `{spec.name}`.\n"
        f"Intended user: {spec.intended_user}\n"
        "Follow safety rules exactly and separate evidence from inference."
    )


def render_user_prompt(spec: WorkflowSpec, input_text: str) -> str:
    steps = "\n".join(f"- {step.id}: {step.instruction}" for step in spec.steps)
    safety = "\n".join(f"- {rule}" for rule in spec.safety_rules)
    return (
        f"Workflow description:\n{spec.description}\n\n"
        f"Context usage pattern:\n{spec.context_usage_pattern}\n\n"
        f"Steps:\n{steps}\n\n"
        f"Safety rules:\n{safety}\n\n"
        f"Input material:\n{input_text}"
    )
