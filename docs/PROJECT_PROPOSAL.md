# 项目说明

Research Orbit 是面向科研人员的通用 Agentic Research OS。它的目标不是替代某个科学求解器，而是把日常 AI 协作中的论文编辑、公式处理、COMSOL 模型审查、仿真迁移、日志归因、多机记忆归档和长期项目经验，沉淀为可复用、可审计、可扩展的 Agent 工作流系统。

## 背景

科研人员与 AI Agent 协作时，经常遇到以下问题：

- 长对话中的关键经验难以复用；
- Word 和 MathType 编辑容易破坏公式对象；
- COMSOL 模型审查不能依赖记忆手抄公式；
- 仿真迁移需要明确验证顺序；
- solver、CI、Python traceback 日志很长，归因需要证据；
- 多台电脑同时工作时容易覆盖彼此产物；
- 申请材料、证明材料和私有记录需要与公开仓库严格隔离。

Research Orbit 把这些经验抽象为 workflow、memory card、redaction rule 和本地 application pack 生成器。

## 设计原则

- 通用科研 Agent 工作流系统，而不是单一材料体系项目；
- provider-neutral，而不是单一模型厂商项目；
- 默认 dry-run，可在无密钥和 CI 环境运行；
- 私有材料默认本地生成并忽略；
- 所有公开示例均保持小型、脱敏、可审查；
- 公开可见不等于授权使用。

## 当前完成度

项目已经包含 Python package、CLI、workflow YAML、memory card 生成器、provider 抽象、redaction 审查、本地申请包生成、Web UI、测试、示例、文档和 GitHub Actions CI。
