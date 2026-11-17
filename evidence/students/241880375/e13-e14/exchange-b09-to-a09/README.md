# B09 → A09 E13 项目检测结果

- 执行方：A09 / 241880375 张海洋
- 提供方：B09
- 日期：2026-11-17
- 状态：A09 全量/增量检测完成；等待 B09 消费 A09 交换项目并回传构建、修复、复检结果

## 1. 项目与提交

| 项目 | 值 |
|---|---|
| B09 仓库 | <https://github.com/llxxy-cn/devops-b09> |
| 项目子目录 | `fixtures/e11e12-b1-real` |
| Base | `30ffe4c41492334478a2446a8be0662d3f31d478` |
| Target | `a7e3b644ca9b1b9d0b26bd41e839fcbf5ea1c293` |
| 构建命令 | `make clean && make` |
| 测试命令 | `make test` |
| 运行命令 | `./app` |
| 预期/实际输出 | `hello E3` |

A09 当前入口支持 `project_subdir`，已在 B09 仓库根目录下切换到 `fixtures/e11e12-b1-real` 执行，完整 base/target SHA 均未改写。

## 2. 手工构建和运行

- Base 运行记录：`run-base.log`，退出码 0，输出 `hello E3`
- Target 运行记录：`run-target.log`，退出码 0，输出 `hello E3`

## 3. A09 全量/增量检测

| 字段 | 值 |
|---|---|
| 状态 | `SUCCEEDED` |
| job_id | `job-f18dbac70128426dbea57fc516b19ce3` |
| trace_id | `trace-59fad11cb5db435e8676aa2541847a1b` |
| result.json SHA256 | `4e528cb510c736876e6aacaf4bf0244fe4ea56fe5cda33e63eac46e6232a3602` |
| full-check.json SHA256 | `af401bfd6795266cc474d364dddc49c9df7b8831d39665bf9828e30f2b9a8f55` |
| incremental-check.json SHA256 | `6fd68688873fdd1aa24ea5de5c5d9202580e560bc62ff476f7363d0f442a7f04` |
| 原始证据包 | `e13-c1-b09-detection-evidence.tar.gz` |
| 原始证据包 SHA256 | `22241fb4430cbeb7431f1b31e6b3e1bc4afd8c6eaf90c1f56f18fa94e9830784` |

- Base 全量发现：空。
- Target 全量发现：`MISSING(main.o, extra.h)`。
- Target 增量发现：`MISSING(main.o, extra.h)`。
- 全量与增量结果一致。

## 4. 给 B09 消费的 A→B 报告信封

- 文件：`fixed-md-b.json`
- SHA256：`ee70139fa5e7b606400ed830e5c2839f42279ee9db5a658d774d27b080b0e7df`
- source job_id：`job-f18dbac70128426dbea57fc516b19ce3`
- source trace_id：`trace-59fad11cb5db435e8676aa2541847a1b`
- source report URI：`artifact://job-f18dbac70128426dbea57fc516b19ce3/incremental-check.json`
- source report SHA256：`6fd68688873fdd1aa24ea5de5c5d9202580e560bc62ff476f7363d0f442a7f04`

B09 请求中的 `fixed_report_sha256` 应设置为 `ee70139fa5e7b606400ed830e5c2839f42279ee9db5a658d774d27b080b0e7df`，不得修改文件字节。

## 5. 请求文件

`request.json` 内容为 A09 实际使用的请求，关键字段：

```json
{
  "repo": "/course/data/b09-project",
  "project_subdir": "fixtures/e11e12-b1-real",
  "base": "30ffe4c41492334478a2446a8be0662d3f31d478",
  "target": "a7e3b644ca9b1b9d0b26bd41e839fcbf5ea1c293",
  "candidate": "/course/data/b09-project/docs/students/241880481/e11-e12/real-project/candidate.Dockerfile",
  "expected_output": "hello E3"
}
```

本目录的 `runtime-log-scan.txt` 为脱敏扫描结果。
