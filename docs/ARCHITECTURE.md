# 架构

Research Orbit 将公开可复用工作流基础设施与本地私有科研材料分离。

## 分层

1. CLI 层：`research-orbit` 提供 inspect、providers、memory-card 生成、workflow 执行、redaction 审查、application-pack 生成和 validate。
2. UI 层：`research-orbit ui` 从包内静态资源启动本地 Web 工作台，展示 workflow、provider 状态、示例 memory cards、redaction findings 和安全路径。
3. Schema 层：Pydantic 模型定义 memory card、workflow、provider config、redaction finding 和 application pack。
4. Workflow 层：YAML 描述 agent task、safety rule、success criteria、context usage pattern 和 evidence materials。
5. Provider 层：provider adapter 将模型调用与 workflow 逻辑隔离。`dry-run` 本地确定性运行；OpenAI-compatible provider 通过环境变量配置。
6. Safety 层：redaction 检查和 ignore 规则防止私有材料进入 Git。
7. Documentation 层：公开文档说明项目使用方式、provider 边界、安全边界、评估计划和本地申请包规则。

## 数据流

文本笔记或日志进入 CLI 后，memory-card generator 会分类并总结为结构化记录。workflow execution 加载 YAML spec，渲染 prompt，调用 provider，并输出 Markdown report。redaction audit 本地扫描文本，不调用外部 API。

Web UI 使用同一套本地项目 API 读取状态。它不读取 `.local_private/`，不显示 API key，也不调用外部模型。

Application-pack generation 是独立本地流程，默认写入 `.local_private/application_pack/`，该目录被 Git 忽略。

## 扩展点

- 在 `workflows/` 增加新 YAML；
- 在 `src/research_orbit/providers/` 增加 provider adapter；
- 在 `memory_cards.py` 增加分类规则；
- 在 `validators.py` 增加项目约束；
- 在 `src/research_orbit/ui_assets/` 增加 UI 面板；
- 在 `application_pack.py` 增加本地私有模板。
