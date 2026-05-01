# My Research Orbit

![Research Orbit CI](https://github.com/tietouaming/My-Research-Orbit/actions/workflows/ci.yml/badge.svg)

本仓库包含 **Research Orbit**：一个面向科研人员的 Agentic Research OS，用于把日常 AI 协作中的论文编辑、公式处理、COMSOL 仿真模型审查、代码迁移、错误日志归因、运行经验总结、多机归档和长期记忆管理，沉淀为可复用、可审计、可扩展的 Agent 工作流系统。

Research Orbit 是通用科研 Agent 工作流系统，不是单一模型厂商项目，也不是旧镁合金求解器项目。OpenAI、Claude、Gemini、GLM、MiniMax、Kimi、MiMo、DeepSeek 以及 OpenAI-compatible endpoint 都只是 provider 适配层的一部分。

公开可见不等于授权使用。任何使用、复制、修改、商用、训练、二次分发或衍生工作，都必须获得作者本人明确授权。请先阅读 [LICENSE](LICENSE)、[NOTICE.md](NOTICE.md) 和 [USAGE_NOTICE.md](USAGE_NOTICE.md)。

## 主要能力

- 从 Markdown、TXT、log 笔记生成可复用科研操作记忆卡片。
- 读取并执行结构化 Agent workflow YAML。
- 提供默认 `dry-run` provider，CI 和无密钥环境可完整运行。
- 提供 OpenAI 与 OpenAI-compatible provider 抽象。
- 为 Claude、Gemini、GLM、MiniMax、Kimi、MiMo、DeepSeek 保留清晰配置说明和能力边界。
- 本地扫描敏感路径、API key/token/secret/password、邮箱、手机号和大型/私有科研文件扩展名。
- 默认把本地私有申请材料生成到 `.local_private/application_pack/`。
- 提供本地 Web 工作台，用于查看 workflows、providers、memory cards 和 redaction findings。
- 包含 tests、examples、outputs、docs 和 GitHub Actions CI。

## 安装

```powershell
git clone https://github.com/tietouaming/My-Research-Orbit.git
cd My-Research-Orbit
python -m pip install -e ".[dev]"
```

需要 Python 3.11 或更高版本。

## 快速开始

```powershell
research-orbit inspect
research-orbit providers
research-orbit list-workflows
research-orbit build-memory-cards --input examples --output outputs/memory_cards.jsonl --format jsonl
research-orbit run-workflow --workflow research_memory_compactor --input examples/sample_operation_log.md --output outputs/research_memory_report.md
research-orbit audit-redaction --input examples --output outputs/redaction_report.md
research-orbit generate-application-pack --target mimo-orbit
research-orbit validate
research-orbit ui
pytest -q
```

默认 provider 是 `dry-run`，因此这些命令不需要 API key，也不会向外部服务发送数据。

如需生成可复现示例输出，可设置：

```powershell
$env:RESEARCH_ORBIT_FIXED_CREATED_AT="2026-05-01T00:00:00Z"
```

## 本地 Web UI

启动本地工作台：

```powershell
research-orbit ui --host 127.0.0.1 --port 8765
```

打开：

```text
http://127.0.0.1:8765
```

UI 由 Python 包内静态资源和标准库 HTTP server 提供，只读取公开项目状态：workflow、示例、provider 配置状态和本地 redaction 扫描结果。它不会上传数据，不会显示 API key，也不会读取 `.local_private/` 中的申请材料。

## Workflow

`workflows/` 下包含 6 个基础 workflow：

- `research_memory_compactor`：把日常 Agent 操作日志压缩为可复用记忆卡片。
- `word_mathtype_editor`：规划 Word 和 MathType 安全编辑，强调备份、修订和公式对象边界。
- `comsol_model_auditor`：审查脱敏结构化 COMSOL 模型摘要，避免凭记忆手抄公式。
- `simulation_porting_reviewer`：审查 COMSOL 到 FEniCSx/MOOSE/Python 的迁移证据，先做 t=0 对齐。
- `run_log_diagnoser`：诊断 solver、automation 和 CI 日志，输出证据、原因、排查顺序和未知项。
- `application_pack_writer`：在本地忽略目录生成申请材料草稿。

每个 workflow 都包含 inputs、outputs、tools、steps、safety_rules、success_criteria、context_usage_pattern、provider_requirements 和 evidence_materials。

## Provider 配置

默认 dry-run：

```powershell
$env:RESEARCH_ORBIT_PROVIDER="dry-run"
```

OpenAI：

```powershell
$env:RESEARCH_ORBIT_PROVIDER="openai"
$env:OPENAI_API_KEY="<your key>"
$env:OPENAI_MODEL="<model>"
```

通用 OpenAI-compatible endpoint：

```powershell
$env:RESEARCH_ORBIT_PROVIDER="openai-compatible"
$env:RESEARCH_ORBIT_API_BASE_URL="https://provider.example/v1"
$env:RESEARCH_ORBIT_API_KEY="<your key>"
$env:RESEARCH_ORBIT_MODEL="<model>"
```

Kimi、MiMo 等 provider 可通过 OpenAI-compatible 路径配置：

```powershell
$env:RESEARCH_ORBIT_PROVIDER="kimi"
$env:KIMI_API_BASE_URL="<compatible base URL>"
$env:KIMI_API_KEY="<your key>"
$env:KIMI_MODEL="<model>"

$env:RESEARCH_ORBIT_PROVIDER="mimo"
$env:MIMO_API_BASE_URL="<compatible base URL>"
$env:MIMO_API_KEY="<your key>"
$env:MIMO_MODEL="<model>"
```

GLM、MiniMax、Kimi、MiMo、DeepSeek 均作为可配置 provider 路径记录，不硬编码未确认 endpoint。Claude 和 Gemini 目前保留接口和明确未实现提示，不伪造真实调用成功。

## 安全与脱敏

发布任何生成材料前运行：

```powershell
research-orbit audit-redaction --input examples --output outputs/redaction_report.md
```

禁止提交：

- 原始 COMSOL `.mph`、`.mphbin`；
- HDF5、NPZ、VTU、XDMF、PNG、GIF 等大型结果文件；
- API key、token、password、secret、证书；
- 未脱敏本机路径、账号、日志；
- `.local_private/` 下的申请材料。

## 本地私有申请材料

生成申请材料：

```powershell
research-orbit generate-application-pack --target mimo-orbit
```

默认输出：

```text
.local_private/application_pack/
```

该目录已被 `.gitignore` 忽略，不会提交到 GitHub。

## 仓库声明

本仓库采用“需要作者授权”的许可方式。它公开用于展示、审阅和归档，但不是 OSI 意义上的开源项目。任何使用、修改、商用、训练、二次分发或衍生工作，都必须获得作者本人明确授权。

请阅读：

- [LICENSE](LICENSE)
- [NOTICE.md](NOTICE.md)
- [USAGE_NOTICE.md](USAGE_NOTICE.md)
- [SECURITY.md](SECURITY.md)
- [PRIVACY.md](PRIVACY.md)
- [DISCLAIMER.md](DISCLAIMER.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)

## 开发

```powershell
python -m pip install -e ".[dev]"
ruff check .
pytest -q
research-orbit validate
research-orbit ui
```

CI 只使用 `dry-run`，不依赖真实 provider 凭据。

## 当前限制

- memory card 提取目前是确定性规则型，后续可加入更强语义抽取。
- OpenAI-compatible provider 需要用户提供 base URL、key 和 model。
- Claude/Gemini direct transport 尚未实现真实请求。
- 公开项目不直接解析原始 `.mph`，只处理脱敏结构化摘要。
- Web UI 当前是本地查看工作台，后续会加入 workflow 运行和历史记录。

## 路线图

- 增强 memory card 抽取、去重和合并。
- 增加 Claude/Gemini direct transport。
- 增加 UI 中的 dry-run workflow 执行按钮。
- 增加脱敏 COMSOL structured summary importer。
- 扩展 Word/MathType 安全检查与报告。
