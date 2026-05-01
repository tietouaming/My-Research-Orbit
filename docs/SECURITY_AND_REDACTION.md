# 安全与脱敏

Research Orbit 假设科研工作中包含私有文档、未公开模型、真实路径、日志和密钥，因此默认采用本地优先和最小公开原则。

## 禁止提交

- 原始 `.mph` 或 `.mphbin`；
- HDF5、NPZ、VTU、XDMF、PNG、GIF 或大型 solver/result 文件；
- 账号、密码、token、API key、secret、证书；
- 完整本机绝对路径；
- 未脱敏操作日志；
- `.local_private/` 下的本地申请材料。

## Redaction Audit

运行：

```powershell
research-orbit audit-redaction --input examples --output outputs/redaction_report.md
```

该命令只在本地扫描，不上传、不调用外部 provider。

## 检测类型

- Windows 路径；
- Unix 路径；
- API key、token、secret、password、authorization；
- 邮箱；
- 手机号；
- `.mph`、`.mphbin`、`.h5`、`.hdf5`、`.npz`、`.vtu`、`.xdmf`、`.png`、`.gif`、`.pem`、`.key`、`.token`、`.env` 等扩展名。

## 授权原则

公开可见不等于授权使用。任何使用、复制、商用、训练、二次分发或改动本仓库，均须获得作者本人明确授权。
