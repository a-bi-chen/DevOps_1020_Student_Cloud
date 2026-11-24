# 缺陷 Issue 与修复 PR

## Issue #19：B 组实际项目 Makefile 条件赋值与 CFLAGS

- 用例与发现方：E13 C1，张海洋（A09）
- 输入仓库及完整 SHA：<https://github.com/llxxy-cn/devops-b09>，base `30ffe4c41492334478a2446a8be0662d3f31d478`，target `a7e3b644ca9b1b9d0b26bd41e839fcbf5ea1c293`
- 预期 / 实际：预期 A 全量/增量成功；实际 `FAILED`，`EXECUTION_FAILED` / `UNSUPPORTED_FLAGS`
- 失败阶段、错误码和原始日志路径：首次 `scan(base_project)`；`work/e13-c1-b09-attempt1/result.json`；job `job-67b844e0ff814a21865f4d423228f5ae`
- 严重度：阻断 C1 双向交叉测试
- 最小复现：`python3 run_e11e12.py run --request data/e13-pair/b-to-a-real-request.json --out work/e13-c1-b09-attempt1`
- 是否影响其他任务：只影响使用 `?=`/`:=` 或 `-std=c11 -Wall -Wextra -Werror` 的项目；固定样例与 H1–H3 不受影响

## PR 修复：提交 `1eddc28`

- 关联 Issue：#19（提交信息 `Fixes #19`）
- 修改文件与原因：
  - `labs/e8e10/lab.py`：变量解析支持 `=`、`?=`、`:=`；把 B 项目的完整 CFLAGS 字符串加入显式白名单
  - `labs/e8e10/test_profile.py`：新增 `StudentE13A241880375`，验证条件 flags 被记录且缓存复用
- 失败前证据 / 修复后同一测试证据：
  - 失败：`work/e13-c1-b09-attempt1`（`UNSUPPORTED_FLAGS`）
  - 成功：`work/e13-c1-b09-01`（`SUCCEEDED`，`MISSING(main.o, extra.h)`）
- 新增或修改的回归测试：1 项个人测试；E8–E10 共 15 项、E11–E12 共 15 项全部通过
- 原始仓库修复前后 SHA 核对：B 项目 base/target 未改变；A 代码修复提交 `1eddc28`
- CI 门禁链接与审查人：PR #20；`e8e10-quality-gate`、`e11e12-integration`、`e13e14` contracts
- 剩余风险：白名单仍是显式集合，遇到其他 flags 继续以 `UNSUPPORTED_FLAGS` 拒绝，而不是猜测

## Issue #21：CI 容器内 Git 拒绝 runner 属主工作目录

- 用例与发现方：E14 四容器 CI，张海洋（A09）
- 输入提交：`1eddc28`
- 预期 / 实际：预期五阶段完成；实际 echecker HTTP 422，`fatal: detected dubious ownership`
- 失败阶段、错误码和原始日志路径：echecker `scan(base)`；Actions run 44026158154 的 `four-services` 日志
- 严重度：阻断 E14 CI
- 最小复现：GitHub Actions checkout 后以 runner 属主运行 `prepare`，Compose 服务以 root 读取同一工作目录
- 是否影响其他任务：只影响非 root 属主的 CI/宿主；云机 root 本地运行未复现

## PR 修复：提交 `3aba6ee`、`3231950`

- 关联 Issue：#21（PR #20 中说明）
- 修改文件与原因：
  - `labs/e13e14/compose.yaml`：定义共享环境锚点并在四个服务中合并 `GIT_CONFIG_COUNT/KEY_0/VALUE_0`；服务级 `environment` 会覆盖公共映射，因此不能只写在 `x-common`
  - `labs/e13e14/orchestrate.py`：端口可由环境变量指定；补充 repair/recheck 证据字段
- 失败前证据 / 修复后同一测试证据：
  - 失败：Actions run 44026158154
  - 修复后：同一 workflow 在 `3231950` 上重跑，`four-services` 通过（run 44027176500）
- 新增或修改的回归测试：Compose `config --quiet`；四容器固定样例 E2E；日志扫描
- 原始仓库修复前后 SHA 核对：未修改项目输入；仅服务运行环境变化
- CI 门禁链接与审查人：PR #20 Checks
- 剩余风险：`safe.directory=*` 仅在容器内生效；若未来服务以非 root 且挂载不可信仓库，仍需额外隔离
