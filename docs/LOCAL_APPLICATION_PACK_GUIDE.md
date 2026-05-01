# 本地申请包指南

Research Orbit 可以生成本地私有申请材料。生成结果不是公开项目内容，不应提交 GitHub。

## 默认目录

```text
.local_private/application_pack/
```

该目录已在 `.gitignore` 中忽略。

## 生成命令

```powershell
research-orbit generate-application-pack --target mimo-orbit
```

也支持：

- `general-creator-program`
- `research-tool-grant`

## 本地检查

```powershell
git check-ignore .local_private/application_pack/01_project_summary.md
research-orbit audit-redaction --input .local_private/application_pack --output .local_private/application_pack_redaction_report.md
```

## 规则

- 申请材料只在本地生成；
- 不自动提交；
- 不进入 GitHub；
- 提交外部申请前应确认没有 secret、私有路径和未公开科研材料。
