# 决策记录（ADR）

**背景与约束**

- 课程要求 E8–E10 每人在本人分支上完整跑通 A 组参考流程，保留运行结果，并提交个人报告与贡献。
- 本人为 A 组（BuildChecker/EChecker），使用 `labs/e8e10` 受限教学实现；服务器为共享 root，仓库受 `main` Ruleset 保护。
- 参考文献中的大项目规模与性能数值不作为本样例验收值。

**选择与替代方案**

1. 入口选择：使用 `run_lab.py` 一键入口跑 E8/E9/E10，并额外用 `lab_new_run e10 A` + 详细矩阵脚本跑 E10。
   - 替代：仅用一键入口。放弃原因：一键 E10 不生成 `performance-summary.csv` 和每场景 5 对原始 JSON，证据不足以支撑报告中的 30 行矩阵与性能统计。
   - 替代：仅用详细手册逐块执行。放弃原因：E8/E9 的一键入口与详细路线核心函数相同，且一键已由 CI 验证；为控制时间，E8/E9 用一键，E10 用详细路线。
2. 缓存失效与配置身份：采用教学实现的“预处理/配方/配置签名”复用；`include` 新增或 `CFLAGS` 变化触发保守刷新（两目标）。
3. B 组共享变量与失败保护：本轮不做 B 组；A 组的失败保护体现在 `patch()` 的 `STALE_REPORT`/`UNSAFE_PATH` 拒绝与源文件原字节保持（由既有 7 项测试覆盖）。

**代价与覆盖范围**

- 教学实现只支持两个固定对象目标、顶层 C/H、显式规则、简单变量与受限 CFLAGS；不覆盖隐式规则、递归 Make、符号链接、数字目录 FD 等。
- E10 的 include/flags/header 场景因保守刷新，增量与全量耗时接近（≈1.0×）；unchanged/body/declaration 复用后增量约为全量的 1/6。该数据仅代表本机小样例。
- 使用一键 E8/E9 时，`student-source-commit.txt` 与 `environment-image-id.txt` 不由入口自动生成，已按实际 `git rev-parse HEAD` 和 `docker image inspect` 补齐，并在 `command.txt` 记录命令，保证可追溯。

**验证命令与实际证据**

- E8：`work/e8-A-run-20261103-194013/{baseline.json,incremental.json,buildchecker/}`
- E9：`work/e9-A-run-20261103-194013/{baseline.json,C1.json,C2.json,C3.json,C0/C1/C2-build.log}`
- E10：`work/e10-A-manual.2Dt2nm/matrix/{results.csv,performance-summary.csv,gate.json,*-r{1..5}-*.json,final-buildchecker/}`
- 单测：`work/unit-tests-20261103-194013.log`（Ran 8 tests, OK）
- 镜像：`course-e8e10:241880369` = `sha256:57a8782f82f3f4659b625eef235afa6c0b7ec953e479af13010ab37fe8c4504e`
- 运行基线源码 SHA：`83cc2be2dbeff487d4bc73861ddff843f3306848`
