# E9 A 轨（EChecker 增量图）证据

- 来源：GitHub Actions run `41663999896`（push，success），headSha `5312b6d985c5cbb945cb6852bf488ba3dd5c2aef`。
- 执行位置：`ubuntu-24.04` + 教学镜像 `course-e8e10:ci`（ID 见 `environment-image-id.txt`）。
- 命令：`python3 labs/e8e10/lab.py e9 --track A --out /course/work/A-e9`。
- 产物：`baseline.json`（C0）、`C1.json`（函数体变化）、`C2.json`（新增 `#include "extra.h"`）、`C3.json`（修复 Makefile 声明），以及 C0/C1/C2 构建日志和源文件快照。

## 预期与结果

| 阶段 | 输入变化 | 预期 | 实际 |
|---|---|---|---|
| C1 | `main.c` 函数体 `VALUE+helper()` → `VALUE+helper()+0` | 预处理指令/配方不变，复用 `main.o`、`helper.o` | `reused=[main.o,helper.o]`、`refreshed=[]`、`added=[]`、`resolved=[]` |
| C2 | 新增 `#include "extra.h"` | 变化签名改变，保守刷新两个目标；新增 `MISSING main.o extra.h` | `refreshed=[main.o,helper.o]`、`added=[["MISSING","main.o","extra.h"]]` |
| C3 | Makefile 声明补上 `config.h extra.h` | 声明变化不改变构建配方，复用历史图；两条 MISSING 被消除 | `reused=[main.o,helper.o]`、`resolved` 含 `config.h` 与 `extra.h`，仅剩 `REDUNDANT unused.h` |

## 结论

E9 A 轨通过：增量扫描在 C1 正确复用、在 C2 正确失效、在 C3 正确复用并计算新增/消除集合。`C3.json` 的 actual 图包含 `main.c → config.h/extra.h`，declared 图与之一致（除未使用的 `unused.h`）。

独立复核见 `work/e8e10-A-verification/`：在同一棵树上用 `scan(p, prev)` 与全量 `scan(p)` 对照，C1–C3 的 `actual`/`declared`/`findings` 全部相等。
