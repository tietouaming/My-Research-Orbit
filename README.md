# My Research Orbit

![Research Orbit CI](https://github.com/tietouaming/My-Research-Orbit/actions/workflows/ci.yml/badge.svg)

This repository contains **Research Orbit**, an Agentic Research OS for turning daily
scientific AI collaboration into reusable, auditable research workflows.

Research Orbit is designed for researchers who repeatedly use AI agents to edit papers,
handle formulas, audit COMSOL-derived model summaries, review simulation migrations,
diagnose logs, consolidate multi-machine memory, and prepare local-only project evidence.
The project is provider-neutral: it supports a provider abstraction layer for OpenAI,
Claude, Gemini, GLM, MiniMax, Kimi, MiMo, DeepSeek, and OpenAI-compatible endpoints.

Public visibility does not grant permission to use, copy, modify, redistribute,
commercialize, train models on, or derive work from this repository. See
[LICENSE](LICENSE), [NOTICE.md](NOTICE.md), and [USAGE_NOTICE.md](USAGE_NOTICE.md).

## What It Does

- Generates reusable operation memory cards from Markdown, TXT, and log notes.
- Runs structured Agent workflow specs from YAML.
- Provides a deterministic `dry-run` provider for CI and no-key environments.
- Defines provider adapters for OpenAI and OpenAI-compatible APIs, with clear placeholders
  for Claude and Gemini live transports.
- Documents configuration paths for GLM, MiniMax, Kimi, MiMo, and DeepSeek through
  OpenAI-compatible endpoints when the user supplies a base URL, key, and model.
- Audits local text for sensitive paths, secrets, account-like material, and large/private
  research file extensions.
- Generates local private application packs into `.local_private/application_pack/`.
- Provides a local web workbench for inspecting workflows, providers, memory cards, and
  redaction findings.
- Ships tests, examples, docs, and GitHub Actions CI.

Research Orbit is not a magnesium-alloy solver project. COMSOL, Word, MathType, FEniCSx,
MOOSE, and PyTorch are example high-complexity research settings used to motivate reusable
Agent workflows.

## Installation

```powershell
git clone https://github.com/tietouaming/My-Research-Orbit.git
cd My-Research-Orbit
python -m pip install -e ".[dev]"
```

Python 3.11 or newer is required.

## CLI Quick Start

```powershell
research-orbit inspect
research-orbit providers
research-orbit list-workflows
research-orbit build-memory-cards --input examples --output outputs/memory_cards.jsonl --format jsonl
research-orbit run-workflow --workflow research_memory_compactor --input examples/sample_operation_log.md --output outputs/research_memory_report.md
research-orbit audit-redaction --input examples --output outputs/redaction_report.md
research-orbit generate-application-pack --target mimo-orbit
research-orbit validate
research-orbit ui
pytest -q
```

The default provider is `dry-run`, so these commands do not require API keys and do not
send data to external services.

For reproducible example output in documentation or CI fixtures, set:

```powershell
$env:RESEARCH_ORBIT_FIXED_CREATED_AT="2026-05-01T00:00:00Z"
```

## Local Web UI

Start the local Research Orbit workbench with:

```powershell
research-orbit ui --host 127.0.0.1 --port 8765
```

Then open:

```text
http://127.0.0.1:8765
```

The UI is served from the Python package with the standard library HTTP server. It reads
public project state from workflows, examples, provider configuration status, and local
redaction scans. It does not upload data, does not display API key values, and does not
read `.local_private/` application-pack contents.

## Workflows

Workflow YAML files live in `workflows/` and include:

- `research_memory_compactor`: compresses daily agent notes into reusable memory cards.
- `word_mathtype_editor`: plans safe Word and MathType edits with backup, tracked
  revisions, and formula object boundaries.
- `comsol_model_auditor`: audits structured COMSOL model summaries without hand-copying
  formulas from memory.
- `simulation_porting_reviewer`: reviews COMSOL-to-FEniCSx, MOOSE, or Python migration
  evidence with t=0 alignment as the first gate.
- `run_log_diagnoser`: diagnoses solver, automation, and CI logs with evidence-ranked
  next actions.
- `application_pack_writer`: generates local-only application drafts under an ignored
  private directory.

Each workflow declares inputs, outputs, tools, steps, safety rules, success criteria,
context usage pattern, provider requirements, and evidence materials.

## Provider Configuration

Dry-run mode is always available:

```powershell
$env:RESEARCH_ORBIT_PROVIDER="dry-run"
```

OpenAI:

```powershell
$env:RESEARCH_ORBIT_PROVIDER="openai"
$env:OPENAI_API_KEY="<your key>"
$env:OPENAI_MODEL="<model>"
```

Generic OpenAI-compatible endpoint:

```powershell
$env:RESEARCH_ORBIT_PROVIDER="openai-compatible"
$env:RESEARCH_ORBIT_API_BASE_URL="https://provider.example/v1"
$env:RESEARCH_ORBIT_API_KEY="<your key>"
$env:RESEARCH_ORBIT_MODEL="<model>"
```

Provider-specific configuration examples:

```powershell
$env:RESEARCH_ORBIT_PROVIDER="kimi"
$env:KIMI_API_BASE_URL="<compatible base URL>"
$env:KIMI_API_KEY="<your key>"
$env:KIMI_MODEL="<model>"

$env:RESEARCH_ORBIT_PROVIDER="mimo"
$env:MIMO_API_BASE_URL="<compatible base URL>"
$env:MIMO_API_KEY="<your key>"
$env:MIMO_MODEL="<model>"
```

GLM, MiniMax, Kimi, MiMo, and DeepSeek are documented as configurable provider routes.
No unverified endpoint is hardcoded. Claude and Gemini adapters expose explicit interfaces;
their direct live transports should be implemented and tested before use.

## Security And Redaction

Run a local audit before publishing generated material:

```powershell
research-orbit audit-redaction --input examples --output outputs/redaction_report.md
```

The audit checks for local paths, secrets, passwords, token-like strings, email addresses,
phone numbers, and private or large research file extensions such as `.mph`, `.mphbin`,
HDF5, NPZ, VTU, XDMF, PNG, and GIF.

Do not commit raw COMSOL models, solver binaries, generated private application packs,
unredacted logs, API keys, account information, or real local paths.

## Local Private Application Packs

The command below generates local-only draft material:

```powershell
research-orbit generate-application-pack --target mimo-orbit
```

By default, files are written to:

```text
.local_private/application_pack/
```

That directory is ignored by Git. Generated application files are not public project
material and should be manually reviewed before external use.

## Repository Notices

This repository intentionally uses an authorization-required license. It is visible for
review, archival demonstration, and collaboration discussions, but it is not open source
in the OSI sense unless the author separately grants explicit written permission.

Read these files before using the repository:

- [LICENSE](LICENSE)
- [NOTICE.md](NOTICE.md)
- [USAGE_NOTICE.md](USAGE_NOTICE.md)
- [SECURITY.md](SECURITY.md)
- [PRIVACY.md](PRIVACY.md)
- [DISCLAIMER.md](DISCLAIMER.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)

## Development

```powershell
python -m pip install -e ".[dev]"
ruff check .
pytest -q
research-orbit validate
research-orbit ui
```

CI uses dry-run only and does not require real provider credentials.

## Current Limits

- Memory-card extraction is deterministic and rule-based; it is intentionally conservative.
- OpenAI-compatible providers require user-supplied base URLs, keys, and model names.
- Claude and Gemini direct live transports are placeholders until implemented against
  current official APIs.
- The project does not parse raw `.mph` files directly; it expects desensitized structured
  summaries for public workflows.
- The web UI is a local inspection workbench; workflow execution history and editing
  controls are planned for later versions.

## Roadmap

- Add richer memory-card extraction and evaluation fixtures.
- Add tested direct transports for Claude and Gemini.
- Add UI controls for launching dry-run workflows and comparing generated reports.
- Add structured importers for desensitized COMSOL model summaries.
- Expand Word/MathType safety checklists and dry-run verification reports.
