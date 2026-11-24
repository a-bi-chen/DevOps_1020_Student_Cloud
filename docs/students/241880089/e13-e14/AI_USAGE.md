# AI 使用记录（E13–E14）

- 工具 / 模型 / 日期：Claude Code（deepseek-flash），2026-11-24
- 输入上下文与问题：E13/E14 操作手册与授课 PDF、B09 发来的合并后补充核验消息、团队 `main` 上的 E13–E14 组级材料（241880369 / 241880374 / 241880375）、本人 2026-11-17 的 E13 暂存证据与服务器 `work/e13-b09-reverify-20261124`。目标是核对 241880089 的 P8 实现，并补齐本人 E13 个人材料与 PR。

## 模型建议

1. 先做只读审计：本地、课程服务器、GitHub `main`/分支三处对照，不先改仓库。
2. 个人分支只提交本人真实执行过的 E13 C1 交叉检测；C2–C8、H1–H3、E14 引用组级材料，不复制队友的 job/trace。
3. 以 2026-11-24 服务器复跑的 94 项证据为主证据，生成确定性 tar.gz、`run-summary.json` 和 94 项 `SHA256SUMS`。
4. 新增 `labs/e13` 适配入口的说明与一个自包含测试，验证 `?=`/`:=` 声明解析和 `UNSUPPORTED_FLAGS` 拒绝路径。
5. 合并后复跑只回答“固定项目提交的检测结论是否改变”，不移动 `v0.9-rc`、不替换 2026-11-23 已签收包。

## 采纳 / 拒绝及理由

- 采纳：只读审计、E13 C1 个人切片、94 项证据归档、适配器测试、如实标注未执行项。
- 拒绝：把 C2–C8 / H1–H3 / E14 写成个人完成（没有本人运行证据）；复制队友 `job_id`/`trace_id`；为了“补齐”而修改 `labs/e11e12` 判定逻辑或 B09 仓库；移动 `v0.9-rc`。

## 人工复核项（提交前由本人确认）

- 个人分支名、服务器路径、镜像名与本人学号一致；
- 报告中 Base/Target、findings、`added/resolved/refreshed/reused` 与 `detection-report.json` 一致；
- 94 项 `SHA256SUMS` 在服务器上 `sha256sum -c` 退出码 0；
- 证据包 SHA256 `69ef46da…c37d22`、检测报告 SHA256 `7f624d28…b876` 与仓库文件一致；
- `v0.9-rc` 仍指向 `ee6f7da9…`，未被本次提交移动。

## 实际验证命令 / 输入 / 结果（2026-11-24，云主机 `/root/241880089/devops-e11e12`）

- Base：`30ffe4c41492334478a2446a8be0662d3f31d478`；Target：`a7e3b644ca9b1b9d0b26bd41e839fcbf5ea1c293`
- 项目子目录：`fixtures/e11e12-b1-real`；期望输出：`hello E3`
- BuildChecker：Base `SUCCEEDED` 无缺陷；Target `SUCCEEDED`，`MISSING(main.o, extra.h)`
- EChecker 增量：`added=[["MISSING","main.o","extra.h"]]`，`resolved=[]`，与 Target 全量一致
- 原始命令：Base / Target 的 `make clean`、`make`、`make test`、`./app` 均退出 0
- 证据：`work/e13-b09-reverify-20261124`，94 项 `SHA256SUMS` 全通过

## 未调用模型 / 未伪造的部分

- 编译器、BuildChecker、EChecker、strace 的结果均由服务器真实命令产生；模型没有伪造任何数值。
- 未把服务器密码、GitHub Token、私钥写入仓库、报告、日志或证据包。
- 未修改 B09 仓库、未改写两个原始提交、未改动已签收包字节。

## 贡献边界

本人在 E13–E14 的个人贡献是 A 侧 C1 交叉检测及其 2026-11-24 复跑。组级 C2–C8、H1–H3、E14 四容器与 `v0.9-rc` 由团队完成，报告中已标注为“组级引用”，不计入本人个人完成项。
