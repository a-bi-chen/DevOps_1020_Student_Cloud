# E11–E12 最终联调归档与交付审计

- 小组/轨道：A09 / A（BuildChecker → EChecker）
- 审计日期：2026-11-17
- 审计人：241880375 张海洋
- 结论：**A/B 技术联调已完成；课程最终提交尚不能标记完成，原因是两名成员缺少 E11–E12 个人材料与个人测试。**

## 1. 结论摘要

1. A 组 E11-A、E11-B、E12、真实项目 E12 与异步 API 证据已由 PR #17 合入 A 组 `main`。
2. A 组第四名成员马海川的 E11–E12 独立测试和报告已由 PR #18 合入 A 组 `main`。
3. B 组正式联调 PR #14 已合并；B 组最终 `main` 为 `80b4dafb836365911e6e85451ee367cc874afa46`。
4. B 组正式签收目录已复制到本仓库，`sha256sum -c artifacts.sha256` 全部通过。
5. A 组 `main` 的 E7、E8–E10、E11–E12 三项 CI 均为 `success`。
6. **阻塞项：A 组 `main` 中没有 241880089 陈玉熙、241880369 高嘉程的 E11–E12 个人目录和个人测试。** 因此目前只能提交“技术联调完成”的审计包，不能把它冒充为“四人个人实验全部完成”的最终作业包。

## 2. 仓库与 PR

| 项目 | 值 |
|---|---|
| A 组仓库 | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud> |
| A 组最终 `main` | `b0765a0f990b10a28392fe6d4318b4b73a41177a` |
| A 组 PR #17（张海洋） | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/pull/17> |
| A 组 PR #17 merge SHA | `b634e12eb63c3f9330f7c58ff84981de23647c60` |
| A 组 PR #18（马海川） | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/pull/18> |
| A 组 PR #18 merge SHA / 当前 main | `b0765a0f990b10a28392fe6d4318b4b73a41177a` |
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
| B | E7 B quality gate | <https://github.com/llxxy-cn/devops-b09/actions/runs/44023488947> | success | — | — |
| B | E8-E10 teaching validation | <https://github.com/llxxy-cn/devops-b09/actions/runs/44023488990> | success | — | — |
| B | E11-E12 integration | <https://github.com/llxxy-cn/devops-b09/actions/runs/44023488982> | success | `e11e12-evidence-44023488982`（第 2 次尝试，ID `14302247540`，2,250,326 B） | `0dbe891a036b1a42644b5eab5e8287ac9f86958229401e99df50fe6b7ce5b9f3` |

两个最终 artifact 已保存于 `evidence/students/241880375/e11-e12/actions-artifacts/`，避免网页过期后无法复核。

## 5. A 组四人 E11–E12 材料盘点

| 学号/姓名 | E11–E12 个人报告 | 个人测试 | 状态 |
|---|---|---|---|
| 241880089 陈玉熙 | 无 `docs/students/241880089/e11-e12/` | 无 | **缺失，阻塞最终提交** |
| 241880369 高嘉程 | 无 `docs/students/241880369/e11-e12/` | 无 | **缺失，阻塞最终提交** |
| 241880374 马海川 | `docs/students/241880374/e11-e12/` | `StudentE11E12A241880374.test_candidate_outside_data_rejected` | 已合入 main |
| 241880375 张海洋 | `docs/students/241880375/e11-e12/` | `StudentE11E12A241880375.test_restart_marks_unfinished_job_and_keeps_completed_job` | 已合入 main |

仓库中不存在 `student/241880089/e11-e12`、`student/241880369/e11-e12` 分支，也没有二人的 E11–E12 PR。其现有分支和材料均为 E8–E10，不能冒充本轮个人实验。

## 6. 最终课程提交前置条件

在课程网页提交“最终小组作业包”前，还需：

1. 陈玉熙、高嘉程分别按 A 轨 E11–E12 手册在自己的分支完整运行实验，保留原始结果。
2. 二人分别提交 `docs/students/<学号>/e11-e12/` 个人报告、ADR/AI 使用记录（按课程要求）和一个有独立预期的测试。
3. 两个 PR 合入 A 组 `main` 后，重新确认 E7、E8–E10、E11–E12 三项 CI 全绿，并记录新的最终 main SHA。
4. 重新生成最终小组 ZIP，再提交课程网页。
5. B 组 PR #14 已合并，本轮无需让 B 组重跑 E12；也不要覆盖已归档的 B 签收文件。

## 7. 不重跑声明

本归档只做最终核对、复制和索引，没有重跑 E11–E12 实验，没有修改测试代码，没有改写历史证据，也没有删除或覆盖 E7、E8–E10、E11–E12 的原有工作流和证据。
