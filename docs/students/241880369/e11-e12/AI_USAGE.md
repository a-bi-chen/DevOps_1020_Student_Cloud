# AI 使用记录

- 工具/模型/日期：opencode（deepseek-flash），2026-11-17
- 输入上下文与问题：E11–E12 课程材料、`A09_高嘉程_关键信息.md`、团队 `main` 上的 `run_e11e12.py` 与 `labs/e11e12`、E8–E10 个人报告。目标是补齐 241880369 的 E11–E12 个人实验、独立测试、报告和 PR 证据。
- 模型建议：
  1. 从最新 `main` 建 `student/241880369/e11-e12`，不重写团队编排代码。
  2. 新增 `fixed_report` 必须位于 `/course/data` 的独立契约测试。
  3. 复用团队真实项目 `course-one/make-introduction` 的适配 fixture，但由本人重新运行 E12。
  4. DRAFT 首次构建因 Debian 官方源过慢超时，候选 Dockerfile 切换清华源后重跑。
  5. 报告中的 `job_id/trace_id/SHA/validation` 一律从实际产物读取，不复制队友结果。
- 采纳/拒绝及理由：
  - 采纳：复用 `main` 编排、独立测试、真实项目复跑、清华源修复、API 幂等/409/哈希验证。
  - 拒绝：重新实现一套 E11/E12（会破坏 E8–E10 已验证接口）；只用固定样例（不能作为真实项目验收）；复制队友 `job_id/trace_id`（违反个人可追溯要求）。
- 人工修改：本人确认了分支、服务器路径、镜像名、真实项目 base/target、B09 签收引用范围；本人复核了报告中的每个 `job_id/trace_id/SHA` 与 `work/e11e12-personal-summary.json` 一致。
- 实际验证命令/输入/结果：
  - `python3 run_e11e12.py build` → 镜像 `course-e11e12:241880369`，ID `sha256:ba4e7393...`
  - `python3 run_e11e12.py test` → 12 tests OK；新增测试后 13 tests OK
  - `e11-a` → `job-efc49baae58c414490f14be0275a413a`，`SUCCEEDED`
  - `e12` 固定样例 → `job-81be941f47fd4f8fa5a903f5a5455b6c`，五阶段 `SUCCEEDED`
  - `e12` 真实项目 → `job-268fc09fa76c4f8391867c2da7d950d8`，五阶段 `SUCCEEDED`
  - API → `job-045cf351d04e4b5fa6c9ffe7f4ae26c3`，同键同 job、冲突 409、产物哈希一致
- 未调用模型的部分：编译器、BuildChecker、EChecker、DRAFT/MDFixer 的运行结果均由真实命令产生；模型没有伪造任何实验数值。
- 贡献边界：E11-B 和 B09 正式签收是团队已有证据，报告中已明确标注为“团队证据引用”；本人 E11-A、E12 固定样例、E12 真实项目和 API 均为本人重新运行。
- 安全：未把服务器密码、GitHub Token、私钥写入仓库、报告、日志或截图；`data/`、`work/` 按 `.gitignore` 忽略。
