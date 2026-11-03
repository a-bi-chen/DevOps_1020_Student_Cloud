# A09 组 P5–P6 项目（E5–E10）

小组/轨道：A09 / A 轨道（P5 BuildChecker → P6 EChecker）

仓库：https://github.com/a-bi-chen/DevOps_1020_Student_Cloud

本 README 是 P6 阶段的初始化入口：先给出 **E7 的改动与成果摘要**，再给出 **E8–E10 的目标与概述**，最后说明 **组内每人应如何在自己的分支上完成并提交实验**。

## 1. 项目结构

仓库同时保留 P5 与 P6 的代码，两部分互不覆盖：

| 路径 | 阶段 | 内容 |
|---|---|---|
| `services/buildchecker/` | P5 | BuildChecker 服务、Dockerfile、单元测试 |
| `tests/e7/` | P5 | E7 独立 oracle |
| `scripts/` | P5 | `doctor.py`、`lab_cloud.py`、`run_e7_a_gate.py`、`secret_scan.py` 等 |
| `.github/workflows/e7-quality-gate.yml` | P5 | `e7-a-quality-gate` |
| `run_lab.py` | P6 | E8–E10 一键入口（`build` / `e8` / `e9` / `e10`） |
| `labs/e8e10/lab.py` | P6 | EChecker 教学实现（GCC 依赖观测、缓存复用/刷新、Patch） |
| `labs/e8e10/test_profile.py` | P6 | P6 单元测试（基础 7 项 + 各成员独立测试） |
| `labs/e8e10/environment/` | P6 | 教学实验镜像（Dockerfile、锁文件、BuildChecker、fixtures） |
| `.github/workflows/e8e10.yml` | P6 | `e8e10-quality-gate`（A/B 六条路线） |
| `docs/students/<学号>/e8-e10/` | P6 | 各成员个人报告、ADR、AI 使用记录 |
| `evidence/` | 共用 | 验收证据（E5–E7 与 E8–E10） |
| `work/` | 共用 | 运行产物，被 `.gitignore` 忽略，按需归档 |

## 2. E7 的改动与成果（摘要）

### 2.1 改动

- 在 BuildChecker 服务中实现 E5–E7 流程：真实构建采样、修复前后检测、E7 质量门禁。
- 新增“项目根边界”测试（PR #4）：防止 `../project-other/secret.h` 这类路径因字符串前缀相似被误当作项目内文件。
- 新增故意失败的 CI 演示与恢复记录（PR #3），验证“失败阻止合并、修复后恢复通过”。
- 配置 `main` 分支保护与必需检查 `e7-a-quality-gate`（Ruleset `25866762`）。

### 2.2 成果

| 项目 | 结果 |
|---|---|
| 构建与测试 | `17 passed`（原 15 项 + 失败演示 + 边界测试） |
| E7 gate | `8/8 passed`，`gate-result.json` 中 `"passed": true` |
| 独立 oracle | `6 tests OK` |
| secret scan | 源码与镜像两次扫描均未发现问题 |
| 最终镜像 | `course1020-buildchecker:241880369-final` |
| 镜像 digest | `sha256:6e12e90adbe1d3ff47d8f7f38e54186da0e4bf4411348d6db56e3dfe30eb332b` |
| 最终 main CI | run `40503459188`（`abaa94c`），success |

详细报告：`docs/实验报告.md`、`docs/reports/A09-final-status.md`、`docs/reports/A09-E7-boundary-test.md`、`docs/reports/A09-E7-failure-recovery.md`。

## 3. E8–E10 的目标与概述

本组走 **A 轨道 EChecker**。E8、E9、E10 是同一条证据链，不是三个互不相关的实验。

### 3.1 目标

| 实验 | 目标 |
|---|---|
| E8 | 在参考样例 C0 上建立真实基线：用真实 BuildChecker / GCC 观测实际依赖，与 Makefile 声明比较，输出 `MISSING` / `REDUNDANT`；未变化时复用历史图 |
| E9 | 跑通 C0→C1→C2→C3：函数体变化复用缓存；新增 include 触发刷新并新增 `MISSING`；补齐声明后相应 `MISSING` 进入 `resolved` |
| E10 | 六类变化（unchanged / body / include / declaration / flags / header）各 5 次，验证增量与全量的 `actual`、`declared`、`findings` 完全一致，并记录逐场景性能中位数 |

### 3.2 概述

- 教学实现位于 `labs/e8e10/lab.py`，入口为仓库根目录 `run_lab.py`，镜像名 `course-e8e10:<学号>`。
- 缓存 key 由本地 C/H 预处理指令、Makefile 配方、CFLAGS、编译器版本组成；key 变化时保守刷新两个对象目标。
- `labs/e8e10/test_profile.py` 当前包含基础 7 项测试与各成员的独立测试；新增测试应放在独立类中，避免覆盖他人。
- CI `.github/workflows/e8e10.yml` 构建教学镜像、运行单元测试，并执行 A/B 两轨各 E8/E9/E10 共六条路线。

### 3.3 复现命令

```bash
# 构建教学镜像（学号取本仓库 git config --local user.name）
python3 run_lab.py build

# 单条路线；--out 必须是 work/ 下尚不存在的新目录
python3 run_lab.py e8  --track A --out work/e8-A-<日期>
python3 run_lab.py e9  --track A --out work/e9-A-<日期>
python3 run_lab.py e10 --track A --out work/e10-A-<日期>

# Makefile 一键入口
make e8e10-build
make e8e10-test
make e8e10-lab
```

### 3.4 边界

- 教学实现只支持两个固定对象目标、顶层 C/H、显式规则、简单变量与受限 CFLAGS；不覆盖隐式规则、递归 Make 等。
- 不把论文中的 `85.14×` 或 MDFixer 的 `62.999s` 当作本组实测结果。
- E11–E12 的跨组联调不在 E8–E10 范围内，本阶段不声称已完成 E12。

## 4. 组内工作方式（每名成员）

1. **从最新 main 建个人分支**：`student/<学号>/e8-e10`，不直接改 main。
2. **按本轨道手册完整跑通 E8/E9/E10**：每个阶段使用 `work/` 下新的输出目录，保留命令、日志、JSON、OUT、被测源码 SHA 与镜像 ID；需要提交的运行结果单独归档。
3. **提交个人材料**：`docs/students/<学号>/e8-e10/` 下至少包含 `个人报告.md`、`ADR.md`、`AI_USAGE.md`。
4. **至少一项个人贡献**：增加一个**有独立预期**的测试（放在 `labs/e8e10/test_profile.py` 的独立测试类中），或完成一项实现改动；不得只复制他人用例。
5. **通过 PR 提交并保留证据**：PR headSha 应对应真实 Actions 运行；保存 artifact、CI 链接与最终合并 SHA。
6. **组内协作**：可以讨论、分工做扩展；每名成员只确认自己负责的内容，不代替他人签署结论。

当前已归档的个人材料在 `docs/students/2418800{89,369,374,375}/e8-e10/`；对应分支为 `student/2418800{89,369,374,375}/e8-e10`。

## 5. CI 与分支保护

- Ruleset `25866762`（`main`，active）要求两项必需检查：`e7-a-quality-gate`（P5，保留）与 `e8e10-quality-gate`（P6，新增），均来自 GitHub Actions（`integration_id: 15368`）。
- 规则包括：禁止删除、禁止非快进推送、必须通过 PR、分支需保持最新（strict）。
- 配置快照：`ci/A-main-protection.json`；P6 基础设施证据：`evidence/A09-E8-E10/241880089-github-infrastructure/`。

## 6. 文档索引

| 内容 | 位置 |
|---|---|
| E7 摘要 | 本 README 第 2 节；`docs/E7-summary.md` |
| E8–E10 目标与概述 | 本 README 第 3 节；`docs/E8-E10-overview.md` |
| P5 实验报告 | `docs/实验报告.md` |
| P5 详细报告 | `docs/reports/` |
| P6 个人报告 | `docs/students/<学号>/e8-e10/` |
| 课程操作手册 | `docs/00_开始与目录.md` … `docs/06_常见问题.md` |
