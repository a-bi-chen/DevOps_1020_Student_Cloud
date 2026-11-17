# A09 E11–E12 归档全量检查记录

- 生成时间：2026-11-17T14:11:34+00:00
- 结果：**21 PASS / 1 WARN / 0 FAIL**（共 22 项）

## 1. 四位组员材料

| 学号 | 姓名 | 个人材料 | 个人测试 | 证据文件数 | 结论 |
|---|---|---|---|---|---|
| 241880089 | 陈玉熙 | 齐全 | 已归档 | 18 | PASS |
| 241880369 | 高嘉程 | 齐全 | 已归档 | 5 | PASS |
| 241880374 | 马海川 | 齐全 | 已归档 | **目录缺失** | WARN |
| 241880375 | 张海洋 | 齐全 | 已归档 | 22 | PASS |

## 2. 校验清单

| 检查项 | 结果 | 说明 |
|---|---|---|
| 241880089 个人材料 | **PASS** | 陈玉熙：报告/ADR/AI_USAGE 齐全 |
| 241880089 个人测试 | **PASS** | labs/e11e12/test_student_241880089.py |
| 241880089 证据目录 | **PASS** | 18 个文件，4895419 字节 |
| 241880369 个人材料 | **PASS** | 高嘉程：报告/ADR/AI_USAGE 齐全 |
| 241880369 个人测试 | **PASS** | labs/e11e12/test_student_241880369.py |
| 241880369 证据目录 | **PASS** | 5 个文件，627811 字节 |
| 241880374 个人材料 | **PASS** | 马海川：报告/ADR/AI_USAGE 齐全 |
| 241880374 个人测试 | **PASS** | labs/e11e12/test_student_241880374.py |
| 241880374 证据目录 | **WARN** | report 已归档，但 evidence/ 目录缺失，无法按 SHA256 复核 |
| 241880375 个人材料 | **PASS** | 张海洋：报告/ADR/AI_USAGE 齐全 |
| 241880375 个人测试 | **PASS** | labs/e11e12/test_contract.py |
| 241880375 证据目录 | **PASS** | 22 个文件，10241123 字节 |
| manifest evidence/students/241880089/e11-e12/SHA256SUMS | **PASS** | 1 项，失败 0 项 |
| manifest evidence/students/241880369/e11-e12/artifacts.sha256 | **PASS** | 3 项，失败 0 项 |
| manifest evidence/students/241880375/e11-e12/archived-artifacts.sha256 | **PASS** | 12 项，失败 0 项 |
| manifest evidence/students/241880375/e11-e12/b09-signoff/artifacts.sha256 | **PASS** | 7 项，失败 0 项 |
| 证据 JSON 可解析 | **PASS** | 7 个 JSON，失败 0 个 |
| B09 签收字段 | **PASS** | accepted=true，job/trace/base/target/补丁/日志/复检哈希全部一致 |
| B09 归档 Git 对象一致 | **PASS** | blob={'b0765a0f': '5c52c1824f147019ac25f6706f0549318a1f0cec', 'pr17_head': '5c52c1824f147019ac25f6706f0549318a1f0cec', 'current_main': '5c52c1824f147019ac25f6706f0549318a1f0cec'} |
| B09 归档 SHA256 | **PASS** | 19479d51720decbca2518453e00646a4700c7b21101b018965bfdbc0c8cce648 |
| B09 签收产物哈希 | **PASS** | candidate.patch / validation / build / incremental / recheck / bundle 全部一致 |
| README 索引 | **PASS** | 四人学号均已索引 |

## 3. B09 对 A09 E12 的签收核对

- 核对时 A09 `main`：`b0765a0f990b10a28392fe6d4318b4b73a41177a`；PR #17 head：`0cd8054911a18be96900e05c3b7747c6b35a4112`。
- 证据归档 Git blob 三处一致：`5c52c1824f147019ac25f6706f0549318a1f0cec`（b0765a0f / PR #17 / 当前 main `bfd2ab1`）。
- 归档 SHA256：`19479d51720decbca2518453e00646a4700c7b21101b018965bfdbc0c8cce648`；与 B09 记录的 `19479d51720decbca2518453e00646a4700c7b21101b018965bfdbc0c8cce648` 一致。
- A 端 job/trace：`job-1bd0ed1b449f44f293853df90440844f` / `trace-4e7c0c6afd0447f9869d2f5e1ee6f4ae`；base/target 为 `3fcb72029bf560afde2d29436395ff3b979a19fd` / `15c059958a41a5a0513dc048036439843a34ad28`。
- B09 直接消费原始 `incremental-check.json`（SHA256 `8508d502...`），未使用 `fixed-md.json`；修复提交 `817b245...` 的父提交为 A 端 target，仅修改 Makefile。
- 复检 `recheck_missing_count=0`，仅保留允许的 `REDUNDANT(main.o, unused.h)`；最终 MD=0。

## 4. 缺口与说明

- 241880374 马海川：个人报告/ADR/AI_USAGE 与个人测试齐全，但仓库中没有 `evidence/students/241880374/e11-e12/`，报告引用的是未入库的 `work/...` 目录；本次不代造证据，标记为 WARN。
- 陈玉熙 241880089：E11–E12 个人材料、个人测试与证据均已归档。
- 本检查只读仓库文件，不修改任何组员材料；所有哈希均按文件字节重新计算。

机器可读结果：`docs/reports/A09-E11-E12-audit.json`
