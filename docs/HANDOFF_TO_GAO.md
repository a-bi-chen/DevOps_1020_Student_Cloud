# 高嘉程接手清单

接手人：高嘉程（241880369）  
交出人：马海川（241880374）  
交接日期：2026-10-26

## 1. 已完成的基线

| 阶段 | 状态 | 证据 |
|---|---|---|
| E5 | PASS | `evidence/A09-E5-E7/241880375-work/e5-01/` |
| E6 | PASS | `evidence/A09-E5-E7/241880375-work/e6-before/`、`e6-after/` |
| E7 本地 gate | PASS 8/8 | `evidence/A09-E5-E7/241880375-work/e7-01/gate/` |
| 正常 CI | PASS | `evidence/CI-A/run-40298566040/` |
| E7 失败/恢复 | PASS | `docs/reports/A09-E7-failure-recovery.md` |

## 2. 当前 PR

### PR #2：证据整合

https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/pull/2

- 作者：马海川
- HEAD：`24184a2bc4bd4788c853788aa82a7b19db1cb568`
- CI：成功
- 状态：`OPEN / BLOCKED`
- 阻塞原因：Ruleset 检查名错误

### PR #3：失败与恢复

https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/pull/3

- 失败提交：`57044b0`
- 恢复提交：`3ac2d96`
- 失败测试：1 failed / 15 passed
- 恢复测试：16 passed
- 恢复 gate：8/8 passed
- 状态：`OPEN / BLOCKED`
- 阻塞原因：Ruleset 检查名错误

## 3. 高嘉程需要完成

1. 修正 main Ruleset：

```text
e7-quality-gate → e7-a-quality-gate
```

2. 合并 PR #2。
3. 合并 PR #3。
4. 创建自己的边界测试 PR，至少新增：

```python
def test_relative_parent_path_cannot_escape_project_root(self):
    self.assertIsNone(
        project_path(
            "../project-other/secret.h",
            "/course/project",
            "/course/project",
        )
    )
```

5. 重建镜像，确认 16 passed 和 8/8 gate。
6. 合并边界测试 PR。
7. Review PR #2 或 PR #3。
8. 更新最终报告、贡献表和验收记录。
9. 重新运行 secret scan，并下载所有 artifact。

## 4. 已有失败/恢复证据

仓库文档：

```text
docs/reports/A09-E7-failure-recovery.md
```

服务器工作目录：

```text
work/ci-rejection/
work/ci-recovery/
```

这些是交接证据，不要删除或覆盖。

## 5. 验收前检查

```bash
python3 scripts/secret_scan.py . --history
gh pr checks 2
gh pr checks 3
gh pr view 2 --json state,mergeStateStatus,mergedAt,mergeCommit,url
gh pr view 3 --json state,mergeStateStatus,mergedAt,mergeCommit,url
```

最终必须保存：

- 两个 PR 的 MERGED 记录；
- 边界测试 PR 的 MERGED 记录；
- 失败、恢复、边界测试三次 artifact；
- 四人贡献和 Review 链接；
- 最终报告和证据包。
