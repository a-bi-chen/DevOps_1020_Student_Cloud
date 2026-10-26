# A09 E5–E7 证据索引

本目录保存已经下载并核验的原始证据。

## 0. 成员证据映射

| 姓名 | 学号 | 当前证据 |
|---|---|---|
| 张海洋 | 241880375 | E5–E7 完整 work、修复前后报告、本地 gate |
| 陈玉熙 | 241880089 | GitHub 正常 CI run、artifact、Ruleset 和合并截图 |
| 马海川 | 241880374 | 清理与证据整合 PR、后续测试和失败恢复 PR |
| 高嘉程 | 241880369 | 最终由本人完成的 PR 或 Review 证据 |

## 1. 成员1运行证据

成员：张海洋（241880375）。

目录：

```text
evidence/A09-E5-E7/241880375-work/
```

### E5

路径：`241880375-work/e5-01/`

已核实：

- `program-output.txt` = `1`
- `make-db.txt:609` = `app: main.o`
- `make-db.txt:1061` = `main.o: main.c unused.h`
- trace 中存在成功读取 `config.h`
- trace 中存在写出 `main.o`
- trace 共 7 个进程文件

结论：

```text
MISSING   main.o -> config.h
REDUNDANT main.o -> unused.h
```

### E6

路径：

- `241880375-work/e6-before/`
- `241880375-work/e6-after/`

已核实：

| 项目 | 修复前 | 修复后 |
|---|---|---|
| status | SUCCEEDED | SUCCEEDED |
| clean exit | 0 | 0 |
| build exit | 0 | 0 |
| findings | 2 | 0 |
| trace_id | `e6-2c51407c2b224a56a39a763b5b80e61e` | `e6-c5ad2a904cd34f1a8408bdfebd2ecd4e` |

`verify_e6_evidence.py` 已通过，变化输入集合只有：

```text
Makefile
```

### E7 本地门禁

路径：`241880375-work/e7-01/gate/`

8/8 场景通过：

| case | passed | tool exit | detector status |
|---|---:|---:|---|
| unit-tests | true | 0 | - |
| original-1 | true | 1 | SUCCEEDED |
| original-2 | true | 1 | SUCCEEDED |
| original-3 | true | 1 | SUCCEEDED |
| fixed | true | 0 | SUCCEEDED |
| build-failed | true | 1 | FAILED |
| unsupported | true | 1 | FAILED |
| timeout | true | 1 | TIMED_OUT |

详细 trace_id 和命令见同目录的 `results.csv` 与各场景子目录。

## 2. GitHub Actions 正常路径

成员：陈玉熙（241880089）。

目录：

```text
evidence/CI-A/run-40298566040/
```

对应：

- commit：`ffef5ba95357e084485fb8bf209b97843a0b9b90`
- run：https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/40298566040
- artifact：`e7-a-evidence-40298566040-1`

已核实：

- 整体 job 成功。
- gate 8/8 场景 passed。
- source secret scan 未发现问题。
- image secret scan 未发现问题。
- `work/ci/` 原始证据已归档。

## 3. 仍待补充的证据

- 马海川的团队仓库整合 PR 和独立故障恢复记录。
- 高嘉程本人完成的至少一项实质贡献和一次 Review。
- 新增第 16 项服务测试的修改、构建和门禁结果。
- 故意失败 PR：`1 failed / 15 passed`、`OPEN / BLOCKED`、merge exit=1。
- 修复后的 `16 passed`、`CLEAN`、`MERGED`。
- 失败运行与恢复运行的 artifact。
- Ruleset 中 `e7-a-quality-gate` 的实际配置截图或 API 输出。
- 最终逐人贡献和 Review 记录。
