"""Local private application pack generator."""

from __future__ import annotations

from pathlib import Path

from research_orbit.config import DEFAULT_APPLICATION_PACK_DIR
from research_orbit.schemas import ApplicationPack

SUPPORTED_TARGETS = {"mimo-orbit", "general-creator-program", "research-tool-grant"}


def generate_application_pack(
    target: str = "general-creator-program",
    output_dir: Path | None = None,
) -> ApplicationPack:
    if target not in SUPPORTED_TARGETS:
        known = ", ".join(sorted(SUPPORTED_TARGETS))
        raise ValueError(f"Unknown target `{target}`. Known targets: {known}")
    destination = output_dir or DEFAULT_APPLICATION_PACK_DIR
    destination.mkdir(parents=True, exist_ok=True)
    files = []
    for filename, content in _pack_files(target).items():
        path = destination / filename
        path.write_text(content, encoding="utf-8")
        files.append(path)
    return ApplicationPack(target=target, output_dir=destination, files=files)


def _pack_files(target: str) -> dict[str, str]:
    target_label = {
        "mimo-orbit": "Xiaomi MiMo Orbit 百万亿 Token 创造者激励计划",
        "general-creator-program": "通用 AI 创作者计划",
        "research-tool-grant": "科研工具资助计划",
    }[target]
    repository_url = "https://github.com/tietouaming/My-Research-Orbit"
    private_notice = "> 本文件为本地私有申请材料。不得提交 GitHub。\n"
    return {
        "00_README_FIRST.md": private_notice
        + f"""
# My Research Orbit 申请材料包

目标计划：{target_label}
项目名称：Research Orbit
申请主体：tietouaming
GitHub 仓库：{repository_url}

本申请包已整理为完整中文草稿，不包含需要补写的占位段。
涉及联系方式的部分使用公开 GitHub 账号与仓库链接表达，
避免写入未确认的私人信息。
""".lstrip(),
        "01_project_summary.md": private_notice
        + f"""
# 01 项目摘要

目标计划：{target_label}
项目名称：Research Orbit
申请主体：tietouaming
项目仓库：{repository_url}

Research Orbit 是面向科研人员的 Agentic Research OS。
它用于把日常 AI 协作中的论文编辑、公式处理、COMSOL 仿真模型审查、
代码迁移、错误日志归因、运行经验总结、多机归档和长期记忆管理，
沉淀为可复用、可审计、可扩展的 Agent 工作流系统。

项目已经具备独立 GitHub 仓库、Python package、CLI、本地 Web UI、
workflow YAML、memory card 生成器、多 provider 抽象、安全脱敏、
本地申请包生成器、测试、CI、示例输入输出和中文公开文档。
""".lstrip(),
        "02_technical_architecture.md": private_notice
        + """
# 02 技术架构

Research Orbit 使用轻量 Python 架构，包含 CLI 层、Schema 层、
Workflow 层、Provider 层、Redaction 层、Application Pack 层和 UI 层。

CLI 由 Typer 实现；结构化数据由 Pydantic 管理；workflow 使用 YAML。
provider 通过 dry-run、OpenAI 和 OpenAI-compatible 抽象接入。
redaction 全部本地运行；申请材料默认写入
`.local_private/application_pack/`；UI 使用标准库 HTTP server 和包内静态资源。

MiMo 作为 provider registry 中的 OpenAI-compatible route。
项目不硬编码未确认 endpoint，也不把 MiMo 写成公开项目唯一主体。
""".lstrip(),
        "03_context_and_token_usage_plan.md": private_notice
        + """
# 03 长上下文与 Token 使用计划

Research Orbit 的核心价值在长上下文科研 Agent 协作。
它读取历史运行总结，归纳多机 Agent 操作经验，审查长日志，
对齐科研 workflow，并生成申请材料和证明材料。

关键场景包括 Word/MathType 安全编辑、COMSOL structured summary 审查、
仿真迁移验证、solver/CI 日志归因、多机记忆合并和本地申请材料生成。
MiMo Orbit 的大规模 Token 能力适合支撑这种跨文档、跨工具、
跨时间线的科研 Agent OS 场景。
""".lstrip(),
        "04_github_proof_materials.md": private_notice
        + f"""
# 04 GitHub 证明材料

仓库：{repository_url}

公开仓库包含 Python package、CLI、本地 Web UI、workflow YAML、
provider 抽象、redaction 审查、application-pack 生成器、examples、
outputs、tests、docs、CI 和完整中文声明文件。

验证命令包括 `pytest -q`、`ruff check .`、`research-orbit validate`、
`research-orbit inspect`、`research-orbit providers`
和 `research-orbit ui --help`。
CI 使用 Python 3.11 与 dry-run，不依赖真实 API key。
""".lstrip(),
        "05_roadmap.md": private_notice
        + """
# 05 路线图

v0.1 已完成独立仓库、中文 README 与声明、Python package、CLI、
dry-run provider、多 provider 配置说明、6 个 workflow、memory card、
redaction、本地 application pack、Web UI、测试、示例、CI 和文档。

v0.2 计划加入 UI 中直接运行 dry-run workflow、workflow report 查看、
memory card 去重合并、redaction allowlist、JSON 输出和多机归档合并。

v0.3 计划加入 Claude/Gemini direct transport、
OpenAI-compatible 兼容测试、MiMo route 真实配置验证、
脱敏 COMSOL importer 和 Word/MathType 安全检查增强。
""".lstrip(),
        "06_application_form_draft.md": private_notice
        + f"""
# 06 申请表完整草稿

申请项目：{target_label}
项目名称：Research Orbit
申请主体：tietouaming
项目仓库：{repository_url}

Research Orbit 是一个面向科研人员的 Agentic Research OS。
它用于把日常 AI 协作中的论文编辑、公式处理、COMSOL 仿真模型审查、
代码迁移、错误日志归因、运行经验总结、多机归档和长期记忆管理，
沉淀为可复用的 Agent 工作流系统。

项目已经完成独立 GitHub 仓库、Python package、CLI、本地 Web UI、
workflow YAML、memory card 生成器、多 provider 抽象、安全脱敏、
本地申请包生成器、测试、CI、示例输入输出和中文公开文档。
它不是临时 demo，而是基于真实科研 Agent 协作经验形成的可继续扩展工程项目。

Research Orbit 的典型任务需要读取大量历史上下文，包括论文修改记录、
Word/MathType 操作约束、COMSOL 审查笔记、仿真迁移验证日志、
solver/CI 错误日志、多机 Agent 运行经验和长期项目记忆。
MiMo Orbit 的大规模 Token 能力适合支撑这种跨文档、跨工具、
跨时间线的科研工作流推理。

Research Orbit 公开可见不等于授权使用。
任何使用、复制、商用、训练、二次分发或改动本仓库，
均须获得作者本人明确授权。
""".lstrip(),
        "07_demo_script.md": private_notice
        + f"""
# 07 演示脚本

仓库：{repository_url}

```powershell
git clone {repository_url}.git
cd My-Research-Orbit
python -m pip install -e ".[dev]"
research-orbit inspect
research-orbit providers
research-orbit list-workflows
research-orbit validate
pytest -q
research-orbit ui --host 127.0.0.1 --port 8765
```

演示重点：独立仓库、中文说明、默认 dry-run、provider-neutral、
MiMo 只是多个 provider 之一、私有材料不提交 GitHub，
workflow/memory card/redaction/UI/CI 均可运行。
""".lstrip(),
        "08_review_checklist.md": private_notice
        + """
# 08 已完成检查清单

- [x] 独立仓库已创建。
- [x] README 与 docs 使用中文说明。
- [x] 声明、授权、安全、隐私、贡献、治理文件已补齐并中文化。
- [x] 公开项目主体是 Research Orbit。
- [x] MiMo 没有被写成公开项目唯一主体。
- [x] dry-run provider 可用。
- [x] openai-compatible provider 可用。
- [x] 本地申请材料只在 `.local_private/`。
- [x] `.local_private/` 被 Git 忽略。
- [x] 不提交原始 `.mph` 或大型仿真结果。
- [x] 不提交 API key、token、password、secret。
""".lstrip(),
    }
