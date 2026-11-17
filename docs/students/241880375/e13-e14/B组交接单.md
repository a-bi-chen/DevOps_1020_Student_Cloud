# E13 A→B 报告交接单

- 提供方：A09 / 张海洋 241880375
- 接收方：B09
- 日期：2026-11-17
- A 仓库：<https://github.com/a-bi-chen/DevOps_1020_Student_Cloud>
- A 分支：`student/241880375/e13-e14`
- A 判定提交：`3231950cf151ef407804c6fc7767d6d6a387bbb5`（文档提交另计）

## B 项目与提交

- B 仓库：<https://github.com/llxxy-cn/devops-b09>
- 项目相对路径：`fixtures/e11e12-b1-real`
- base：`30ffe4c41492334478a2446a8be0662d3f31d478`
- target：`a7e3b644ca9b1b9d0b26bd41e839fcbf5ea1c293`
- 预期行为：目标提交新增 `extra.h`，程序输出 `hello E3`

## A 当次报告

- 报告文件（仓库内）：`evidence/students/241880375/e13-e14/handoff/fixed-md-b.json`
- SHA256：`ee70139fa5e7b606400ed830e5c2839f42279ee9db5a658d774d27b080b0e7df`
- 来源 job_id：`job-f18dbac70128426dbea57fc516b19ce3`
- 来源 trace_id：`trace-59fad11cb5db435e8676aa2541847a1b`
- A 侧发现：`MISSING(main.o, extra.h)`
- A 侧结果目录：`work/e13-c1-b09-01`（本提交包内归档）

## B 组需要执行

1. 在 B 分支导入：
   - `labs/e13e14/handoff_a_to_b.py`
   - 带 `fixed_report_sha256` 校验的 `labs/e11e12/pipeline.py`
2. 用本交接单报告的 SHA256 设置请求字段 `fixed_report_sha256`，不要沿用旧 SHA。
3. 对同一 base/target 运行 B 的 DRAFT/MDFixer 链路，保存：
   - 请求 JSON、`fixed_report_sha256`
   - `fixed-md-input.json` 中的 `source_report`
   - B 的 job_id / trace_id
   - 构建、修复、验证和复检日志
   - 补丁与最终 `recheck` 结果
4. 回传以下字段：
   - B 的 job_id / trace_id
   - 是否成功消费报告（`accepted`）
   - 补丁 SHA256
   - `recheck` 是否无 `MISSING`
   - B 的结果目录或提交链接
   - B 侧 CI 运行链接（如有）

## 注意

- 不要修改报告字节；若修改，保留原 SHA 重跑应得到 `ARTIFACT_HASH_MISMATCH`。
- 不要用 E11–E12 的旧 fixed-md 或旧 job 冒充本轮 C1。
- B 的独立回执到齐前，A 侧不把组级 E13 门禁写成完全通过，也不创建 `v0.9-rc`。
