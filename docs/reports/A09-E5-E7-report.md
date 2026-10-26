# A09 E5–E7 实验报告

小组/轨道：A09 / A 轨道 BuildChecker

团队成员：

| 姓名 | 学号 | GitHub/身份 |
|---|---|---|
| 马海川 | 241880374 | `weijige7` |
| 张海洋 | 241880375 | GitHub 账号待确认 |
| 陈玉熙 | 241880089 | `a-bi-chen`，仓库创建者 |
| 高嘉程 | 241880369 | 待本人补充 |

阶段分工：

- 张海洋：E5–E7 基线运行、依赖检测、修复复检和本地门禁。
- 陈玉熙：创建 GitHub 仓库、配置 Actions/Ruleset、完成正常 CI 和合并流程。
- 马海川：证据整合、扩展测试、失败恢复、最终报告与验收。
- 高嘉程：由本人新增第 16 项边界测试并 Review 马海川的整合 PR。

仓库：https://github.com/a-bi-chen/DevOps_1020_Student_Cloud

当前基线提交：`ffef5ba95357e084485fb8bf209b97843a0b9b90`

云主机：Ubuntu 22.04.5 LTS，x86_64，2 CPU，3.5 GiB 内存；Docker 29.1.3，Compose 2.29.2，Python 3.10.12，GNU Make 4.3。

## 1. 代码与实现来源

BuildChecker 核心位于 `services/buildchecker/buildchecker/fullcheck.py`，使用 `strace -ff` 采集文件与进程系统调用，从 `make -p` 的 Files 段提取声明依赖，再按目标计算实际图与声明图的差集。

教学 profile 的范围是：

- 单个 Make 进程；
- 每个 recipe 一个最终输出；
- 项目目录内的成功 read-open 作为实际读取证据；
- `O_DIRECTORY`、`O_PATH`、系统路径和项目外路径被过滤；
- 多输出、数字目录 FD、符号链接和递归 Make 等不支持场景必须显式失败。

## 2. E5：原始复现

### 2.1 输入

`fixtures/md-rd`：

```make
main.o: main.c unused.h
	$(CC) -c main.c -o main.o
```

`main.c` 实际包含 `config.h`；`unused.h` 未被包含。

### 2.2 执行与命令

本阶段由张海洋（241880375）执行。

```bash
python3 scripts/lab_cloud.py build \
  --image course1020-buildchecker:local \
  --out work/build-01 \
  --build-timeout 1200

python3 scripts/lab_cloud.py e5 \
  --image course1020-buildchecker:local \
  --out work/e5-01
```

### 2.3 结果

- 服务测试：15 passed，exit=0。
- E5：exit=0，程序输出 `1`，构建 stderr 为空。
- `app: main.o`：Make 数据库第 609 行。
- `main.o: main.c unused.h`：Make 数据库第 1061 行。
- `config.h` 成功读取：trace 第 580 行。
- `main.o` 成功写打开：trace 第 23 行。
- E5 trace 共 7 个进程文件。

精确集合差：

```text
实际 main.o: {main.c, config.h}
声明 main.o: {main.c, unused.h}

实际 - 声明 = {config.h}   -> MISSING
声明 - 实际 = {unused.h}   -> REDUNDANT
```

证据根目录：

```text
evidence/A09-E5-E7/241880375-work/e5-01/
```

## 3. E6：自动检测与修复复检

### 3.1 修复前

本阶段由张海洋（241880375）执行。

```bash
python3 scripts/lab_cloud.py e6 \
  --image course1020-buildchecker:local \
  --out work/e6-before
```

结果：

- status=`SUCCEEDED`
- clean/build exit 均为 0
- findings=2
- trace_id=`e6-2c51407c2b224a56a39a763b5b80e61e`
- findings 精确为 `MISSING(main.o, config.h)`、`REDUNDANT(main.o, unused.h)`

### 3.2 修复后

```bash
python3 scripts/lab_cloud.py e6 --fixed \
  --image course1020-buildchecker:local \
  --out work/e6-after
```

结果：

- status=`SUCCEEDED`
- clean/build exit 均为 0
- findings=`[]`
- trace_id=`e6-c5ad2a904cd34f1a8408bdfebd2ecd4e`

### 3.3 证据校验

```bash
python3 scripts/verify_e6_evidence.py \
  --before work/e6-before/evidence/findings.json \
  --after work/e6-after/evidence/findings.json
```

实际通过，变化输入集合只有：

```text
Makefile
```

前后 evidence 均包含 actual graph、declared graph、processes、Make 数据库、trace 和构建日志。

## 4. E7：本地完整门禁

独立判定测试：6 tests OK。运行与门禁执行人：张海洋（241880375）。

完整 gate：

| case | passed | exit | detector status |
|---|---:|---:|---|
| unit-tests | true | 0 | - |
| original-1 | true | 1 | SUCCEEDED |
| original-2 | true | 1 | SUCCEEDED |
| original-3 | true | 1 | SUCCEEDED |
| fixed | true | 0 | SUCCEEDED |
| build-failed | true | 1 | FAILED |
| unsupported | true | 1 | FAILED |
| timeout | true | 1 | TIMED_OUT |

整体 `passed=true`，8/8 场景通过。

证据：

```text
evidence/A09-E5-E7/241880375-work/e7-01/gate/
```

其中 `gate-result.json` 保存状态、trace_id 和整体判定，`results.csv` 按场景保存退出码和 detector status，各场景子目录保存命令、stdout、stderr、输入副本和 evidence。

## 5. GitHub Actions 正常路径

Run 由陈玉熙（241880089）接入和配置：

https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/40298566040

提交：`ffef5ba95357e084485fb8bf209b97843a0b9b90`

Job：`e7-a-quality-gate`

结果：

- 整体 success；
- gate 8/8 passed；
- source secret scan 未发现问题；
- image secret scan 未发现问题；
- artifact `e7-a-evidence-40298566040-1` 已归档到本仓库 `evidence/CI-A/run-40298566040/`。

## 6. 尚未完成的 E7 验收项

以下项目仍在执行中，完成后需要更新本报告和验收记录：

1. 新增至少一项自己的边界测试，使服务测试从 15 项增加到 16 项或更多。
2. 修复 Ruleset 必需检查名为 `e7-a-quality-gate`。
3. 创建故意失败 PR，取得 `1 failed / 15 passed`、`BLOCKED` 和 merge exit=1。
4. 修正测试预期，取得最新提交 `16 passed`、`CLEAN` 和 `MERGED`。
5. 下载失败运行和恢复运行的 artifact。
6. 填写逐人贡献和 Review 记录。

在这些项目完成前，E5–E7 不能标记为最终验收完成。

## 7. 限制

- 当前是教学 profile，不是论文完整工具。
- 只支持单个 Make 进程和每个 recipe 一个最终输出。
- 不处理符号链接、递归 Make 和数字目录 FD 等复杂场景。
- 实验只覆盖固定 `md-rd` 样例，不能据此宣称复现论文 30 个项目的性能和误报结果。

## 8. 证据索引

| 阶段 | 路径 | 结论 |
|---|---|---|
| E5 | `evidence/A09-E5-E7/241880375-work/e5-01/` | 1 MD、1 RD，原始 trace 完整 |
| E6 before | `evidence/A09-E5-E7/241880375-work/e6-before/` | 2 findings，build=0 |
| E6 after | `evidence/A09-E5-E7/241880375-work/e6-after/` | 0 findings，build=0，仅 Makefile 变化 |
| E7 local | `evidence/A09-E5-E7/241880375-work/e7-01/gate/` | 8/8 passed |
| CI normal | `evidence/CI-A/run-40298566040/` | success、8/8 passed、无 secret |
| CI failure | 待生成 | PENDING |
| CI recovery | 待生成 | PENDING |

## 9. 逐人贡献状态

| 姓名 | 学号 | 已核验贡献 | 待补个人记录 |
|---|---|---|---|
| 张海洋 | 241880375 | E5/E6/E7 完整运行证据；初始化提交 `9165f37` | 对他人 PR 的 Review |
| 陈玉熙 | 241880089 | 仓库创建者 `a-bi-chen`；PR #1、正常 CI run、Ruleset | 对后续 PR 的 Review |
| 马海川 | 241880374 | 当前清理与证据整合分支；后续扩展测试和恢复合并 | 本人 PR、Review、最终报告 |
| 高嘉程 | 241880369 | 已分配第 16 项边界测试 | 本人提交测试 PR，并 Review 马海川整合 PR |

高嘉程部分留到最后，由本人完成；不能把其他成员的代码提交冒充成他的个人提交。
