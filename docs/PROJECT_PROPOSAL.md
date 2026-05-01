# Project Proposal

Research Orbit is a general-purpose Agentic Research OS for scientific work. Its goal is
to turn repeated AI-assisted research operations into reusable workflows that can be
audited, tested, and extended.

The project is motivated by real research workflows where an agent must reason across
manuscript edits, equation objects, model summaries, solver logs, migration evidence,
multi-machine notes, and long-running project memory. These tasks require long context,
careful evidence tracking, and explicit safety boundaries.

Research Orbit does not present a single model provider as the project identity. It uses
a provider abstraction layer so researchers can run in `dry-run` mode, OpenAI mode,
OpenAI-compatible mode, or future provider-specific modes for Claude, Gemini, GLM,
MiniMax, Kimi, MiMo, and DeepSeek.

## Goals

- Make daily research agent operations reusable.
- Preserve source evidence and verification status.
- Keep private materials local by default.
- Provide deterministic CI behavior without API keys.
- Support future provider experiments without rewriting workflow logic.

## Non-Goals

- It is not a public release of private manuscripts, raw models, or solver artifacts.
- It is not a replacement for scientific validation.
- It is not a provider-specific application wrapper.
- It does not claim direct live integration for providers whose transports are not yet
  implemented and tested.
