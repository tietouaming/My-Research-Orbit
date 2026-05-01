# GitHub Proof Materials Guide

Public proof material should show that Research Orbit is a real, runnable project without
exposing private research assets.

Good public proof:

- Project README with install and CLI commands.
- Python package under `src/research_orbit/`.
- Workflow YAML files under `workflows/`.
- Desensitized examples under `examples/`.
- Tests under `tests/`.
- CI workflow under `.github/workflows/research-orbit-ci.yml`.
- Documentation for architecture, providers, safety, roadmap, and evaluation.

Do not publish:

- Generated private application packs.
- Raw `.mph`, `.mphbin`, HDF5, NPZ, VTU, XDMF, PNG, GIF, or other large result files.
- Real local paths, account names, passwords, API keys, or tokens.
- Unredacted logs or manuscripts.

Before pushing, run:

```powershell
research-orbit audit-redaction --input examples --output outputs/redaction_report.md
research-orbit validate
pytest -q
```
