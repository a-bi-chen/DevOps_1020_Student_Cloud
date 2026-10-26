# A09 E7 失败与恢复记录

## 基本信息

- 失败 PR：#3 https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/pull/3
- 失败提交：`57044b0d1ce3cf78c1e8df03e478f395e9b16013`
- 恢复提交：`3ac2d96d04fd33635a867444fa2a81acd2773a5b`
- 执行人：马海川（241880374）

## 1. 故意失败

将 version 成功返回值错误期望为 1：

```python
def test_intentionally_wrong_version_exit_code():
    assert main(["version"]) == 1
```

实际返回 0，因此测试失败：

```text
AssertionError: Intentional teaching fault: version actually returns zero
assert 0 == 1
1 failed, 15 passed in 0.05s
```

失败运行：

- push：40323172264
- pull_request：40323242261

两次 `e7-a-quality-gate` 均为 FAILURE。

## 2. 失败时合并被拒

```text
MERGE_ATTEMPT_EXIT_CODE=1
mergeStateStatus=BLOCKED
state=OPEN
```

日志：

```text
Pull request #3 is not mergeable: the base branch policy prohibits the merge.
```

## 3. 修正测试预期

同一 PR 的分支上把预期改为 0：

```python
def test_version_returns_success_exit_code():
    assert main(["version"]) == 0
```

恢复提交：`3ac2d96d04fd33635a867444fa2a81acd2773a5b`

恢复运行：

- push：40323775871
- pull_request：40323785662

结果：

```text
16 passed in 0.05s
```

恢复 gate：8/8 cases `passed=true`。

## 4. 恢复后合并仍被拒

恢复后再次尝试普通 merge，退出码仍为 1，PR 为 `OPEN / BLOCKED`。

原因不是测试失败，而是 Ruleset 当前要求：

```text
e7-quality-gate
```

Workflow 实际上报：

```text
e7-a-quality-gate
```

将 Ruleset 修正为 `e7-a-quality-gate` 后，才能完成最终合并。

## 5. 证据位置

服务器 `work/ci-rejection/`：

- `PR-before-fix.json`
- `runs.json`
- `failed-check.log`
- `merge-rejection.log`
- `artifacts-40323172264/`

服务器 `work/ci-recovery/`：

- `PR-before-merge.json`
- `merge-success-attempt.log`
- `artifacts-40323775871/`
- `artifacts-40323785662/`
