# AI 使用记录

工具/模型/日期：Codex（OpenAI coding agent），2026-11-03。

## 输入上下文与问题

- 输入：E8 文件夹中的 A09 任务分工、老师 E8/E9 A 组操作手册、个人测试示例、提交与排错手册、实验包源码。
- 问题：完成张海洋（241880375）的第 0 步、E8 A 真实基线、E9 A C0—C3、个人独立测试、报告与 GitHub 提交准备。

## 模型建议

- 按老师手册逐步执行 E8/E9，而不是只运行一键 demo，以保留每一步 `steps/` 日志。
- 使用 BuildChecker actual-graph 作为 E8 历史图来源，并保留 GCC 投影作为独立核对。
- 采用保守缓存 key：所有本地 C/H 指令、配方、flags、编译器版本；C2 刷新两个目标。
- 新增 `StudentE9A.test_include_inside_header_invalidates`，断言 actual、added、refreshed、reused。

## 采纳/拒绝及理由

- 采纳：逐步手册路线、BuildChecker 来源标注、保守刷新、独立测试类。
- 采纳但加强：在老师示例的 `assertIn` 基础上增加 `added` 精确集合断言和 `reused==[]`，防止只检查单条边而漏掉额外发现。
- 拒绝：把 E10 结果写入张海洋报告；E10 不由张海洋负责。
- 拒绝：伪造课程 B 组 Patch/validation 返回；当前只准备冻结交接包。

## 人工修改

- 张海洋的 Git 身份设置为 `241880375 <241880375@njupt.edu.cn>`，与本人既有提交记录一致。
- 人工核对 BuildChecker 原始 trace、make-db、baseline/incremental JSON 与 C0—C3 内部 commit。
- 人工确认只用真实 OUT 数据填写报告，未使用教师示例路径或论文性能数字。
- 人工确认报告中不包含服务器密码、Token 或其他凭据。

## 实际验证命令/输入/结果

```bash
# 环境
python3 run_lab.py build
docker image inspect course-e8e10:241880375

# E8 A
lab_new_run e8 A
lab_python "$OUT" <<'PY' ... fixture/scan/buildchecker/incremental ... PY

# E9 A
lab_new_run e9 A
lab_python "$OUT" <<'PY' ... C0/C1/C2/C3 ... PY

# 单元测试
docker run --rm --network none --user "$(id -u):$(id -g)" \
  -e HOME=/tmp -v "$PWD:/course" -w /course course-e8e10:241880375 \
  python3 -m unittest discover -s labs/e8e10 -p test_profile.py -v
```

实际结果：E8 A `BASELINE_PASS`、`BUILDCHECKER_BASELINE_PASS`、`REUSE_PASS`；E9 A `C0_BUILD_AND_BASELINE_PASS`、`C1_REUSE_PASS`、`C2_REFRESH_PASS`、`C3_RESOLVED_PASS`；单元测试 `Ran 8 tests ... OK`。

## 贡献边界

参考实现 `labs/e8e10/lab.py` 来自课程实验包，张海洋未修改其核心算法。张海洋的个人代码贡献是 `labs/e8e10/test_profile.py` 中的 `StudentE9A` 独立测试类；个人实验贡献是 E8/E9 A 的真实运行、证据冻结和报告。E10 与课程 B 组往返不由本报告冒充完成。

## E10 补跑记录（老师 2026-11-03 更新要求）

老师更新要求：组内每个人都要在自己的分支上完整跑通本轨道 E8—E10；与 B 组交换/联调推迟到 E11—E12。

Codex 按 `10_E10_A组.md` 逐步执行 E10 A：

- 六个场景各 5 次增量/全量对照；
- 30 行 `results.csv` 全部 `equal=True`；
- 保存 `performance-summary.csv`、`gate.json` 和最终 BuildChecker 证据；
- 模型建议保留真实计时，不把刷新场景的接近 1 的比值包装成论文加速倍数；
- 人工核对六类复用/刷新、最终 `REDUNDANT unused.h`、trace id 和 SHA256。

实际结果：`MATRIX_PASS {'unchanged': 5, 'body': 5, 'include': 5, 'declaration': 5, 'flags': 5, 'header': 5}`、`DYNAMIC_CROSSCHECK_AND_MATRIX_PASS`。E10 未新增第二个测试，个人独立测试仍为 `StudentE9A.test_include_inside_header_invalidates`，避免与高嘉程负责的 E10 测试冲突。
