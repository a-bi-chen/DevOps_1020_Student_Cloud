# AI使用记录

工具/模型/日期：

- Claude Code（AI 编码助手），2026-11-03。

输入上下文与问题：

- 上下文：A09 组 A 轨 P6，`main` 已整理为 E8–E10 模板；需要在 `student/241880089/e8-e10` 分支完成 E8。
- 问题：如何在不具备本地 Docker 的 Windows 环境完成 A 轨真实 BuildChecker 基线；如何补一个与组内其他用例不重复的个人测试；如何归档 CI artifact 并写报告。

模型建议：

- 先同步分支到最新 `main`，建立 `docs/students/241880089/e8-e10/` 并触发 CI。
- 用 CI 的 `ubuntu-24.04` + `course-e8e10:ci` 执行 `lab.py e8 --track A`，下载 artifact 归档，而不是用本地 GCC `-MM` 冒充 BuildChecker。
- 个人测试选择“Makefile 配方变化使缓存失效”，与组内已有的“新增 include”“声明变化”“间接 include”用例形成互补。
- 报告中区分外层分支 SHA、样例内部 C0 提交和镜像 ID；明确标注 BuildChecker 在 CI 而非本机执行。

采纳/拒绝及理由：

- 采纳：CI 执行与 artifact 归档；配方变化测试；报告中的环境/证据对应关系。
- 拒绝：在本机用 `scan()` 结果代替 E8 真实基线；引用旧运行或他人运行；在未完成 E9/E10 时声称已完成。

人工修改：

- 由本人确认 E8 的预期依赖与 findings，核对 `baseline.json`、`incremental.json`、`buildchecker/findings.json` 与 trace 行。
- 由本人决定只提交 E8，E9/E10 留待后续完成；报告中的结论与未完成项由本人负责。
- 个人测试类名与断言由本人复核，未直接复制组内其他成员用例。

实际验证命令/输入/结果：

```bash
cd labs/e8e10
python3 -m unittest discover -s . -p test_profile.py -v
# Ran 8 tests ... OK

# CI（容器内）
python3 labs/e8e10/lab.py e8 --track A --out /course/work/A-e8
# COMPLETED e8 A ...；BuildChecker status=SUCCEEDED
```

- CI run `41662015872` 成功；`e8e10-quality-gate` 与 `e7-a-quality-gate` 均为 success。
- artifact `e8e10-evidence-41662015872` 已下载，`A-e8` 归档到 `work/e8-A-ci-41662015872/`。

未调用模型时写明未调用；记录参考实现和自己的贡献边界：

- 教学实现 `lab.py`、BuildChecker 与 workflow 来自课程参考实现，本人未修改其逻辑。
- 本人贡献：个人测试 `StudentE8A089.test_recipe_change_invalidates_cache`、E8 运行归档、报告与 ADR；AI 助手参与了分支操作、artifact 下载脚本与文字草稿，结论由本人核对。
