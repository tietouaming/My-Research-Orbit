# Workflow Report: research_memory_compactor

- version: `0.1`
- input: `examples/sample_operation_log.md`
- provider: `dry-run`
- model: `deterministic-template`
- dry_run: `True`

## Description
Compress daily agent operation notes into reusable scientific memory cards.

## Steps
### collect: Collect source notes
Read only user-provided or repository-local text notes and preserve source paths.

Expected evidence: source file list

### classify: Classify operations
Classify each note into research workflow categories before summarizing.

Expected evidence: category per card

### extract_rule: Extract reusable rule
Convert the observed operation into a concise reusable rule with risk and verification status.

Expected evidence: reusable_rule, risk_level

### audit: Check safety
Flag sensitive paths, credentials, raw model files, and unredacted records before publication.

Expected evidence: redaction findings

## Safety Rules

- Do not include unredacted local paths, account names, credentials, or raw private logs.
- Do not overwrite another machine's notes during consolidation.
- Keep raw scientific models and large binary artifacts outside Git.

## Success Criteria

- Every card has title, source path, category, problem, solution, reusable rule, risk, verification, and tags.
- The output can be regenerated deterministically in dry-run mode.

## Provider Output

Dry-run provider response

- fingerprint: `e0ec6543f41f`
- external_api_call: false
- result: The workflow prompt was rendered and can be inspected safely.
- next_step: Replace `RESEARCH_ORBIT_PROVIDER` only when a real provider is explicitly configured.
