# Agent Workflows

Research Orbit 的 workflow 是结构化 YAML 文件，用来把科研 Agent 任务转化为可审计流程。

每个 workflow 至少包含：

- `name`
- `version`
- `description`
- `intended_user`
- `inputs`
- `outputs`
- `tools`
- `steps`
- `safety_rules`
- `success_criteria`
- `context_usage_pattern`
- `provider_requirements`
- `evidence_materials`

## 已有 Workflow

- `research_memory_compactor`：把日常 Agent 操作日志压缩成 memory cards。
- `word_mathtype_editor`：规划 Word/MathType 安全编辑，强调备份、修订和公式对象边界。
- `comsol_model_auditor`：审查脱敏 COMSOL structured summary，不凭记忆手抄模型。
- `simulation_porting_reviewer`：审查迁移证据，先 t=0 整场对齐，再短时烟测，再长时分析。
- `run_log_diagnoser`：对 solver、CI、Python 日志做证据优先归因。
- `application_pack_writer`：在本地私有目录生成申请材料。

## 运行方式

```powershell
research-orbit list-workflows
research-orbit run-workflow --workflow research_memory_compactor --input examples/sample_operation_log.md --output outputs/research_memory_report.md
```

默认 provider 是 `dry-run`，不会调用外部 API。
