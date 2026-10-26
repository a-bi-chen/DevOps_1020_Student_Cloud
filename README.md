# A-buildchecker 云主机实验

本目录是可运行的教学参考实现，已合并 E6/E7 代码，未包含助教门禁演示测试。
请先阅读实验包 docs/00_开始与目录.md，再按 02_A轨道操作指南.md 完成步骤。
统一入口：`python3 scripts/lab_cloud.py --help`。
不需要 Windows、WSL、Docker Desktop，不使用助教的学号、代理地址或宿主机目录。
仓库旧 Makefile/Compose 属于 E4 环境接口；本次优先使用 lab_cloud.py，避免镜像标签混用。
# E5–E7：论文复现、MVP 与验证

在本组云服务器上完成实验。A 组进行 BuildChecker 依赖检测，B 组进行 DRAFT 构建修复。

## 包里有什么

|目录|内容|
|---|---|
|labs/A-buildchecker/|A 组代码、样例与测试|
|labs/B-draft/|B 组代码、样例、Dockerfile 候选与测试|
|docs/|环境准备、分组操作、CI、验收清单和常见问题|
|ci/|分支保护配置、失败测试和修复后的测试|
|templates/|实验报告、验收记录、候选来源记录|

## 操作顺序

1. 按 docs/01_云主机环境与上传.md 准备目录和工具。
2. A 组按 docs/02_A轨道操作指南.md，B 组按 docs/03_B轨道操作指南.md 操作。
3. 按 docs/04_GitHub_CI与合并门禁.md 完成 CI 和合并测试。
4. 按 docs/05_验收清单.md 整理报告与结果。

命令在 SSH 登录后的服务器终端执行。每个代码框可整块复制，按顺序运行；终端输出用于核对结果。

