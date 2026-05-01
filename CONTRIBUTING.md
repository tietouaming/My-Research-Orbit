# Contributing

Contributions are welcome only under the repository's authorization-required terms.
Opening a pull request does not grant permission to use the project outside the scope of
reviewing and discussing that contribution.

## Ground Rules

- Keep the public project provider-neutral.
- Do not make MiMo, OpenAI, Claude, Gemini, GLM, MiniMax, Kimi, DeepSeek, or any other
  provider the sole public identity of the project.
- Do not commit private application packs or unredacted operation records.
- Do not commit raw `.mph`, `.mphbin`, HDF5, NPZ, VTU, XDMF, PNG, GIF, or large generated
  artifacts.
- Do not hardcode API keys, tokens, passwords, secrets, account names, or private paths.
- Keep examples small and desensitized.
- Prefer deterministic `dry-run` tests for CI.

## Local Checks

```powershell
python -m pip install -e ".[dev]"
ruff check .
pytest -q
research-orbit validate
```

## Pull Request Expectations

Each pull request should describe:

- what changed;
- how it was tested;
- whether it affects security or redaction behavior;
- whether it changes provider configuration;
- whether any generated files are included.

Generated private material under `.local_private/` must not be included.
