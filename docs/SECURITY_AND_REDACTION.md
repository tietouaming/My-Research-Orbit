# Security And Redaction

Research Orbit assumes research work contains private documents, unpublished models,
credentials, local paths, account identifiers, and large result files. The public
repository must contain only desensitized examples, code, workflow specs, tests, and
documentation.

## Do Not Commit

- Raw `.mph` or `.mphbin` files.
- HDF5, NPZ, VTU, XDMF, PNG, GIF, or other large solver/result files.
- Account names, passwords, tokens, API keys, secrets, or private certificates.
- Full local absolute paths.
- Original manuscripts, PDFs, Zotero exports, private Word drafts, or raw MathType data.
- Generated private application packs.

## Public Visibility Is Not Authorization

Public visibility does not grant permission to use, copy, modify, commercialize, train
models on, redistribute, cite, or derive work from this repository. Any such use requires
explicit authorization from the author.

## Audit Command

```powershell
research-orbit audit-redaction --input examples --output outputs/redaction_report.md
```

The audit checks local UTF-8 text for:

- Windows and Unix absolute paths
- API key, token, secret, password, authorization patterns
- email addresses
- phone-like numeric identifiers
- private or large research file extensions

The audit is local-only. It does not upload files and does not call any model provider.

## Provider Safety

`dry-run` is the default. Real providers require explicit environment configuration.
Private application materials or unredacted logs should not be sent to an external
provider unless the user intentionally supplies the material and selects a configured
provider.
