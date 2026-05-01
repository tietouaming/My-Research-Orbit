# Privacy

Research Orbit is designed around local-first handling of sensitive research context.

## Public Repository Contents

The public repository should contain only source code, workflow definitions, tests,
documentation, small desensitized examples, and public example outputs.

## Private Local Contents

The following must remain local:

- generated application packs;
- private operation logs;
- real API keys or provider credentials;
- raw COMSOL models and simulation outputs;
- local absolute paths and account-specific metadata;
- unpublished documents or research details that have not been desensitized.

## External Providers

The default `dry-run` provider does not send data to external services. Real model calls
are only possible after a user explicitly configures a provider through environment
variables and runs a command with user-supplied input.
