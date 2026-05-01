# Local Application Pack Guide

Research Orbit can generate local private application drafts. These drafts are not public
repository material.

Default output:

```text
.local_private/application_pack/
```

The directory is ignored by Git.

## Generate A Pack

```powershell
research-orbit generate-application-pack --target mimo-orbit
```

Other supported targets:

```powershell
research-orbit generate-application-pack --target general-creator-program
research-orbit generate-application-pack --target research-tool-grant
```

Generated files:

- `01_project_summary.md`
- `02_technical_architecture.md`
- `03_context_and_token_usage_plan.md`
- `04_github_proof_materials.md`
- `05_roadmap.md`
- `06_application_form_draft.md`

## Safety Checks

After generation:

```powershell
git check-ignore .local_private/application_pack/01_project_summary.md
research-orbit audit-redaction --input .local_private/application_pack --output outputs/private/application_pack_redaction.md
```

Manually review every generated file before using it outside the local machine. Confirm
that it contains no secrets, private paths, unpublished raw data, or unsupported provider
claims.
