# ADR：E11–E12 集成接口决策

- 编号：ADR-241880089-e11e12-01
- 日期：2026-11-17
- 作者：陈玉熙 / 241880089 / A09 A 轨（BuildChecker → EChecker）

## 问题

如何在不重写 E8–E10 已验证能力的前提下，把 BuildChecker/EChecker 与 DRAFT/MDFixer 串成可核验的 E11/E12 流程，并让 A/B 双方通过统一接口消费带版本和哈希的产物？

## 候选方案

1. 重新实现一套 E11/E12 编译器、检测器和修复器。
2. 复用团队 `main` 上已有的 `run_e11e12.py` 和 `labs/e11e12` 编排，个人分支只补独立测试、真实运行和证据。
3. 只运行固定样例，不接真实项目，不验证 API。

## 采用方案与原因

采用方案 2：

- 复用 `labs/e8e10/lab.py` 的 `scan/patch/validate`，不改变 E8–E10 的 GCC `-MM` 增量语义。
- 复用 `buildchecker.fullcheck.full_check` 生成真实 strace 全量图和 Make 数据库。
- 复用 `labs/e11e12/vendor/draft/autobuild.py` 做真实 DRAFT 两轮构建和容器运行。
- 由 `labs/e11e12/pipeline.py` 编排，统一输出 `schema_version=e11e12-1` envelope：
  `job_id / trace_id / kind / commit / status / data / artifacts[uri,sha256,bytes]`。
- E12 的 MDFixer 输入强制取自本轮 `incremental-check.json`，不再使用固定 `fixed-md.json`。
- API 使用 `idempotency_key`、`job_id`、`trace_id`、`artifact://job/相对路径` 和 `X-Content-SHA256`。

不选方案 1：会破坏 E8–E10 已验证的接口和团队 CI，且无法在课堂时间内重新验证全部路径。

不选方案 3：固定样例不能作为真实项目接入的验收证据，也无法证明 E12 的真实报告消费。

## 输入输出字段

- 输入：`mode`（`e11-a`/`e11-b`/`e12`）、`repo`、`base`、`target`、`candidate`、`fixed_report`、`expected_output`、`build_timeout`。
- 输出：统一 envelope；`full-check` 对应 base commit，`incremental-check/repair/recheck` 对应 target commit。
- API：`POST /v1/jobs`、`GET /v1/jobs/{id}`、`GET /v1/jobs/{id}/artifacts`、`GET /v1/jobs/{id}/files/{path}`。
- 状态码：202 提交成功；400 输入错误；409 幂等冲突或结果未生成；404 不存在或路径越界。

## 兼容性与测试

- 保留 E7、E8–E10 原文件和 workflow，不覆盖旧检查。
- 现有契约测试与三名成员的个人测试全部通过；新增本人测试后共 14 项通过（本地预检）。
- 个人测试：`StudentE11E12A241880089.test_macro_and_mixed_dependency_patch_lands_on_declaration`，验证 macro / mixed 风格下补丁追加到正确声明位置，且不删除 RD。
- E11-A：`baseline-full/actual-graph.json` 投影与 `baseline-cache.json` 一致；目标增量 findings 与目标全量 findings 一致。
- E12 固定样例和真实项目：五阶段全部成功；`accepted=true`；recheck 无 MD、保留 RD。
- API：相同键同输入返回同一 job；冲突返回 409；下载文件 SHA256 与清单及 `X-Content-SHA256` 一致。

## 代价与覆盖范围

- 教学实现仍只支持 `main.c/helper.c/config.h + 显式 Make` 的受限子集；真实项目需要适配并记录。
- DRAFT 构建依赖外部 apt 源；候选 Dockerfile 使用固定基础镜像和国内镜像源保证可重复，`data/` 不提交。
- 真实项目适配复用 A09 团队共享的 `course-one/make-introduction` fixture；本人在个人环境独立运行并记录自己的证据。
- 分机联调若因缺少第二名参与者未完成，将在个人报告中明确标注“未完成”。
