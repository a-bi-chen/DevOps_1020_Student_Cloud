# 决策记录（ADR）

## 背景与约束

- A09 组在 P5（E5–E7）已配置 `main` 分支保护和 `e7-a-quality-gate` 必需检查，P6（E8–E10）必须保留该检查。
- 仓库为公开仓库，`main` 由 Ruleset `25866762` 保护：需要 PR、分支保持最新、必需检查通过。
- 本人负责 GitHub 基础设施、个人分支/PR/artifact 管理，以及一项独立的缓存失效测试；不替组员运行其个人路线。

## 选择与替代方案

### A. 如何新增 P6 必需检查

选择：先用 API GET 当前 Ruleset，确认 `e7-a-quality-gate` 存在后，再追加 `e8e10-quality-gate`，最后重新 GET 校验两项都在；不修改 `deletion`、`non_fast_forward`、`pull_request` 规则。

替代方案：直接 PATCH 覆盖整个 Ruleset。放弃原因：容易误删 E7 必需检查，无法满足“不能删除或覆盖原 E7 检查”的要求。

代价：更新脚本依赖 PAT，本次执行时未落盘；证据以 Ruleset 页面和 API 快照归档。

### B. 独立测试选择哪个缓存失效方向

选择：删除 `main.c` 中已有的 `#include "config.h"`，断言两个目标刷新、`MISSING main.o → config.h` 进入 `resolved`。

替代方案：再写一个“新增 include”测试。放弃原因：与张海洋 `StudentE9A`、高嘉程 `StudentE10A` 已有场景重复，不能体现本人独立贡献。

代价：删除 include 后实际依赖减少，仍采用保守刷新，无法验证“只刷新受影响目标”的优化。

### C. P6 代码如何与 P5 共存

选择：P6 代码放在 `labs/e8e10/`，入口为仓库根目录 `run_lab.py`，CI 为 `.github/workflows/e8e10.yml`；P5 的 `services/buildchecker/`、`tests/e7/`、`e7-quality-gate.yml` 原样保留。

替代方案：把 P6 代码并入 `services/buildchecker/`。放弃原因：会改动 P5 已验收的构建与门禁，风险大且不符合“根目录集成、不覆盖原 E5–E7 服务”的要求。

## 代价与覆盖范围

- 教学实现只支持两个固定对象目标、顶层 C/H、显式规则、简单变量与受限 CFLAGS；不覆盖隐式规则、递归 Make、符号链接等。
- E10 的 include/flags/header 场景采用保守刷新，增量与全量耗时接近；不引用论文的 `85.14×` 作为本人结果。
- E11–E12 的真实跨组联调不在本阶段范围内。

## 验证命令与实际证据

```text
# P6 单元测试（本地，含本人新增用例）
cd labs/e8e10 && python3 -m unittest discover -s . -p test_profile.py -v
# Ran 11 tests ... OK

# Ruleset 复核（公开 API）
GET https://api.github.com/repos/a-bi-chen/DevOps_1020_Student_Cloud/rulesets/25866762
# required: e7-a-quality-gate, e8e10-quality-gate
```

证据文件：

- `evidence/A09-E8-E10/241880089-github-infrastructure/README.md`
- `evidence/A09-E8-E10/241880089-github-infrastructure/241880089_e8e10_0*.png`
- `labs/e8e10/test_profile.py`（`StudentE8A089`）
