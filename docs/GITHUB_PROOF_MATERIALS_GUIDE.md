# GitHub 证明材料指南

公开证明材料应展示 Research Orbit 是真实可运行项目，同时避免泄露私有科研材料。

## 可以展示

- README、docs、workflow YAML；
- Python package 与 CLI；
- tests 与 CI；
- 脱敏 examples；
- 公开 outputs；
- provider-neutral 架构说明；
- redaction 与 `.gitignore` 安全规则。

## 不得展示

- `.local_private/` 申请材料；
- 原始 `.mph`、`.mphbin`、HDF5、NPZ、VTU、XDMF、PNG、GIF；
- 真实 API key、token、password、secret；
- 未脱敏路径和操作日志；
- 未公开科研模型细节。

## 推荐证明命令

```powershell
research-orbit inspect
research-orbit providers
research-orbit list-workflows
research-orbit validate
pytest -q
```
