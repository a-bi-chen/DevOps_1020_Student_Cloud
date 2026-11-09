# 陈玉熙 E8–E10 GitHub 基础设施证据

成员：陈玉熙（241880089），GitHub `a-bi-chen`，仓库管理员。

归档日期：2026-11-03

仓库：https://github.com/a-bi-chen/DevOps_1020_Student_Cloud

## 1. 基线

- 验收时 main：`83cc2be2dbeff487d4bc73861ddff843f3306848`
- PR #7：`E8-E10: import teaching implementation and quality gate`
- PR #7 head：`67dda9e83930dd1d018b5a7da19f5f4e34d32a4e`
- PR #7 merge：`83cc2be2dbeff487d4bc73861ddff843f3306848`
- 原 `e7-a-quality-gate` 检查保留，未删除或覆盖。

## 2. Ruleset

- Ruleset ID：`25866762`
- 名称：`main`；`enforcement: active`
- 更新时间：`2026-11-03T03:22:17.749Z`
- `strict_required_status_checks_policy: true`
- 必需检查：

| 检查名 | integration_id | 状态 |
|---|---:|---|
| `e7-a-quality-gate` | 15368 | 原有，保留 |
| `e8e10-quality-gate` | 15368 | 本次新增 |

其他规则未改动：`deletion`、`non_fast_forward`、`pull_request`。

## 3. CI 结果

| 检查 | PR #7 head | main 合并提交 |
|---|---|---|
| `e7-a-quality-gate` | success（run 41564244227 / 41564240129） | success（run 41564695967） |
| `e8e10-quality-gate` | success（run 41564244368 / 41564240141） | success（run 41564695930） |

## 4. 截图

| 文件 | 内容 | 来源页面 |
|---|---|---|
| `241880089_e8e10_01_ruleset-25866762.png` | Ruleset `main` 页面，Active | https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/rules/25866762 |
| `241880089_e8e10_02_ruleset-api-25866762.png` | Ruleset API 快照，含 ID 与两项必需检查 | https://api.github.com/repos/a-bi-chen/DevOps_1020_Student_Cloud/rulesets/25866762 |
| `241880089_e8e10_03_pr7-checks.png` | PR #7 Checks 页面，两个 workflow 均成功 | https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/pull/7/checks |
| `241880089_e8e10_04_main-e7-job.png` | main 上 `e7-a-quality-gate` 成功 | https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/41564695967/job/125683279968 |
| `241880089_e8e10_05_main-e8e10-job.png` | main 上 `e8e10-quality-gate` 成功 | https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/41564695930/job/125683279745 |

Ruleset 页面在匿名访问时会折叠检查名，因此额外保存 API 快照，作为 ID 和检查名的权威展示。

## 5. 边界

- 未修改测试代码。
- 未替张海洋运行 E9。
- 未删除、覆盖 `e7-a-quality-gate` 必需检查。
- 截图均来自公开页面，使用全新无登录浏览器上下文，不包含 Token、密钥或服务器凭据。

## 6. 最终 PR #12 状态（补充记录）

本节补充 E8–E10 个人分支最终合并状态。数据来自仓库内 `E8-E10_A组修改记录.md` 和本地 git 历史；**本目录截图仍对应 PR #7 的基线验收，不能当作 PR #12 的截图证据**。

- 个人分支最终 head：`3afc3453907aa1ca6b8d4b126595b4cf51378649`
- 最终推送门禁 run：`41667606590`（success；`e8e10-quality-gate`、`e7-a-quality-gate` 均 success）
- PR #12：https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/pull/12
- PR 检查 run：`41669789469`（E8–E10）、`41669789798`（E7 A），均 success
- 合并提交：`1fe05f4c7024057b56b713ea1d911575824c2ed2`
- 合并后远端个人分支被自动删除，本地从 `3afc345` 恢复 `student/241880089/e8-e10`。

`e7-a-quality-gate` 仍在 Ruleset `25866762` 中作为必需检查保留；本次没有修改 Ruleset。若需要 PR #12 的页面级截图，应另行补充，不能复用 PR #7 的截图。A→B 交接未执行，本文件不提供其证据。
