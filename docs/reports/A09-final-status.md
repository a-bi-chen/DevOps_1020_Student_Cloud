# A09 E7 最终状态记录

记录时间：2026-10-27

记录人：高嘉程（241880369，GitHub `Allen-Ga`）

## 1. PR 状态

| PR | 标题 | 状态 | 合并时间（UTC） | Merge commit |
|---:|---|---|---|---|
| #2 | chore: consolidate A09 E5-E7 evidence and baseline | MERGED | 2026-10-27T12:17:10Z | `614eecaef6bd6ad8ada43f37ac022828408f1773` |
| #3 | test: demonstrate E7 merge rejection | MERGED | 2026-10-27T12:18:49Z | `fb913a723b56eedbd0f0dcfebc7b290d9dcfb345` |
| #4 | test: add E7 project-root boundary test | MERGED | 2026-10-27T12:20:00Z | `c81c1937171b1d4587300751195b7a3586988507` |

最终 main：`c81c1937171b1d4587300751195b7a3586988507`。

## 2. Ruleset

Ruleset `main`（ID `25866762`）已修正：

```text
required_status_checks: e7-a-quality-gate
integration_id:         15368
strict_required_status_checks_policy: true
current_user_can_bypass: never
updated_at:             2026-10-27T20:16:33+08:00
```

`Allen-Ga` 仍为 `admin:false, maintain:false`，但 Ruleset 修正后已可正常合并。

## 3. 最终验证（main）

- 构建：`17 passed`，`BUILD_EXIT_CODE=0`
- E7 gate：`8/8 passed`，`GATE_EXIT_CODE=0`，`gate-result.json` 中 `"passed": true`
- 独立 oracle：`6 tests OK`
- secret scan：未发现问题（文件 728 个，含 Git 历史）
- 最终镜像：`course1020-buildchecker:241880369-final`
- 镜像 digest：`sha256:6e12e90adbe1d3ff47d8f7f38e54186da0e4bf4411348d6db56e3dfe30eb332b`
- 最终 main CI：run 40502929554，success

说明：最终 17 项 = 原 15 项 + PR #3 的演示测试 + PR #4 的边界测试。

## 4. 边界测试

- 代码提交：`5a906d5`
- 记录提交：`541ac44`、`b7ea0d3`
- PR #4 最终 CI：run 40502794587、40502803898，均 pass
- 合并 commit：`c81c193`
- 详细记录：`docs/reports/A09-E7-boundary-test.md`

## 5. Review

高嘉程（`Allen-Ga`）对 PR #2 的正式 Review：`APPROVED`，时间 2026-10-27T12:03:00Z。

## 6. 已保存记录

```text
docs/reports/A09-E7-boundary-test.md
docs/reports/A09-contributions.md
docs/reports/A09-acceptance.csv
docs/reports/A09-E5-E7-report.md
docs/reports/A09-final-status.md
work/ci-boundary/PR-before-merge.json
work/ci-boundary/merge-rejection.log
work/final-records/pr2.json
work/final-records/pr3.json
work/final-records/pr4.json
work/final-records/pr2-merged.json
work/final-records/pr3-merged.json
work/final-records/pr4-merged.json
work/final-records/pr2-checks.txt
work/final-records/pr3-checks.txt
work/final-records/pr4-final-checks.txt
work/final-records/ruleset-main.json
work/final-records/repo.json
work/final-records/main-runs.json
work/final-records/artifacts/
```

## 7. 结论

E5–E7 的 E7 验收项已完成：边界测试、Ruleset 修正、PR #2/#3/#4 合并、个人 Review、最终构建与门禁、artifact 保存均已完成。
