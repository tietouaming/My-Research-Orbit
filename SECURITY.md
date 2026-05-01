# 安全策略

## 适用范围

当前安全策略覆盖 Research Orbit 的公开源码、CLI、workflow 定义、示例、文档、本地 redaction 审查和本地 application-pack 生成行为。

## 报告安全问题

不要在公开 issue 中贴出 secret、凭据、私有路径、未公开科研材料或原始模型文件。请通过 GitHub 联系仓库所有者，并先提供最小化、已脱敏的描述。

## 敏感材料规则

禁止提交：

- `.env`、`.env.*`、`.key`、`.pem`、`.token` 或凭据文件；
- API key、token、password、secret、账号或证书；
- 原始 `.mph`、`.mphbin`、HDF5、NPZ、VTU、XDMF、PNG、GIF 或大型求解器输出；
- 未脱敏本机路径、私有操作日志或私有申请包；
- 未公开研究模型或专有文档。

## 本地优先原则

默认 provider 是 `dry-run`，不会调用外部 API。真实 provider 必须通过环境变量显式配置。本地申请包默认写入 `.local_private/application_pack/`，并被 Git 忽略。

## 脱敏审查

发布任何生成内容前运行：

```powershell
research-orbit audit-redaction --input examples --output outputs/redaction_report.md
```

该审查只在本地运行，不上传文件。
