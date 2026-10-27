# A09 逐人贡献记录（动态）

本文件随 E5–E7 剩余任务持续更新。最终提交时以 Git、PR、Review 和运行证据为准。

| 姓名 | 学号 | 已确认贡献 | 仍需补充 |
|---|---|---|---|
| 马海川 | 241880374 | E5 基线验证；PR #2（head `072667e`，merge `614eeca`）完成唯一代码入口、团队证据和报告；PR #3（merge `fb913a7`）完成 `1 failed/15 passed → 16 passed` 的失败恢复闭环；编写最终交接文档 | 对他人 PR 的有效 Review（如课程要求） |
| 张海洋 | 241880375 | 完成 E5 原始采集、E6 修复前后检测、E7 本地 8 项门禁；初始化提交 `9165f370ad30da9c1f9f7e5a51bda7f04d4ec690`；提交邮箱已核对 | 对另一名成员 PR 的有效 Review；补 GitHub 用户名 |
| 陈玉熙 | 241880089 | GitHub `a-bi-chen`，仓库创建者；完成正常 CI；配置 main Ruleset；完成 PR #1 和正常运行证据；2026-10-27 修正 Ruleset 必填检查名为 `e7-a-quality-gate` | 对另一名成员 PR 的有效 Review |
| 高嘉程 | 241880369 | 新增父目录逃逸边界测试（代码 `5a906d5`，PR #4 merge `c81c193`）；完成 PR #2 正式 Review（`APPROVED`）；合并 PR #2/#3/#4；最终 main `17 passed`、8/8 gate、oracle 6 tests OK、secret scan 通过；保存 PR/CI/artifact 记录 | 无（E5–E7 验收完成） |

## 最终合并记录

| PR | 合并时间（UTC） | Merge commit |
|---:|---|---|
| #2 | 2026-10-27T12:17:10Z | `614eecaef6bd6ad8ada43f37ac022828408f1773` |
| #3 | 2026-10-27T12:18:49Z | `fb913a723b56eedbd0f0dcfebc7b290d9dcfb345` |
| #4 | 2026-10-27T12:20:00Z | `c81c1937171b1d4587300751195b7a3586988507` |

最终 main：`c81c1937171b1d4587300751195b7a3586988507`。

## 贡献判定规则

1. 代码贡献以提交作者、PR 内容和合并记录为依据。
2. Review 以 GitHub Review 记录为依据。
3. 实验贡献以对应 work 目录、trace、JSON 和 gate 结果为依据。
4. 团队任务归属可以在汇报中说明，但不能伪造个人 Git 提交。
5. 最终贡献比例在所有成员记录完成后再确定。
