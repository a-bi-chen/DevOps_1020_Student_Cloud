# E10 A 轨（六场景一致性/性能）证据

- 来源：GitHub Actions run `41663999896`（push，success），headSha `5312b6d985c5cbb945cb6852bf488ba3dd5c2aef`。
- 执行位置：`ubuntu-24.04` + 教学镜像 `course-e8e10:ci`（ID 见 `environment-image-id.txt`）。
- 命令：`python3 labs/e8e10/lab.py e10 --track A --out /course/work/A-e10`。
- 产物：`results.csv`（6 场景 × 5 次，共 30 行）、六个场景 JSON、`gate.json`、`final-buildchecker/`（真实 BuildChecker 终检）与源文件快照。
- 本地汇总：`performance-summary.csv`（每场景 n、增量/全量中位数、增量最小/最大值、全量/增量比）与 `结论.txt`。两者均由 `results.csv`、`gate.json` 和终态 BuildChecker 产物计算/整理，未改写 CI 原始数字。

## 场景矩阵

| 场景 | 变化 | 预期缓存行为 | 实际（每行相同） |
|---|---|---|---|
| `unchanged` | 无 | 复用两个目标 | `reused=2`、`refreshed=0` |
| `body` | `helper.c` 函数体 | 复用两个目标 | `reused=2`、`refreshed=0` |
| `include` | `main.c` 新增 `#include "extra.h"` | 保守刷新两个目标 | `reused=0`、`refreshed=2` |
| `declaration` | Makefile 声明补 `config.h extra.h` | 复用历史图 | `reused=2`、`refreshed=0` |
| `flags` | `-O0` → `-O1` | 配方/标志变化，刷新两个目标 | `reused=0`、`refreshed=2` |
| `header` | `config.h` 间接包含 `extra.h` | 预处理指令变化，刷新两个目标 | `reused=0`、`refreshed=2` |

## 一致性与性能

- `results.csv` 30 行全部 `equal=True`：每个场景的增量报告与全量 `scan(p)` 在 `actual`、`declared`、`findings` 上逐字段相等。
- `gate.json` 为 `{"track":"A","passed":true,"rows":30}`。
- 中位耗时（CI 容器内，单次，精确值见 `performance-summary.csv`）：复用路径约 0.0026 s（增量）对约 0.017 s（全量），比值约 6.5–6.6；刷新路径增量约 0.017 s，与全量同量级（比值约 0.99–1.00），符合“保守刷新”的设计。
- `final-buildchecker/findings.json`：`status=SUCCEEDED`、`clean/build` 退出码 0，终态仅 `REDUNDANT main.o unused.h`，与 GCC 投影一致。

## 产物布局说明

- 顶层是 CI 一键入口的原始归档：六个场景 JSON、`results.csv`、`gate.json` 和 `final-buildchecker/`。
- `matrix/` 是为对齐操作手册布局而创建的重组副本，内容逐字节来自顶层，不是第二次运行；详见 `matrix/README.md`。
- CI 只保留每个场景重复 5 次后的末次 JSON，逐次记录在 `results.csv` 中，没有另外保存 5 份成对 JSON。`matrix/` 也不补造逐次文件。

## 结论

E10 A 轨通过：六类变化下增量与全量结果完全一致，缓存复用/失效方向符合预期；最终真实 BuildChecker 交叉检查通过。文字版结论见 `结论.txt`，精确性能数值见 `performance-summary.csv`。

独立复核见 `work/e8e10-A-verification/`：30 行 gate 逐行复核，并把终态 BuildChecker 图与本地全新 GCC 扫描对照，`actual` 与 `findings` 均相等。
