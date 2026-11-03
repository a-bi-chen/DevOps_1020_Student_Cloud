# AI使用记录

工具/模型/日期：

- Claude Code（AI 编码助手），2026-11-03。

输入上下文与问题：

- 上下文：A09 组 A 轨 P6，`main` 已整理为 E8–E10 模板；需要在 `student/241880089/e8-e10` 分支完成 A 轨 E8、E9、E10。
- 问题：如何在不具备本地 Docker 的 Windows 环境完成 A 轨真实 BuildChecker 基线；如何补与组内其他用例不重复的个人测试；如何归档 CI artifact、写报告，并做两次独立检验。

模型建议：

- 先同步分支到最新 `main`，建立 `docs/students/241880089/e8-e10/` 并触发 CI。
- 用 CI 的 `ubuntu-24.04` + `course-e8e10:ci` 执行 `lab.py e8/e9/e10 --track A`，下载 artifact 归档，而不是用本地 GCC `-MM` 冒充 BuildChecker。
- E8 个人测试选“Makefile 配方变化使缓存失效”；E9 选“头文件宏值变化使缓存失效但依赖图不变”；E10 选“新增无关头文件触发保守刷新且增量等于全量”，与组内已有的“新增 include”“声明变化”“间接 include”用例区分。
- 独立检验分两层：方法层做增量 vs 全量、BuildChecker vs GCC；运行层在同一提交上做第二次 CI 并比较语义字段。
- 报告中区分外层分支 SHA、样例内部 C0 提交和镜像 ID；明确标注 BuildChecker 在 CI 而非本机执行。

采纳/拒绝及理由：

- 采纳：CI 执行与 artifact 归档；三个个人测试；方法层与运行层两次独立检验；报告中的环境/证据对应关系。
- 拒绝：在本机用 `scan()` 结果代替 E8/E10 真实 BuildChecker；引用旧运行或他人运行；在未完成 E9/E10 时声称已完成；把 B 轨结果混入 A 轨结论。

人工修改：

- 由本人确认 E8/E9/E10 的预期依赖、findings、复用/刷新方向，核对 `baseline.json`、`C1/C2/C3.json`、`results.csv`、`gate.json` 与 BuildChecker 产物。
- 由本人复核三个个人测试类的类名与断言，未直接复制组内其他成员用例。
- 由本人决定只做 A 轨；B 轨留给 B 组在自己的分支完成。

实际验证命令/输入/结果：

```bash
cd labs/e8e10
python3 -m unittest discover -s . -p test_profile.py -v
# Ran 10 tests ... OK（课程 7 项 + 本人 3 项）

# CI（容器内）
python3 labs/e8e10/lab.py e8 --track A --out /course/work/A-e8
python3 labs/e8e10/lab.py e9 --track A --out /course/work/A-e9
python3 labs/e8e10/lab.py e10 --track A --out /course/work/A-e10
# E8 BuildChecker status=SUCCEEDED；E10 gate rows=30, passed=true
```

- E8 CI run `41662015872` 成功；E9/E10 CI run `41663999896` 成功；个人测试与 E8 报告提交 `39d3ff7` 由 run `41663498413` 验证成功。
- 第二次独立运行 `41666559898`（`workflow_dispatch`，同一 headSha `5312b6d`）成功；语义比较 `differences=[]`。
- artifact `e8e10-evidence-41662015872`、`e8e10-evidence-41663999896`、`e8e10-evidence-41666559898` 已下载，关键文件归档到 `work/`。

未调用模型时写明未调用；记录参考实现和自己的贡献边界：

- 教学实现 `lab.py`、BuildChecker 与 workflow 来自课程参考实现，本人未修改其逻辑。
- 本人贡献：个人测试 `StudentE8A089`、`StudentE9A089`、`StudentE10A089`，E8/E9/E10 运行归档，两次独立检验的脚本与记录，报告、ADR 与 AI 使用记录；AI 助手参与了分支操作、artifact 下载脚本、复核脚本与文字草稿，结论由本人核对。
