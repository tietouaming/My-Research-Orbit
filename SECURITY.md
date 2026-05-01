# Security Policy

## Supported Scope

Security review currently covers the public Research Orbit source tree, CLI, workflow
definitions, examples, documentation, and local-only redaction/application-pack behavior.

## Reporting A Security Issue

Do not open a public issue containing secrets, credentials, private paths, unpublished
research material, or raw model files. Contact the repository owner through GitHub and
provide only a minimal, desensitized description until a private channel is agreed.

## Sensitive Material Rules

Do not commit:

- `.env`, `.env.*`, `.key`, `.pem`, `.token`, or credential files;
- API keys, tokens, passwords, secrets, account names, or private certificates;
- raw `.mph`, `.mphbin`, HDF5, NPZ, VTU, XDMF, PNG, GIF, or large solver outputs;
- unredacted local paths, private operation logs, or private application packs;
- unpublished research models or proprietary documents.

## Local-Only Behavior

The default provider is `dry-run`, which does not call external APIs. Real providers must
be explicitly configured through environment variables. Generated application packs are
written to `.local_private/application_pack/` by default and are ignored by Git.

## Redaction

Run this command before publishing generated material:

```powershell
research-orbit audit-redaction --input examples --output outputs/redaction_report.md
```

The audit is local-only and does not upload files.
