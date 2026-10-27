# A09 E7 项目根边界测试记录

## 基本信息

- 执行人：高嘉程（241880369）
- 分支：`e7-boundary-test-241880369`
- 代码提交：`5a906d59e9bcdcea751ec74042661d0051612c3c`
- 记录提交：`541ac44df2ea9c798f4409739c9fd126e3ac4476`、`b7ea0d3a44a747357752d02ea742f7f1c3e1d809`
- PR：#4 https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/pull/4
- Merge commit：`c81c1937171b1d4587300751195b7a3586988507`
- 合并时间：2026-10-27T12:20:00Z
- 测试文件：`services/buildchecker/tests/test_fullcheck.py`

## 1. 新增测试

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

输入：

```text
项目根： /course/project
相对路径：../project-other/secret.h
归一化后：/course/project-other/secret.h
```

预期：返回 `None`。该文件位于项目根之外，不能因为字符串前缀相似被误算为项目内文件。

## 2. 验证结果

边界分支构建：

```text
16 passed
BUILD_EXIT_CODE=0
```

合并后的最终 main 构建：

```text
17 passed
BUILD_EXIT_CODE=0
```

最终 main 的 17 项 = 原 15 项 + PR #3 演示测试 + 本边界测试。

完整 E7 gate：

```text
GATE_EXIT_CODE=0
gate-result.json: "passed": true
8/8 cases passed
```

独立 oracle：

```text
Ran 6 tests
OK
```

secret scan：

```text
密钥检查：未发现问题（文件 728 个，含 Git 历史）
```

最终镜像：

```text
course1020-buildchecker:241880369-final
sha256:6e12e90adbe1d3ff47d8f7f38e54186da0e4bf4411348d6db56e3dfe30eb332b
```

证据路径：

```text
work/build-boundary/unit-tests/stdout.log
work/e7-boundary/gate/gate-result.json
work/build-final/unit-tests/stdout.log
work/e7-final/gate/gate-result.json
```

## 3. CI 结果

PR #4 的 `e7-a-quality-gate` 检查全部通过：

- 代码提交 `5a906d5`：run 40499695852、40500116665
- 记录提交 `541ac44`：run 40500335454、40500345205
- 记录提交 `b7ea0d3`：run 40502042264、40502047451
- 更新分支后 `c6b2b4f`：run 40502794587、40502803898
- 合并后 main `c81c193`：run 40502929554

## 4. 合并记录

Ruleset 修正前，合并被拒绝：

```text
MERGE_ATTEMPT_EXIT_CODE=1
X Pull request #4 is not mergeable: the base branch policy prohibits the merge.
```

证据：

```text
work/ci-boundary/PR-before-merge.json
work/ci-boundary/merge-rejection.log
```

Ruleset 修正后（`e7-a-quality-gate`，App ID 15368），PR #4 于 2026-10-27T12:20:00Z 合并：

```text
merge commit: c81c1937171b1d4587300751195b7a3586988507
```

## 5. Review 记录

高嘉程（`Allen-Ga`）已完成对 PR #2 的正式 Review：

- 状态：`APPROVED`
- 时间：2026-10-27T12:03:00Z
- PR：https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/pull/2

## 6. 已保存记录

```text
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
work/final-records/artifacts/40342643704/
work/final-records/artifacts/40342653053/
work/final-records/artifacts/40323775871/
work/final-records/artifacts/40323785662/
work/final-records/artifacts/40500335454/
work/final-records/artifacts/40500345205/
work/final-records/artifacts/40502929554/
```

## 7. 结论

边界测试已进入镜像和门禁，PR #4 已合并到 main；最终 main 构建 17 passed，E7 gate 8/8。
