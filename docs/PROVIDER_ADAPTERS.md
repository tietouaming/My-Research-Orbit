# Provider Adapters

Research Orbit uses provider adapters so workflow logic does not depend on a single model
vendor.

## dry-run

`dry-run` is the default provider. It never calls external APIs and produces deterministic
template output. CI uses this mode.

```powershell
$env:RESEARCH_ORBIT_PROVIDER="dry-run"
```

## OpenAI

The OpenAI adapter uses Chat Completions style requests and environment variables:

```powershell
$env:RESEARCH_ORBIT_PROVIDER="openai"
$env:OPENAI_API_KEY="<key>"
$env:OPENAI_MODEL="<model>"
```

`OPENAI_API_BASE_URL` can override the default official base URL if needed.

## OpenAI-Compatible

The generic adapter supports providers or gateways that expose an OpenAI-compatible chat
completions API:

```powershell
$env:RESEARCH_ORBIT_PROVIDER="openai-compatible"
$env:RESEARCH_ORBIT_API_BASE_URL="<base URL>"
$env:RESEARCH_ORBIT_API_KEY="<key>"
$env:RESEARCH_ORBIT_MODEL="<model>"
```

## Claude

The Anthropic Claude adapter currently exposes a clear configuration interface and refuses
to fake live success. A tested Messages API transport should be added before live use.

Required variables:

- `ANTHROPIC_API_KEY`
- `ANTHROPIC_MODEL`

## Gemini

The Gemini adapter currently exposes a clear configuration interface and refuses to fake
live success. A tested Gemini transport should be added before live use.

Required variables:

- `GEMINI_API_KEY`
- `GEMINI_MODEL`

## GLM, MiniMax, Kimi, MiMo, DeepSeek

These providers can be routed through OpenAI-compatible configuration when the user has a
verified compatible endpoint.

Examples:

```powershell
$env:RESEARCH_ORBIT_PROVIDER="zhipu"
$env:ZHIPU_API_BASE_URL="<base URL>"
$env:ZHIPU_API_KEY="<key>"
$env:ZHIPU_MODEL="<model>"

$env:RESEARCH_ORBIT_PROVIDER="minimax"
$env:MINIMAX_API_BASE_URL="<base URL>"
$env:MINIMAX_API_KEY="<key>"
$env:MINIMAX_MODEL="<model>"

$env:RESEARCH_ORBIT_PROVIDER="kimi"
$env:KIMI_API_BASE_URL="<base URL>"
$env:KIMI_API_KEY="<key>"
$env:KIMI_MODEL="<model>"

$env:RESEARCH_ORBIT_PROVIDER="mimo"
$env:MIMO_API_BASE_URL="<base URL>"
$env:MIMO_API_KEY="<key>"
$env:MIMO_MODEL="<model>"

$env:RESEARCH_ORBIT_PROVIDER="deepseek"
$env:DEEPSEEK_API_BASE_URL="<base URL>"
$env:DEEPSEEK_API_KEY="<key>"
$env:DEEPSEEK_MODEL="<model>"
```

No API key is hardcoded or printed. No private material is sent to external providers
unless the user explicitly selects and configures a live provider.
