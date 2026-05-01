# Evaluation Plan

Research Orbit is evaluated as an engineering workflow system, not as a scientific solver.

## Functional Checks

- `research-orbit inspect` reports project paths and workflow count.
- `research-orbit providers` masks provider configuration status.
- `research-orbit list-workflows` validates all YAML workflow files.
- `research-orbit build-memory-cards` writes JSONL and Markdown memory cards.
- `research-orbit run-workflow` writes deterministic dry-run reports.
- `research-orbit audit-redaction` writes local redaction reports.
- `research-orbit generate-application-pack` writes private drafts under ignored paths.
- `research-orbit validate` catches missing files, invalid workflows, and ignore-rule gaps.

## Quality Checks

- Memory cards preserve source paths and reusable rules.
- Workflow reports separate safety rules, evidence, and provider output.
- Provider registry never prints raw API keys.
- Application-pack generation defaults to `.local_private/application_pack/`.
- Public docs do not present a single provider as the project identity.

## Regression Tests

Pytest covers redaction, memory cards, workflow loading, provider registry behavior,
application pack generation, and CLI smoke commands. CI runs only dry-run mode.
