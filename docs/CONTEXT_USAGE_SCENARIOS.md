# Context And Token Usage Scenarios

Research Orbit is designed for long-context and multi-round research work.

## Long Document Reading

Agents often need to read many small Markdown notes, runbooks, solver reports, and review
logs before producing a reusable conclusion. Memory compaction reduces that context into
structured cards with source paths and verification status.

## Multi-Round Manuscript Revision

Scientific writing may span many edit rounds. The Word/MathType workflow keeps backup,
tracked revisions, formula object boundaries, captions, cross references, and comments in
view across turns.

## Word And MathType Safe Editing

Formula objects are not normal text. Long context is used to remember document state,
selection risks, backup paths, revision mode, and post-edit verification requirements.

## COMSOL Model Review

COMSOL-derived summaries can include parameters, variables, weak forms, geometry, mesh,
boundary conditions, studies, solvers, probes, and result groups. The workflow keeps these
sections together and avoids hand-copying formulas from memory.

## Weak Form And Boundary Checks

Long context helps compare original expressions, interpreted equations, domains,
boundaries, and solver settings. The output should state what is verified and what remains
uncertain.

## Run Log Diagnosis

Solver and CI logs can be long and repetitive. The diagnoser extracts the first error,
repeated symptoms, evidence, likely causes, ordered checks, and non-conclusions.

## Multi-Machine Memory Merge

When several machines work on the same research project, each machine should write
additive notes. Later consolidation should merge by review instead of overwriting files.

## Local Application Material Generation

Application drafts may need project summaries, architecture, context usage, proof
materials, roadmaps, and form drafts. Research Orbit generates these locally and keeps the
results out of Git.

## Code Review And Test Failure Repair

The same workflow pattern can review code changes, summarize failing tests, rank fixes,
and capture reusable rules for future agent runs.
