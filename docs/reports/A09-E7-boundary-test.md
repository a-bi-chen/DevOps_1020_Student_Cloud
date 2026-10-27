# A09 E7 项目根边界测试记录

## 基本信息

- 执行人：高嘉程（241880369）
- 分支：`e7-boundary-test-241880369`
- 代码提交：`5a906d59e9bcdcea751ec74042661d0051612c3c`
- 记录提交：`541ac44df2ea9c798f4409739c9fd126e3ac4476`
- PR：#4 https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/pull/4
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

## 2. 本地验证

构建：

```text
16 passed
BUILD_EXIT_CODE=0
```

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
密钥检查：未发现问题（文件 105 个，含 Git 历史）
```

镜像：

```text
course1020-buildchecker:241880369
sha256:8364984fa2a1325a20d707d46577b42622c7d08035dcd9560a7c8714e6818ebb
```

证据路径：

```text
work/build-boundary/unit-tests/stdout.log
work/e7-boundary/gate/gate-result.json
```

## 3. CI 结果

PR #4 的 `e7-a-quality-gate` 检查全部通过：

- 代码提交 `5a906d5`：run 40499695852、40500116665
- 记录提交 `541ac44`：run 40500335454、40500345205

## 4. 合并尝试与阻塞

```text
MERGE_ATTEMPT_EXIT_CODE=1
X Pull request #4 is not mergeable: the base branch policy prohibits the merge.
```

证据：

```text
work/ci-boundary/PR-before-merge.json
work/ci-boundary/merge-rejection.log
```

Ruleset `main`（ID `25866762`）：

- 必填检查名：`e7-quality-gate`
- Workflow 实际上报：`e7-a-quality-gate`（App ID 15368）
- `current_user_can_bypass`: `never`
- `Allen-Ga` 权限：`admin:false, maintain:false`

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
work/final-records/pr2-checks.txt
work/final-records/pr3-checks.txt
work/final-records/pr4-checks.txt
work/final-records/ruleset-main.json
work/final-records/repo.json
work/final-records/artifacts/40342643704/
work/final-records/artifacts/40342653053/
work/final-records/artifacts/40323775871/
work/final-records/artifacts/40323785662/
work/final-records/artifacts/40500335454/
work/final-records/artifacts/40500345205/
```

## 7. 待完成

- 仓库管理员把 Ruleset `main`（ID `25866762`）的必填检查名改为 `e7-a-quality-gate`，或把 `Allen-Ga` 提升为 admin。
- 合并 PR #2、PR #3、PR #4。
- 保存最终 MERGED 记录。
- PR #2 合并后，把本记录补入 `docs/reports/A09-contributions.md` 和 `docs/reports/A09-acceptance.csv`。
