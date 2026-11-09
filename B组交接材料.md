# B 组交接材料（A09 / 陈玉熙 / 241880089）

- 提供方：A 轨 A09（EChecker）
- 接收方：B 组负责人
- 生成日期：2026-11-09
- 用途：核对项目版本、构建配置、真实 MD 报告、检测证据和重检方式。
- 边界：本文件是**材料索引**，不是签收单。正式 A→B 交接以双方负责人确认的记录为准；截至本文生成时，B 组返回文件与验收结论尚未回填（见第 7 节）。

## 0. 速查

| 项目 | 值 |
|---|---|
| 仓库 | https://github.com/a-bi-chen/DevOps_1020_Student_Cloud |
| 分支 | `student/241880089/e8-e10` |
| 代码/证据基线 SHA | `489158f2636b5f83c46b253c68469a63291d8a62` |
| 文档提交 | 以 `git log -1 --format=%H -- B组交接材料.md` 为准（仅文档变更，不改变代码/证据） |
| 当前工作区 | clean（`git status --porcelain` 为空） |
| E8 受测项目根目录 | `work/e8-A-ci-41662015872/project/` |
| Makefile | `work/e8-A-ci-41662015872/project/Makefile` |
| 构建命令 | `make app`；清理 `make clean` |
| 编译器 | `gcc (Debian 14.2.0-19) 14.2.0`，`CFLAGS = -O0` |
| 最小格式 MD 报告 | `work/e8-A-ci-41662015872/baseline.json` |
| 检测状态 | `work/e8-A-ci-41662015872/buildchecker/findings.json` → `SUCCEEDED` |
| 原始检测证据 | `work/e8-A-ci-41662015872/buildchecker/` |
| 重检入口 | `python3 labs/e8e10/lab.py e8 --track B --out <新目录>` |

> 本文所有 `work/...` 路径均相对于仓库根目录。CI 容器内的输出目录是 `/course/work/A-e8`，下载 artifact 后归档为 `work/e8-A-ci-41662015872/`。

## 1. 项目及版本

### 1.1 仓库、分支、提交

- 仓库地址：`git@github.com:a-bi-chen/DevOps_1020_Student_Cloud.git`
- 网页地址：https://github.com/a-bi-chen/DevOps_1020_Student_Cloud
- 分支：`student/241880089/e8-e10`
- 代码/证据基线 SHA：`489158f2636b5f83c46b253c68469a63291d8a62`
- 文档提交：以 `git log -1 --format=%H -- B组交接材料.md` 为准；该提交只增加/修改文档，不改变代码与 E8–E10 证据
- 远端分支 HEAD：可能比代码基线多一个仅文档提交，可用 `git ls-remote origin student/241880089/e8-e10` 查询
- 当前工作区：clean，无未提交修改

### 1.2 检测版本与当前版本的对应（重要）

2026-11-09 为统一提交者身份，使用 `git filter-repo --mailmap` 改写了本分支历史。改写只改变 author/committer，不改变文件树。新旧 SHA 的对应关系如下：

| 证据中记录的旧 SHA | 当前分支中的等价 SHA | tree |
|---|---|---|
| `77e891c4da81b40f14a75045829b637e1444dbe7` | `a0802185e793f2de7e6290edbfb8c7760a819b91` | `fccd31a3f3f7aa90e91f8df1a02faad910207b66` |
| `5312b6d985c5cbb945cb6852bf488ba3dd5c2aef` | `74ca22ea7b8756523ecb2853d422eef7e28df93f` | `1cb7497c70a594392e899f30849e6933499693c4` |
| `3afc3453907aa1ca6b8d4b126595b4cf51378649` | `1aa63dc611b7ef56cd61e96a4c5bee6aa10661bc` | `7095858daa6047948c5d51519bc2364230d5b295` |
| `65196e35a7a96c02b10649c294f3f9e1acf4823f` | `489158f2636b5f83c46b253c68469a63291d8a62` | `f8e47adac663c5fd70527a1c8c9a2000434534bc` |

说明：

- `work/e8-A-ci-41662015872/student-source-commit.txt` 中记录 `outer_commit=77e891c...`，在当前分支中对应 `a080218...`。
- `a080218`、`74ca22e`、`1aa63dc` 都是 `489158f` 的祖先；B 组按 SHA 取用时，用右列的新 SHA。
- `labs/e8e10/lab.py` 与 `run_lab.py` 在 `77e891c` 和 `489158f` 之间未变化；检测逻辑相关文件中，`labs/e8e10/test_profile.py` 新增了第 4 个个人测试，`.github/workflows/e8e10.yml` 增加了 `include-hidden-files: true`。也就是说，**产生 E8 检测结果的逻辑与当前分支一致**，但 `489158f` 本身尚无已归档的 CI artifact。

### 1.3 对应项目文件

E8 受测 C0 fixture 位于：

```text
work/e8-A-ci-41662015872/project/
├── Makefile
├── main.c
├── helper.c
├── config.h
├── extra.h
└── unused.h
```

fixture 由 `labs/e8e10/lab.py:14` 的 `fixture()` 生成。上表文件在 Git blob（LF 行尾）中的 SHA-256 与 `buildchecker/findings.json` 的 `input_sha256` 一致：

| 文件 | SHA-256 |
|---|---|
| `Makefile` | `9206301c23ce4cb93c3fc1434037e475cf69f53e132dc541f6028d05e30258b2` |
| `main.c` | `0da2f94ca7b27cfeae51e4842a4a39f527929b28a82f40b3796d308cc72c1379` |
| `helper.c` | `90a60f959d215b0b91807c6dd2c94acf6684a9fe26629dc1591e9b2ea773d78c` |
| `config.h` | `ac32a92f4af359517c993d6e8583ea2d9b053c2ad171b4c602bc242894bd9696` |
| `extra.h` | `5e20ae92639ee989af5638bd0308a6a86e71bdb4345f60b962ba9db7265e4f7c` |
| `unused.h` | `3f7fec0991b34d614462e29b450c76638f07171936a12df337c578c2d1481b37` |

校验时建议直接对 Git blob 计算，避免 Windows `core.autocrlf=true` 把 LF 转成 CRLF：

```bash
git show HEAD:work/e8-A-ci-41662015872/project/main.c | sha256sum
```

`input_sha256` 中还包含 `.gitignore`（`d7bfd391...`），但该隐藏文件未被归档，仓库中也无法取得，无法复核；它是 fixture 的忽略规则，不参与 MD 判定。

### 1.4 检测时是否有未提交修改

- 检测在 GitHub Actions 的 `actions/checkout` 工作区中执行，机制上为干净检出。
- 现有 artifact 中没有归档 `git status --porcelain` 的空输出，因此严格说，仓库内没有一份“检测时 clean”的独立证据；能证明版本对应关系的是 `student-source-commit.txt`、`input_sha256` 和上述 SHA 映射。
- 当前仓库工作区已确认 clean。

## 2. 构建配置

| 项目 | 值 |
|---|---|
| 项目根目录 | `work/e8-A-ci-41662015872/project/` |
| 构建目录 | 同项目根目录（原地构建） |
| Makefile 路径 | `work/e8-A-ci-41662015872/project/Makefile` |
| 默认目标 | `app`（Makefile 中第一个目标） |
| 其他目标 | `main.o`、`helper.o`、`clean`（`.PHONY`） |
| 完整构建命令 | `make app` |
| 清理命令 | `make clean` |
| 编译器 | `gcc (Debian 14.2.0-19) 14.2.0` |
| 编译参数 | `CFLAGS = -O0` |
| 编译命令 | `gcc $(CFLAGS) -c main.c -o main.o`、`gcc $(CFLAGS) -c helper.c -o helper.o` |
| 链接命令 | `gcc main.o helper.o -o app` |
| 生成文件 | `main.o`、`helper.o`、`app` |
| 运行环境 | `ubuntu-24.04` + 镜像 `course-e8e10:ci`（`sha256:c76ea6c17331defaa9c67302b1ebcfa0510706e0df2dbd52bcffb4db1c197894`） |
| 前置工具 | `make`、`gcc`、`git`；完整检测另需 `strace` 与 BuildChecker（镜像内 `/app`） |

Makefile 原文：

```make
CFLAGS = -O0
app: main.o helper.o
	gcc main.o helper.o -o app
main.o: main.c unused.h
	gcc $(CFLAGS) -c main.c -o main.o
helper.o: helper.c
	gcc $(CFLAGS) -c helper.c -o helper.o
.PHONY: clean
clean:
	rm -f main.o helper.o app
```

复现构建：

```bash
cd work/e8-A-ci-41662015872/project
make clean
make app
./app        # 输出 1
```

如需在 CI 同款环境中复现，使用 `course-e8e10:ci` 镜像；普通 Linux 上只要 `gcc`/`make` 版本兼容即可完成构建，但 BuildChecker 的 strace 证据应在教学镜像中重跑。

## 3. 真实 MD 报告

E8 的真实检测结果分成两个 JSON，各有分工；仓库里**没有**一份同时包含“外层提交 + 检测状态 + findings”的单一 JSON。

### 3.1 最小格式报告：`baseline.json`

路径：`work/e8-A-ci-41662015872/baseline.json`

关键字段：

| 字段 | 值 |
|---|---|
| `schema_version` | `e8e10-1` |
| `profile` | `GCC_LOCAL_HEADERS_EXPLICIT_MAKE` |
| `commit` | `f4d0e190a47172f736f05bd20d49fe68b3a7127a`（fixture 内部 C0 提交，不是外层分支 SHA） |
| `actual["main.o"]` | `["config.h", "main.c"]` |
| `actual["helper.o"]` | `["helper.c"]` |
| `declared["main.o"]` | `["main.c", "unused.h"]` |
| `declared["helper.o"]` | `["helper.c"]` |
| `findings` | 见下 |
| `added` | 初始扫描相对空历史，等于两条 findings |
| `resolved` | `[]` |
| `refreshed` | `["main.o", "helper.o"]` |
| `reused` | `[]` |
| `baseline_source` | `BuildChecker actual-graph.json projected to object targets` |

`findings` 原文：

```json
[
  {"type": "MISSING", "target": "main.o", "dependency": "config.h"},
  {"type": "REDUNDANT", "target": "main.o", "dependency": "unused.h"}
]
```

这与 B 组固定报告格式完全一致。

### 3.2 检测状态与原始 BuildChecker 报告：`findings.json`

路径：`work/e8-A-ci-41662015872/buildchecker/findings.json`

关键字段：

| 字段 | 值 |
|---|---|
| `status` | `SUCCEEDED` |
| `detector` | `BUILDCHECKER_TEACHING` |
| `detector_version` | `0.2.0-teaching` |
| `trace_id` | `e6-b2bf9da5e8d04381b5624faafc08e6e7` |
| `elapsed_ms` | `280` |
| `build_command` | `["make", "app"]` |
| `clean_command` | `["make", "clean"]` |
| `build_exit_code` / `clean_exit_code` | `0` / `0` |
| `observed_targets` | `["app", "helper.o", "main.o"]` |
| `scope` | `Single Make process; one final output per recipe job; successful read-open observations` |

该报告的 `findings` 是 `baseline.json` 的超集：同样保留 `type` / `target` / `dependency`，另带 `evidence`、`declared_dependencies`、`scope` 等字段，例如：

```json
{"type": "MISSING", "target": "main.o", "dependency": "config.h",
 "evidence": [{"source": "system_call", "trace_file": "t.28", "line": 579, "pid": 28, "operation": "openat"}, ...],
 "declared_dependencies": ["main.c", "unused.h"]}
```

### 3.3 B 组字段对照

| B 组字段 | 仓库中的来源 |
|---|---|
| `commit` | `baseline.json` 的 `commit` 是 fixture 内部提交 `f4d0e19`；外层学生源码版本用 `a080218`（旧 `77e891c`）或代码基线 `489158f` |
| `type` / `target` / `dependency` | `baseline.json` 的 `findings`，或 `buildchecker/findings.json` 的 `findings` |
| 报告版本 | `baseline.json` 的 `schema_version: e8e10-1`；检测器版本为 `detector_version: 0.2.0-teaching` |
| 检测状态 | `buildchecker/findings.json` 的 `status: SUCCEEDED`（以及两个 exit code 均为 0） |

### 3.4 路径基准

- `work/...` 路径相对于仓库根目录。
- `buildchecker/findings.json` 的 `artifacts.*` 相对于 `work/e8-A-ci-41662015872/buildchecker/`。
- `baseline.json` 的 `commit` 相对于 fixture 项目内的 `project/.git`。
- `trace_command` 中的 `/course/work/A-e8/...` 是 CI 容器路径；归档后对应 `work/e8-A-ci-41662015872/...`。

### 3.5 已知限制

1. `project/.git` 未归档。生成 artifact 时 workflow 未设置 `include-hidden-files: true`，所以 fixture 的 `commit: f4d0e19` 不能从仓库直接验证。当前 workflow 已补该设置，但尚未重跑。
2. 没有外层 commit 与检测状态合一的 JSON；需要同时引用 `baseline.json` 和 `buildchecker/findings.json`。
3. `489158f` 尚无归档 CI artifact；现有 E8 报告对应 `77e891c`（等价 `a080218`）。
4. `.gitignore` 未归档，其 `input_sha256` 无法复核；其余 6 个文件的哈希可按第 1.3 节验证。

## 4. 检测证据

### 4.1 本次检测命令

```bash
# CI 容器内，工作目录 /course
python3 labs/e8e10/lab.py e8 --track A --out /course/work/A-e8
```

对应 GitHub Actions run `41662015872`，headSha `77e891c`（当前分支等价 `a080218`）。

原始 trace 命令（来自 `findings.json`）：

```json
["strace","-ff","-s","4096","-o","/course/work/A-e8/buildchecker/trace/t",
 "-e","trace=%file,%process","make","-p","app"]
```

### 4.2 证据位置

| 证据 | 路径 | 用途 |
|---|---|---|
| 最小格式报告 | `work/e8-A-ci-41662015872/baseline.json` | 图、findings、增量复用 |
| 增量复扫 | `work/e8-A-ci-41662015872/incremental.json` | 未变化 C0 的 reused/refreshed |
| BuildChecker 报告 | `work/e8-A-ci-41662015872/buildchecker/findings.json` | 状态、exit code、findings、input 哈希 |
| 实际依赖图 | `work/e8-A-ci-41662015872/buildchecker/actual-graph.json` | strace 观测到的边 |
| 声明依赖图 | `work/e8-A-ci-41662015872/buildchecker/declared-graph.json` | Makefile 声明的边 |
| Make 数据库 | `work/e8-A-ci-41662015872/buildchecker/make-db.txt` | `make -p` 原始数据库 |
| 进程记录 | `work/e8-A-ci-41662015872/buildchecker/processes.json` | 进程树/作业 |
| 原始 trace | `work/e8-A-ci-41662015872/buildchecker/trace/t.26` 至 `t.35` | 文件/进程系统调用 |
| 清理日志 | `work/e8-A-ci-41662015872/buildchecker/clean.log`、`clean-stderr.log` | clean 阶段 |
| 构建日志 | `work/e8-A-ci-41662015872/buildchecker/build-stderr.log` | 构建阶段 |
| 版本记录 | `work/e8-A-ci-41662015872/student-source-commit.txt` | 外层/fixture 提交 |
| 环境记录 | `work/e8-A-ci-41662015872/environment-image-id.txt` | 镜像、runner、编译器 |
| 结论摘要 | `work/e8-A-ci-41662015872/结论.txt` | E8 结论 |

### 4.3 E9/E10 补充证据

B 组如需查看同一实现的其他实验，补充材料在：

| 实验 | 目录 | 内容 |
|---|---|---|
| E9 | `work/e9-A-ci-41663999896/` | C0/C1/C2/C3 JSON、构建日志、快照 |
| E10 | `work/e10-A-ci-41663999896/` | 30 行 `results.csv`、六场景 JSON、`gate.json`、终态 BuildChecker |
| 独立检验 | `work/e8e10-A-verification/` | 增量/全量对照、两次 CI 语义比较 |

E9/E10 的 headSha 为旧 `5312b6d`（当前分支等价 `74ca22e`）。E8 的 MD 修复与重检只需使用第 1–4 节材料。

## 5. 后续重检方式

### 5.1 仓库内的修复与验证机制

`labs/e8e10/lab.py` 已实现 B 轨所需的两个关键函数：

- `patch()`（`labs/e8e10/lab.py:76`）：
  - 报告 `commit` 与 fixture 当前 HEAD 不一致 → `STALE_REPORT`
  - 依赖路径包含 `..` 或绝对路径 → `UNSAFE_PATH`
  - 依赖文件不存在 → `MISSING_INPUT`
  - 只为 `MISSING` 生成 Makefile 补丁，保留 `REDUNDANT`
- `validate()`（`labs/e8e10/lab.py:97`）：
  - 复制沙箱（忽略 `.git`、`*.o`、`app`）
  - `git apply --check` → `git apply`
  - `make clean` + `make app`
  - 运行 `./app` 校验输出
  - 修改 `config.h` 后再次 `make app`，验证原先的增量构建缺陷已修复
  - 重新 `scan()` 生成 `recheck.json`，检查不再有 `MISSING`
  - 写 `validation.json`；任一步失败则回滚，源 `Makefile` 不变

### 5.2 B 轨命令

```bash
# 在仓库根目录；<out> 必须是尚不存在的新目录
python3 labs/e8e10/lab.py e8 --track B --out work/B-e8-recheck
```

产物：

| 文件 | 含义 |
|---|---|
| `fixed-md-report.json` | 输入报告的副本 |
| `candidate.patch` | 根据 `MISSING` 生成的 Makefile 补丁 |
| `expected-failure.json` | 使用过期报告时应触发的 `STALE_REPORT` |
| `validation.json` | 补丁是否应用、构建/运行/增量重检/回滚结果 |
| `recheck.json` | 修复后的重新扫描结果（位于 validation 证据目录下） |

### 5.3 建议的验收步骤

1. 用第 1.3 节的 `git show ... | sha256sum` 校验 6 个项目文件，确认拿到的是同一 C0。
2. 将 `candidate.patch` 应用到 `project/Makefile`，执行 `make clean && make app`，确认 `./app` 输出 `1`。
3. 修改 `config.h`（如 `VALUE` 从 1 改为 2），执行 `make app`，确认 `./app` 输出 `2`，证明原 `MISSING main.o config.h` 导致的增量构建问题已消除。
4. 重新扫描或重新运行 BuildChecker，比较 findings：
   - 原 `MISSING main.o config.h` 应消失；
   - 原 `REDUNDANT main.o unused.h` 按当前 `patch()` 设计会保留，需要 B 组决定是否一并清理；
   - 新增问题用新报告的 findings 减去原报告 findings（等价于 `added`），已消除项用 `resolved`。
5. 把 B 组修复后的项目版本、重检报告路径、`added` / `resolved` 列表回填到第 7 节。

### 5.4 注意事项

- `patch()` 只修 `MISSING`，不会自动删除 `REDUNDANT`；如果验收要求“零 findings”，需要另行处理 `unused.h`。
- `validate()` 内部的复检使用 `scan()`（GCC `-MM` 投影），不是 BuildChecker；若验收明确要求 BuildChecker 复核，需要额外运行 `buildchecker()` 或 CI。
- `patch()` 要求报告 `commit` 与当前 fixture HEAD 完全一致；如果 B 组在 fixture 内新提交，必须用新报告，否则会得到 `STALE_REPORT`。
- 当前 A→B 正式交接尚未签收，本文不代替 B 组返回文件或验收结论。

## 6. 需要双方确认的事项

| 事项 | 当前状态 | 建议 |
|---|---|---|
| 代码基线 `489158f` 的 CI artifact | 未归档 | 如需把报告绑定到交付基线，重跑 `e8e10-quality-gate` 并下载 artifact；workflow 已加 `include-hidden-files: true` |
| fixture `project/.git` | 未归档 | 重跑后应随 artifact 归档；现有报告用 `input_sha256` 做内容绑定 |
| `REDUNDANT main.o unused.h` | 保留 | 由 B 组确认是否清理，或在验收中明确接受 |
| A→B 签收/返回 | 待 B 组 | 由双方负责人记录时间和参与人 |

## 7. 交接记录（待填）

| 字段 | 内容 |
|---|---|
| 交付时间 | 待填 |
| 交付人 | 陈玉熙（241880089，A09） |
| 接收人 | 待填（B 组负责人） |
| 交付分支 / 代码基线 | `student/241880089/e8-e10` / `489158f2636b5f83c46b253c68469a63291d8a62` |
| 检测版本 SHA | 外层 `a0802185e793f2de7e6290edbfb8c7760a819b91`（旧 `77e891c`）；fixture `f4d0e190a47172f736f05bd20d49fe68b3a7127a` |
| B 组返回文件/确认 | 待填 |
| dry-run PR/commit | 待填 |
| 重检报告路径 | 待填 |
| `added` / `resolved` | 待填 |
| 验收结论 | 待填 |
| 备注 | 本表未填写项不视为已完成 |
