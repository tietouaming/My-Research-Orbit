# 评估计划

Research Orbit 评估的是科研工作流系统质量，而不是某个科学求解器的数值精度。

## 当前可验证项

- CLI 命令是否可运行；
- workflow YAML 是否字段完整；
- memory card 是否包含必要结构；
- provider registry 是否不泄露 key；
- redaction 是否能发现敏感模式；
- `.local_private/` 是否被忽略；
- CI 是否能在 Python 3.11 下通过；
- Web UI 是否能读取真实项目状态。

## 自动测试

```powershell
pytest -q
ruff check .
research-orbit validate
```

## 后续评估

- 为每个 workflow 增加 expected report fixture；
- 增加 memory card 抽取准确率检查；
- 增加 redaction false positive/false negative 样例；
- 增加 provider-compatible 请求构造测试；
- 增加 UI 状态快照测试。
