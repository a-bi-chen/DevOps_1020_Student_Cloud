# A09 E7 项目根边界测试记录

## 基本信息

- 执行人：高嘉程（241880369）
- 分支：`e7-boundary-test-241880369`
- 代码提交：`5a906d59e9bcdcea751ec74042661d0051612c3c`
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

证据路径：

```text
work/build-boundary/unit-tests/stdout.log
work/e7-boundary/gate/gate-result.json
```

## 3. CI 结果

PR #4 的 `e7-a-quality-gate` 检查通过：

- run 40499695852（push）
- run 40500116665（pull_request）

## 4. 待完成

- 当前 Ruleset 必填检查名仍为 `e7-quality-gate`，而 workflow 上报 `e7-a-quality-gate`，因此 PR #4 显示 `BLOCKED`。
- 需要仓库管理员将 Ruleset `main`（ID `25866762`）的必填检查名改为 `e7-a-quality-gate`，或将 `Allen-Ga` 提升为 admin 后由本人修改。
- Ruleset 修正后合并 PR #4。
- PR #2 合并后，把本记录补入 `docs/reports/A09-contributions.md` 和 `docs/reports/A09-acceptance.csv`。
