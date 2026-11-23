# E11–E12 最终联调归档与交付审计

- 小组/轨道：A09 / A（BuildChecker → EChecker）
- 审计日期：2026-11-17
- 最后更新：2026-11-17（PR #23 合并后回填）
- 审计人：241880375 张海洋
- 结论：**A/B 技术联调已完成；241880369 高嘉程的个人材料与个人测试已由 PR #23 合并；课程最终提交仍不能标记完成，原因是 241880089 陈玉熙仍缺 E11–E12 个人材料与个人测试。**

> **2026-11-17 状态更新（本文件下方第 1–7 节为当时审计快照）：**
> 241880089 陈玉熙的 E11–E12 个人材料、个人测试与云主机证据已由 PR #25 合入，merge commit 为 `bfd2ab1`；四人材料与证据目录现已齐全。
> B09 已对 A09 E12 正式签收；A09 侧按文件字节复核后确认：B09 核对时的 `main` 为 `b0765a0f990b10a28392fe6d4318b4b73a41177a`，证据归档在 b0765a0f、PR #17 head `0cd8054911a18be96900e05c3b7747c6b35a4112` 与当前 main `bfd2ab1` 三处的 Git blob 均为 `5c52c1824f147019ac25f6706f0549318a1f0cec`，归档 SHA256 为 `19479d51720decbca2518453e00646a4700c7b21101b018965bfdbc0c8cce648`。
> B09 直接消费的原始 `incremental-check.json` SHA256 为 `8508d50232bfa4a529d51accd4dc94e5765a0fe0a0b130eebf73f8f866a98716`（未使用 `fixed-md.json`）；A 端 `job_id=job-1bd0ed1b449f44f293853df90440844f`、`trace_id=trace-4e7c0c6afd0447f9869d2f5e1ee6f4ae`，base/target 与交付值一致；修复提交 `817b2459d53f586f7f3800ce20d0c3f002621f77` 的父提交为 A 端 target，仅修改 `Makefile`；`candidate.patch` SHA256 `88074f66c291dcad1344c48f6a2b9ddd42d235d9d0415c85fb33310c5b7cb2af`，`validation.json` SHA256 `aeb157c32906bfe7859fc93e14c2a52cbb5e63dad0004c033d8c29f788475394` 且 `accepted=true`；`build.log` / `incremental.log` / 复检报告 SHA256 分别为 `29bfc712…` / `52b1b084…` / `08792b92…`，复检 MD=0，仅保留允许的 `REDUNDANT(main.o, unused.h)`；修复项目 bundle SHA256 `e6f7cd9802728705c85fd003ee031900a44691715c1768590a5de830017c0dda`。
> 最新全量检查见 `docs/reports/A09-E11-E12-audit.md`。

## 1. 结论摘要

1. A 组 E11-A、E11-B、E12、真实项目 E12 与异步 API 证据已由 PR #17 合入 A 组 `main`。
2. A 组第四名成员马海川的 E11–E12 独立测试和报告已由 PR #18 合入 A 组 `main`。
3. B 组正式联调 PR #14 已合并；B 组最终 `main` 为 `80b4dafb836365911e6e85451ee367cc874afa46`。
4. B 组正式签收目录已复制到本仓库，`sha256sum -c artifacts.sha256` 全部通过。
5. A 组 `main` 的 E7、E8–E10、E11–E12 三项 CI 均为 `success`。
6. **当前阻塞项：A 组 `main` 中仍没有 241880089 陈玉熙的 E11–E12 个人目录和个人测试。** 因此目前只能提交“技术联调完成”的审计包，不能把它冒充为“四人个人实验全部完成”的最终作业包。
7. 241880369 高嘉程的个人报告、个人测试、E11-A/E12/API 证据已由 PR #23 合入 `main`；最终 `main` 为 `a1c89c6c96bc2c56ff257b3754f89e880236821c`。

## 2. 仓库与 PR

| 项目 | 值 |
|---|---|
| A 组仓库 | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud> |
| A 组最终 `main` | `a1c89c6c96bc2c56ff257b3754f89e880236821c` |
| A 组 PR #17（张海洋） | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/pull/17> |
| A 组 PR #17 merge SHA | `b634e12eb63c3f9330f7c58ff84981de23647c60` |
| A 组 PR #18（马海川） | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/pull/18> |
| A 组 PR #18 merge SHA | `b0765a0f990b10a28392fe6d4318b4b73a41177a` |
| A 组 PR #23（高嘉程） | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/pull/23> |
| A 组 PR #23 merge SHA / 当前 main | `a1c89c6c96bc2c56ff257b3754f89e880236821c` |
| B 组仓库 | <https://github.com/llxxy-cn/devops-b09> |
| B 组 PR #14 | <https://github.com/llxxy-cn/devops-b09/pull/14> |
| B 组 PR #14 merge SHA | `0c373199fc0f0528d930da039ca2fe642027d40b` |
| B 组最终 `main` | `80b4dafb836365911e6e85451ee367cc874afa46` |

B 组 PR #14 的 `e7-b-quality-gate`、`e8e10-quality-gate`、`e11e12-integration` 均通过。B 组随后 PR #15 只更新最终文档，最终 main CI 仍全部通过。

## 3. B 组正式签收产物

归档目录：`evidence/students/241880375/e11-e12/b09-signoff/`

来源：B 组 `main` 提交 `80b4dafb836365911e6e85451ee367cc874afa46` 中的
`docs/students/241880556/e11-e12-b4/formal/signoff/`。

| 文件 | SHA256 |
|---|---|
| `validation.json` | `aeb157c32906bfe7859fc93e14c2a52cbb5e63dad0004c033d8c29f788475394` |
| `candidate.patch` | `88074f66c291dcad1344c48f6a2b9ddd42d235d9d0415c85fb33310c5b7cb2af` |
| `build.log` | `29bfc7126a891b1deca1f143ff3f7d2a0003e1c4d43a3df25ba739524b1a9a0c` |
| `incremental.log` | `52b1b0840faee45dffd5d909945f740dd9fad73b1dc58e544ac1c0491ce05e57` |
| `recheck.json` | `08792b92a49d4b4cd59c4919f4a7c9d4679bf3bf1010559190046e53a7080c00` |
| `repaired-project.bundle` | `e6f7cd9802728705c85fd003ee031900a44691715c1768590a5de830017c0dda` |
| `repaired-commit.txt` | `ef979a2d7183c1d9e26b214ab0b7edb5cebe019e7f8cb551dc66895b55b21e31` |

签收结果：

- `accepted=true`
- A job：`job-1bd0ed1b449f44f293853df90440844f`
- A trace：`trace-4e7c0c6afd0447f9869d2f5e1ee6f4ae`
- base：`3fcb72029bf560afde2d29436395ff3b979a19fd`
- target：`15c059958a41a5a0513dc048036439843a34ad28`
- 修复提交：`817b2459d53f586f7f3800ce20d0c3f002621f77`
- 原始 `incremental-check.json` SHA256：`8508d50232bfa4a529d51accd4dc94e5765a0fe0a0b130eebf73f8f866a98716`
- 构建输出：`1`；修改 `config.h` 后增量重建输出：`2`
- `recheck_missing_count=0`；仅保留原有 `REDUNDANT(main.o, unused.h)`

A 组原始证据归档 `e11e12-evidence-241880375.tar.gz` 的 SHA256 为
`19479d51720decbca2518453e00646a4700c7b21101b018965bfdbc0c8cce648`，大小 7,149,921 字节，与 B 签收记录一致。

## 4. Actions 与 artifact

| 组别 | 工作流 | Run | 结论 | Artifact | Artifact SHA256 |
|---|---|---|---|---|---|
| A | E7 A quality gate | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/43857981566> | success | — | — |
| A | E8-E10 teaching validation | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/43857981555> | success | — | — |
| A | E11-E12 integration | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/43857981494> | success | `e11e12-evidence-43857981494`（ID `14220839475`，343,410 B） | `8064005c2bf51a2dc413641f933fd9be12ff228dc368214ccaf94f61334ec44f` |
| A（PR #23，241880369） | E7 A quality gate | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/44051185529> | success | — | — |
| A（PR #23，241880369） | E8-E10 teaching validation | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/44051185736> | success | — | — |
| A（PR #23，241880369） | E11-E12 integration | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/44051185678> | success | `e11e12-evidence-44050562100`（ID `14312968942`，343,396 B） | `cddefe63b0f74d767b10781a7541cd3bbaecc355e369db4f71e86f88f74cd4ac` |
| A（PR #23 合并后 main） | E7 A quality gate | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/44053027137> | success | — | — |
| A（PR #23 合并后 main） | E8-E10 teaching validation | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/44053027052> | success | — | — |
| A（PR #23 合并后 main） | E11-E12 integration | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/44053027111> | success | — | — |
| B | E7 B quality gate | <https://github.com/llxxy-cn/devops-b09/actions/runs/44023488947> | success | — | — |
| B | E8-E10 teaching validation | <https://github.com/llxxy-cn/devops-b09/actions/runs/44023488990> | success | — | — |
| B | E11-E12 integration | <https://github.com/llxxy-cn/devops-b09/actions/runs/44023488982> | success | `e11e12-evidence-44023488982`（第 2 次尝试，ID `14302247540`，2,250,326 B） | `0dbe891a036b1a42644b5eab5e8287ac9f86958229401e99df50fe6b7ce5b9f3` |

两个最终 artifact 已保存于 `evidence/students/241880375/e11-e12/actions-artifacts/`，避免网页过期后无法复核。

## 5. A 组四人 E11–E12 材料盘点

| 学号/姓名 | E11–E12 个人报告 | 个人测试 | 状态 |
|---|---|---|---|
| 241880089 陈玉熙 | 无 `docs/students/241880089/e11-e12/` | 无 | **缺失，阻塞最终提交** |
| 241880369 高嘉程 | `docs/students/241880369/e11-e12/` | `StudentE11E12A241880369.test_fixed_report_outside_data_rejected` | 已合入 main（PR #23） |
| 241880374 马海川 | `docs/students/241880374/e11-e12/` | `StudentE11E12A241880374.test_candidate_outside_data_rejected` | 已合入 main |
| 241880375 张海洋 | `docs/students/241880375/e11-e12/` | `StudentE11E12A241880375.test_restart_marks_unfinished_job_and_keeps_completed_job` | 已合入 main |

仓库中仍不存在 `student/241880089/e11-e12` 分支，也没有其 E11–E12 PR；其现有分支和材料均为 E8–E10，不能冒充本轮个人实验。`student/241880369/e11-e12` 已由 PR #23 合并。

### 241880369 高嘉程个人交付（PR #23）

- PR：<https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/pull/23>，merge SHA `a1c89c6c96bc2c56ff257b3754f89e880236821c`
- 首推代码/测试 head：`d4c3a62936c9af5d089fdc3215c9f185f827c5e5`；后续证据/文档回填 head：`98f595c19ad971102ca5d7735f422c80f5616685`
- 个人测试：`StudentE11E12A241880369.test_fixed_report_outside_data_rejected`；契约测试 12 → 13 OK
- E11-A：`job-efc49baae58c414490f14be0275a413a` / `trace-06722428a2ab41a08b0a3ce5fa13b1f1`，`SUCCEEDED`
- E12 固定样例：`job-81be941f47fd4f8fa5a903f5a5455b6c` / `trace-b888bbdda42d476fb4da7e0e658f12fa`，五阶段 `SUCCEEDED`
- E12 真实项目：`job-268fc09fa76c4f8391867c2da7d950d8` / `trace-b16b370e11284e97b63e24e46228fddd`，五阶段 `SUCCEEDED`
- API：`job-045cf351d04e4b5fa6c9ffe7f4ae26c3` / `trace-ce6da84edbd7486180aa2ea0a59f1578`；幂等同 job、冲突 409、产物 SHA 与 `X-Content-SHA256` 一致
- 证据：`docs/students/241880369/e11-e12/`、`evidence/students/241880369/e11-e12/`、`labs/e11e12/test_student_241880369.py`

## 6. 最终课程提交前置条件

在课程网页提交“最终小组作业包”前，还需：

1. 陈玉熙按 A 轨 E11–E12 手册在自己的分支完整运行实验，保留原始结果。
2. 陈玉熙提交 `docs/students/241880089/e11-e12/` 个人报告、ADR/AI 使用记录（按课程要求）和一个有独立预期的测试。
3. 该 PR 合入 A 组 `main` 后，重新确认 E7、E8–E10、E11–E12 三项 CI 全绿，并记录新的最终 main SHA。
4. 重新生成最终小组 ZIP，再提交课程网页。
5. B 组 PR #14 已合并，本轮无需让 B 组重跑 E12；也不要覆盖已归档的 B 签收文件。

## 7. 不重跑声明

本归档的本次回填只做最终核对和状态更新；241880369 的实验与证据由其本人执行并经 PR #23 合并，审计人没有代跑或改写其数据。本次回填没有修改测试代码，没有改写历史证据，也没有删除或覆盖 E7、E8–E10、E11–E12 的原有工作流和证据。
