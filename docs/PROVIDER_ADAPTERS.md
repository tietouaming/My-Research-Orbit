# Provider Adapters

Research Orbit 使用 provider adapter 隔离 workflow 逻辑和模型调用。项目公开定位是 provider-neutral，任何单一 provider 都不是项目主体。

## dry-run

默认 provider。无需密钥，不访问网络，输出确定性模板，适合 CI、测试和无密钥演示。

```powershell
$env:RESEARCH_ORBIT_PROVIDER="dry-run"
```

## OpenAI

面向 OpenAI Chat Completions 风格调用。API key 和 model 均来自环境变量。

```powershell
$env:RESEARCH_ORBIT_PROVIDER="openai"
$env:OPENAI_API_KEY="<key>"
$env:OPENAI_MODEL="<model>"
```

## OpenAI-compatible

通用兼容接口，适用于用户明确提供 base URL、key 和 model 的 provider 或网关。

```powershell
$env:RESEARCH_ORBIT_PROVIDER="openai-compatible"
$env:RESEARCH_ORBIT_API_BASE_URL="https://provider.example/v1"
$env:RESEARCH_ORBIT_API_KEY="<key>"
$env:RESEARCH_ORBIT_MODEL="<model>"
```

## Claude 与 Gemini

`anthropic` 和 `gemini` 当前保留清晰接口和配置校验，但 direct live transport 尚未实现。项目不会伪造真实调用成功。

## GLM、MiniMax、Kimi、MiMo、DeepSeek

这些 provider 通过 OpenAI-compatible 路径配置，不硬编码未确认 endpoint。

```powershell
$env:RESEARCH_ORBIT_PROVIDER="mimo"
$env:MIMO_API_BASE_URL="<compatible base URL>"
$env:MIMO_API_KEY="<key>"
$env:MIMO_MODEL="<model>"
```

MiMo 只是多个 provider 之一，不是公开项目主体。

## 安全规则

- 不打印 API key 原文；
- 无环境变量时默认 dry-run；
- CI 不依赖真实 provider；
- 私有申请材料不会自动发送给任何外部 provider；
- 未确认接口不硬编码。
