# E8–E10 A 轨两次独立检验

本目录记录两次相互独立的检验，用来确认 A 轨结果不是单一实现路径或单次运行的偶然产物。两次检验都只使用 A 轨数据；B 轨产物不参与结论。

## 检验一：方法独立（增量 vs 全量、BuildChecker vs GCC）

| 对象 | 独立对照 | 结果 |
|---|---|---|
| E8 | 真实 BuildChecker 的 `actual-graph.json` / `findings.json` 对照同一 C0 树的 `baseline.json` 与全新 GCC `-MM` 扫描 | 依赖图与 findings 三方完全一致：`MISSING main.o config.h`、`REDUNDANT main.o unused.h` |
| E9 | 同一棵树上 `scan(p, prev)` 与全量 `scan(p)` 对照，覆盖 C1/C2/C3 | 三阶段 `actual`/`declared`/`findings` 全部相等；C1 复用、C2 刷新、C3 复用并消除两条 MISSING |
| E10 | `results.csv` 的 30 行逐行检查增量/全量 `equal`；终态 BuildChecker 对照全新 GCC 扫描 | 30/30 行 `equal=True`；终态依赖图与 findings 一致，仅 `REDUNDANT main.o unused.h` |

证据文件：

- `check1-method/e9-incremental-vs-full.json`
- `check1-method/e8-e10-buildchecker-vs-gcc.json`

## 检验二：运行独立（同一提交的两次 CI 运行）

| 项目 | 运行 1 | 运行 2 |
|---|---|---|
| Actions run | `41663999896`（push） | `41666559898`（workflow_dispatch） |
| headSha | `5312b6d985c5cbb945cb6852bf488ba3dd5c2aef` | 同左 |
| 结论 | success | success |

比较时去掉每次运行必然变化的字段：样例内部 git `commit`、`elapsed_s`/`elapsed_ms`、BuildChecker `trace_id`、trace 的 PID/行号。其余语义字段逐项比较：

- E8：`baseline`、`incremental`、BuildChecker findings/actual graph；
- E9：`baseline`、`C1`、`C2`、`C3`；
- E10：`baseline` 与六个场景 JSON、30 行 `results.csv` 的结构/`equal`/缓存行为、`gate.json`、终态 BuildChecker findings/actual graph。

结果：`check2-rerun/summary.json` 中 `passed=true`，`differences=[]`；两次运行的 A 轨语义结果完全相同。

## 复现命令

在仓库根目录执行（Linux 或带 `make`/`gcc`/`git` 的环境）：

```bash
# 检验一：E9 增量 vs 全量（会新建临时 fixture）
python3 -I work/e8e10-A-verification/scripts/e9_method_check.py . /tmp/e9-check

# 检验一：E8/E10 的 BuildChecker vs GCC（artifact 目录需先解压）
python3 -I work/e8e10-A-verification/scripts/e8_e10_method_check.py . \
  /path/to/e8e10-evidence-41663999896/all /tmp/e8e10-check

# 检验二：两次 artifact 的语义比较
python3 -I work/e8e10-A-verification/scripts/rerun_compare.py \
  /path/to/run1/all /path/to/run2/all /tmp/rerun-check
```

本次检验一在 Windows + MinGW gcc 14.2.0 + GNU Make 4.4.1 上执行，使用 `mingw32-make` 的 `make` 别名；E8/E10 的 BuildChecker 侧数据来自 CI 教学镜像。检验二完全使用 CI artifact，不依赖本地构建。

## 结论

两次检验均通过。E8–E10 A 轨的增量结果与全量结果一致，真实 BuildChecker 与 GCC 投影一致，且同一提交的两次独立 CI 运行给出相同语义结果。

## 边界

- 运行独立检验对应 headSha `5312b6d`，早于最终 PR head `3afc345`；它没有覆盖最终提交。
- 第 4 个个人测试（删除已有 include）是在最终 CI `41667606590` 之后新增的，目前仅在本地通过 11 项，未被本目录的两次 CI 检验覆盖。
- 本目录的结论只针对 A 轨；B 轨和 A→B 交接均未执行，不能引用本目录声称已完成。
