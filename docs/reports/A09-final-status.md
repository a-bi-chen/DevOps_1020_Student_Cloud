# A09 E7 最终状态记录

记录时间：2026-10-27

记录人：高嘉程（241880369，GitHub `Allen-Ga`）

## 1. PR 状态

| PR | 标题 | 状态 | mergeStateStatus | CI | Review |
|---:|---|---|---|---|---|
| #2 | chore: consolidate A09 E5-E7 evidence and baseline | OPEN | BLOCKED | `e7-a-quality-gate` pass | Allen-Ga APPROVED |
| #3 | test: demonstrate E7 merge rejection | OPEN | BLOCKED | `e7-a-quality-gate` pass | 无 |
| #4 | test: add E7 project-root boundary test | OPEN | BLOCKED | `e7-a-quality-gate` pass | 无 |

三个 PR 均为 `mergeable: MERGEABLE`，不是代码冲突。

## 2. 阻塞原因

Ruleset `main`（ID `25866762`）：

```text
required_status_checks: e7-quality-gate
workflow check:         e7-a-quality-gate
strict_required_status_checks_policy: true
current_user_can_bypass: never
```

`Allen-Ga` 仓库权限：

```text
admin: false
maintain: false
push: true
triage: true
```

因此无法修改 Ruleset。需要仓库所有者 `a-bi-chen` 修改检查名，或把 `Allen-Ga` 提升为 admin。

## 3. 已完成证据

- 边界测试代码：`5a906d5`
- 边界测试记录：`541ac44`
- 构建：`16 passed`
- E7 gate：`8/8 passed`
- 独立 oracle：`6 tests OK`
- secret scan：未发现问题
- 镜像：`course1020-buildchecker:241880369`
- 镜像 ID：`sha256:8364984fa2a1325a20d707d46577b42622c7d08035dcd9560a7c8714e6818ebb`

## 4. 记录文件

```text
docs/reports/A09-E7-boundary-test.md
work/ci-boundary/PR-before-merge.json
work/ci-boundary/merge-rejection.log
work/final-records/pr2.json
work/final-records/pr3.json
work/final-records/pr4.json
work/final-records/pr2-checks.txt
work/final-records/pr3-checks.txt
work/final-records/pr4-checks.txt
work/final-records/ruleset-main.json
work/final-records/repo.json
work/final-records/artifacts/
```

## 5. Ruleset 修正后操作顺序

1. 修正 Ruleset 必填检查名为 `e7-a-quality-gate`。
2. 合并 PR #2。
3. 合并 PR #3（如提示落后，先更新分支）。
4. 合并 PR #4（如提示落后，先更新分支）。
5. 保存三个 PR 的 MERGED 记录。
6. 更新 `docs/reports/A09-contributions.md` 和 `docs/reports/A09-acceptance.csv`。
7. 下载并保存最终 artifact。
