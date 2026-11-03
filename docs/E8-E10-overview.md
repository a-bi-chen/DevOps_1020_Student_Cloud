# E8–E10 目标与概述

阶段：P6　小组/轨道：A09 / A（EChecker 教学实现）

本文件是 `main` 上 E8–E10 模板的一部分；个人材料按第 4 节在自己的分支提交，`main` 只保留 `docs/students/_template/`。

## 1. 总体目标

E8、E9、E10 构成一条连续证据链：先用真实观测建立依赖图基线，再验证增量扫描的缓存复用与失效，最后用六类变化矩阵核对增量与全量的一致性。所有结论必须来自本组真实运行，不引用论文数值冒充实测。

## 2. 各实验目标

### E8：真实基线

- 输入：参考样例 C0（`main.c` 包含 `config.h`，Makefile 声明 `main.o: main.c unused.h`）。
- 做法：用真实 BuildChecker（trace + Make 数据库）或 GCC `-MM` 观测实际依赖，与 Makefile 声明比较。
- 预期：`MISSING main.o → config.h`、`REDUNDANT main.o → unused.h`；输入未变化时两个对象目标复用历史图。
- 产出：`baseline.json`、`incremental.json`、BuildChecker 日志与 findings。

### E9：C0–C3 增量链

| 步骤 | 变化 | 预期 |
|---|---|---|
| C1 | 普通函数体变化 | 复用历史图，findings 不变 |
| C2 | 新增 `extra.h` include | 两个目标刷新，新增 `MISSING extra.h` |
| C3 | 在 Makefile 补齐声明 | 两项 `MISSING` 进入 `resolved`，保留 `REDUNDANT unused.h` |

产出：每一步的 build 日志、JSON、OUT、被测源码 SHA 与镜像 ID。

### E10：六类变化矩阵

- 六类场景：`unchanged`、`body`、`include`、`declaration`、`flags`、`header`，每类 5 次。
- 校验：每一行增量与全量的 `actual`、`declared`、`findings` 完全一致（`equal=True`）。
- 性能：记录每个场景的增量/全量耗时中位数与离散范围；教学实现下 include/flags/header 会保守刷新，增量与全量耗时接近。
- 产出：`matrix/`、`gate.json`、`performance-summary.csv`。

## 3. 代码与运行入口

| 文件 | 作用 |
|---|---|
| `run_lab.py` | 一键入口：`build` / `e8` / `e9` / `e10`，学号取本仓库 `git config --local user.name` |
| `labs/e8e10/lab.py` | 教学实现：依赖观测、缓存 key、增量/全量扫描、Patch 与保护 |
| `labs/e8e10/test_profile.py` | 单元测试；新增测试请使用独立测试类 |
| `labs/e8e10/environment/` | 教学镜像、BuildChecker、fixtures 与依赖锁文件 |
| `.github/workflows/e8e10.yml` | `e8e10-quality-gate`：单元测试 + A/B 六条路线 |

```bash
python3 run_lab.py build
python3 run_lab.py e8  --track A --out work/e8-A-<日期>
python3 run_lab.py e9  --track A --out work/e9-A-<日期>
python3 run_lab.py e10 --track A --out work/e10-A-<日期>
```

## 4. 每人交付物

```text
个人分支 student/<学号>/e8-e10
按本轨道手册完整跑通的 E8/E9/E10 运行结果（work/ 下独立目录，另行归档）
docs/students/<学号>/e8-e10/个人报告.md
docs/students/<学号>/e8-e10/ADR.md
docs/students/<学号>/e8-e10/AI_USAGE.md
至少一个独立测试（独立预期）或一项实现改动
PR、PR headSha 对应的 Actions URL、artifact
```

## 5. 约束

- 不直接修改 `main`；所有个人提交走 `student/<学号>/e8-e10` 分支与 PR。
- 新增测试放在独立测试类中，避免覆盖他人用例；测试必须有独立预期，不能只复制已有场景。
- 教学实现只支持两个固定对象目标、顶层 C/H、显式规则、简单变量与受限 CFLAGS。
- E11–E12 跨组联调不在本阶段范围；不声称已完成 E12。
- `work/` 被 Git 忽略；需要提交的运行结果应单独归档或按需 `git add -f`。
