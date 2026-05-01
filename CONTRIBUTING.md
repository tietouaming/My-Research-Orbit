# 贡献指南

欢迎在授权条款范围内提出 issue 或 pull request。提交 PR 不代表获得本项目的使用、商用、修改、训练、二次分发或衍生作品授权。

## 基本规则

- 公开项目必须保持 provider-neutral。
- 不得把 MiMo、OpenAI、Claude、Gemini、GLM、MiniMax、Kimi、DeepSeek 或任何单一 provider 写成项目唯一主体。
- 不得提交私有申请包或未脱敏操作记录。
- 不得提交原始 `.mph`、`.mphbin`、HDF5、NPZ、VTU、XDMF、PNG、GIF 或大型结果文件。
- 不得硬编码 API key、token、password、secret、账号或本机路径。
- 示例必须小型、脱敏、可公开。
- CI 优先使用 deterministic `dry-run`。

## 本地检查

```powershell
python -m pip install -e ".[dev]"
ruff check .
pytest -q
research-orbit validate
```

## PR 说明应包含

- 改动内容；
- 测试方式；
- 是否影响安全或 redaction 行为；
- 是否改变 provider 配置；
- 是否包含生成文件。

`.local_private/` 中的生成材料不得提交。
