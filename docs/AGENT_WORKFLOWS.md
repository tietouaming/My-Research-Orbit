# Agent Workflows

Research Orbit workflows are YAML documents with a stable structure:

- `name`
- `version`
- `description`
- `intended_user`
- `inputs`
- `outputs`
- `tools`
- `steps`
- `safety_rules`
- `success_criteria`
- `context_usage_pattern`
- `provider_requirements`
- `evidence_materials`

The schema is validated by `research-orbit list-workflows` and `research-orbit validate`.

## Included Workflows

`research_memory_compactor` converts daily agent operation logs into reusable memory cards.
It is useful after long work sessions where decisions are scattered across commands,
notes, and reports.

`word_mathtype_editor` plans safe manuscript changes. It requires backup, tracked
revisions, and formula object safety. MathType equations are not treated as normal text.

`comsol_model_auditor` audits structured summaries extracted from COMSOL models. The
workflow prioritizes intermediate structured data and original expressions over manual
transcription.

`simulation_porting_reviewer` reviews migration evidence from COMSOL toward FEniCSx,
MOOSE, or Python solvers. The first gate is t=0 whole-field alignment, followed by short
smoke tests and only then long-run interpretation.

`run_log_diagnoser` reads solver, automation, or CI logs and outputs possible causes,
evidence, priority-ordered checks, and limits.

`application_pack_writer` generates local-only application drafts. It writes to ignored
private directories by default and keeps target-specific material out of public Git.
