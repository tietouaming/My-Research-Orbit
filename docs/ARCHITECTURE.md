# Architecture

Research Orbit separates public reusable workflow infrastructure from private research
materials.

## Layers

1. CLI layer: `research-orbit` exposes inspect, provider listing, memory-card generation,
   workflow execution, redaction audit, application-pack generation, and validation.
2. UI layer: `research-orbit ui` serves a local web workbench from package assets. It
   displays workflows, provider status, example memory cards, redaction findings, and
   safe project paths without exposing secrets or private generated materials.
3. Schema layer: Pydantic models define memory cards, workflows, provider configuration,
   redaction findings, and application packs.
4. Workflow layer: YAML files describe agent tasks, safety rules, success criteria, context
   usage patterns, and evidence materials.
5. Provider layer: adapters isolate model calls from workflow logic. `dry-run` is local and
   deterministic. OpenAI-compatible providers use explicit environment configuration.
6. Safety layer: redaction checks and ignore rules keep private material out of Git.
7. Documentation layer: public docs describe project use, provider boundaries, evaluation,
   and private application-pack handling.

## Data Flow

Text notes or logs enter through CLI commands. The memory-card generator classifies and
summarizes them into structured records. Workflow execution loads a YAML spec, renders a
prompt, runs the selected provider, and writes a Markdown report. Redaction audits scan
local text and produce a report without external network calls.

The web UI reads the same local project APIs used by the CLI. It builds a snapshot from
workflow YAML, masked provider configuration, desensitized examples, generated memory
cards, and redaction findings. It does not call external model providers and does not read
ignored private application-pack files.

Application-pack generation is deliberately separate. It writes local-only draft files
under `.local_private/application_pack/`, which is ignored by Git.

## Extension Points

- Add new workflow YAML files under `workflows/`.
- Add new provider adapters under `src/research_orbit/providers/`.
- Add new card classification rules in `memory_cards.py`.
- Add new validators in `validators.py`.
- Add new UI panels under `src/research_orbit/ui_assets/` and expose local state from
  `ui_server.py`.
- Add new local-only private pack templates in `application_pack.py`.
