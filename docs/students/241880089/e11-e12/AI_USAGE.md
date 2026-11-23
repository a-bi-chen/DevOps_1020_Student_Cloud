# AI 使用记录

- 工具/模型/日期：Claude Code（deepseek-flash），2026-11-17
- 输入上下文与问题：E11–E12 课程材料、`DevOps_E11_E12` 操作手册、团队 `main` 上的 `run_e11e12.py` 与 `labs/e11e12`、三名成员已合并的 E11–E12 个人材料、E8–E10 个人报告。目标是补齐 241880089 的 E11–E12 个人实验、独立测试、报告和 PR 证据。
- 模型建议：
  1. 从最新 `main` 建 `student/241880089/e11-e12`，不重写团队编排代码。
  2. 新增 macro / mixed 依赖声明风格的独立契约测试，覆盖 MDFixer 补丁位置，且不删除 RD。
  3. 运行固定样例 E11-A/E11-B/E12，并单独运行真实项目 E12。
  4. 使用个人端口（8081）和个人 work 目录，避免与共享服务器上的队友冲突。
  5. 报告中 `job_id/trace_id/SHA/validation` 一律从实际产物读取，不复制队友结果。
- 采纳/拒绝及理由：
  - 采纳：复用 `main` 编排、macro/mixed 独立测试、真实项目复跑、API 幂等/409/哈希验证、证据按学号归档。
  - 拒绝：重新实现一套 E11/E12（会破坏 E8–E10 已验证接口）；只用固定样例（不能作为真实项目验收）；复制队友 `job_id/trace_id`（违反个人可追溯要求）。
- 人工修改：本人确认分支、服务器路径、镜像名、真实项目 base/target、B09 签收引用范围；本人复核报告中的每个 `job_id/trace_id/SHA` 与实际产物一致。
- 实际验证命令/输入/结果（2026-11-17 云主机 `/root/241880089/devops-e11e12`）：
  - `python3 run_e11e12.py build` → 镜像 `course-e11e12:241880089`，ID `sha256:cc0d1e40…`
  - `python3 run_e11e12.py test` → `Ran 14 tests in 0.035s`，`OK`
  - `e11-a` → `SUCCEEDED`，`job-506c114f29664c588fc17c914b39b5ab` / `trace-95ad2ec832be4b07815e703780c8c9ee`
  - `e11-b` → `SUCCEEDED`，`job-e5e75ddaac104eb28922e26abb29446c` / `trace-37b4970898e74ee182d859e3fcc75914`
  - `e12` 固定样例 → `SUCCEEDED`，五阶段齐全，`job-d33929c866124b9891dfda0719dc68f4` / `trace-123acdc32e1e4446af2ee9b080866ab7`
  - `e12` 真实项目 → `SUCCEEDED`，五阶段齐全，`job-ebf15bedbe6a4a26b9cc2bf594b1e1ec` / `trace-49d42f19ea644235b65eac8c77ec2e56`
  - API → `job-f85899a7364d426e83d9d5133db80e63` / `trace-dfea29f8f40a44e8a6b570de002ced32`；同键同参同 job、改参 409、产物三处 SHA 一致、重启后已完成任务保留且未完成任务标记 `SERVER_RESTARTED`
- 环境适配（非模型建议）：`deb.debian.org` 实测约 19 KB/s，导致 DRAFT 600 s 超时；在候选 Dockerfile 的 apt 行前加入清华镜像 `sed`，原始候选另存为 `candidate.original.Dockerfile`，并用 `prepare_candidate` 复核基线语义不变。
- 未调用模型的部分：编译器、BuildChecker、EChecker、DRAFT/MDFixer 的运行结果均由真实命令产生；模型没有伪造任何实验数值。
- 贡献边界：E11-B 和 B09 正式签收是团队已有证据，报告中已明确标注为“团队证据引用”；E11-A、E11-B、E12 固定样例、E12 真实项目和 API 均需本人在个人环境重新运行并记录。
- 安全：未把服务器密码、GitHub Token、私钥写入仓库、报告、日志或截图；`data/`、`work/` 按 `.gitignore` 忽略。
