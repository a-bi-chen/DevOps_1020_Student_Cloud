# A09 组 E8–E12 统一仓库（A 轨 EChecker）

小组 / 轨道：A09 / A（BuildChecker → EChecker 教学实现）

仓库：<https://github.com/a-bi-chen/DevOps_1020_Student_Cloud>

`main` 是本组 E8–E12 的统一验收版本：E8–E10 教学代码与四人个人测试（14 项）、E11–E12 轨道内集成与四人个人材料均已归档。E11–E12 的四份个人报告见 `docs/students/<学号>/e11-e12/`，团队级结果与 B09 签收见 `docs/reports/`。

## 1. 组员与分支

| 姓名 | 学号 | GitHub | E8–E10 分支 | E11–E12 分支 |
|---|---|---|---|---|
| 陈玉熙 | 241880089 | `a-bi-chen` | `student/241880089/e8-e10` | `student/241880089/e11-e12` |
| 高嘉程 | 241880369 | — | `student/241880369/e8-e10` | `student/241880369/e11-e12` |
| 马海川 | 241880374 | `weijige7` | `student/241880374/e8-e10` | `student/241880374/e11-e12` |
| 张海洋 | 241880375 | — | `student/241880375/e8-e10` | `student/241880375/e11-e12` |

E8–E10 个人测试类：`StudentE8A089`、`StudentE9A089`、`StudentE10A089`、`StudentE9A089RemovedInclude`、`StudentE10A`、`StudentE8A`、`StudentE9A`，合计 7 项个人测试 + 7 项基础 `ProfileTests` = **14 项**。

E11–E12 个人测试类：`StudentE11E12A241880089`、`StudentE11E12A241880369`、`StudentE11E12A241880374`、`StudentE11E12A241880375`。

## 2. 仓库结构

| 路径 | 阶段 | 内容 |
|---|---|---|
| `run_lab.py` | P6 | E8–E10 一键入口：`build` / `e8` / `e9` / `e10` |
| `labs/e8e10/lab.py` | P6 | EChecker 教学实现（GCC 依赖观测、缓存复用/刷新、Patch） |
| `labs/e8e10/test_profile.py` | P6 | 基础 `ProfileTests` 7 项 + 四人 E8–E10 个人测试 7 项 |
| `run_e11e12.py` | E11–E12 | `build` / `prepare` / `run` / `serve` / `test` 入口 |
| `labs/e11e12/` | E11–E12 | 编排、DRAFT/MDFixer、异步任务 API、契约测试与个人测试 |
| `services/buildchecker/`、`tests/e7/`、`scripts/` | P5 / E11–E12 | BuildChecker、E7 门禁、归档审计脚本 |
| `.github/workflows/e7-quality-gate.yml` | P5 | `e7-a-quality-gate` |
| `.github/workflows/e8e10.yml` | P6 | `e8e10-quality-gate`：单元测试 + A/B 六条路线 |
| `.github/workflows/e11e12.yml` | E11–E12 | `e11e12-integration`：契约测试 + E11-A/B/E12 运行 + artifact |
| `docs/students/` | P6–E11–E12 | 四人 E8–E10、E11–E12 个人材料与模板 |
| `docs/reports/` | E11–E12 | 团队交付审计、B09 签收核对与全量检查 |
| `evidence/students/` | E11–E12 | 按学号归档的原始日志、JSON、trace、证据包与 SHA256 清单 |

## 3. 快速开始（E8–E10）

```bash
git clone https://github.com/a-bi-chen/DevOps_1020_Student_Cloud.git
cd DevOps_1020_Student_Cloud
git config --local user.name 2418800XX          # 必须是纯数字学号
git config --local user.email <你的 GitHub 邮箱>
git switch -c student/2418800XX/e8-e10 origin/main
python3 run_lab.py build
python3 run_lab.py e8  --track A --out work/e8-A-run1
python3 run_lab.py e9  --track A --out work/e9-A-run1
python3 run_lab.py e10 --track A --out work/e10-A-run1
```

`--out` 必须是 `work/` 下尚不存在的新目录；`work/` 与 `data/` 不入库，需要保留的结果另存到 `evidence/`。

详细命令、个人测试写法与 E8–E10 场景见 `labs/e8e10/README.md` 和 `docs/E8-E10-overview.md`。

## 4. E8–E10 目标与结果

| 实验 | 目标 |
|---|---|
| E8 | 在 C0 上建立真实基线：实际依赖 vs Makefile 声明，得到 `MISSING` / `REDUNDANT`；输入不变时复用历史图 |
| E9 | C0→C1→C2→C3：函数体变化复用缓存；新增 include 触发刷新并新增 `MISSING`；补齐声明后进入 `resolved` |
| E10 | 六类变化各 5 次，校验增量与全量的 `actual`、`declared`、`findings` 完全一致，并记录耗时中位数 |

四人的 E8–E10 个人材料分别在 `docs/students/<学号>/e8-e10/`；`labs/e8e10/test_profile.py` 共 14 项测试。

## 5. E11–E12 轨道内集成

### 5.1 入口与运行

```bash
python3 run_e11e12.py build
python3 run_e11e12.py prepare
python3 run_e11e12.py run --request <repo 内 request.json> --out work/<mode>-<学号>
python3 run_e11e12.py serve --port 8080
python3 run_e11e12.py test
```

- 三种模式：`e11-a`（BuildChecker 全量图 → 基线缓存 → 增量）、`e11-b`（DRAFT → MDFixer → 固定 MD 报告）、`e12`（`draft → full-check → incremental-check → repair → recheck` 五阶段）。
- 统一 envelope：`schema_version=e11e12-1`，包含 `job_id`、`trace_id`、`kind`、`commit`、`status`、`data` 与 `artifacts[uri,sha256,bytes]`。
- 运行必须在 Linux 云主机；`git config --local user.name` 必须是纯数字学号；镜像名为 `course-e11e12:<学号>`。
- 个人运行结果保存在 `work/<mode>-<学号>/`，证据按学号归档到 `evidence/students/<学号>/e11-e12/`。

### 5.2 四人结果索引

| 学号/姓名 | PR / 合并 | 已完成链路 | 证据 |
|---|---|---|---|
| 241880089 陈玉熙 | PR #25，merge `bfd2ab1` | E11-A、E11-B、E12 固定样例、E12 真实项目、异步 API | `evidence/students/241880089/e11-e12/`（PASS，18 个文件） |
| 241880369 高嘉程 | PR #23，merge `a1c89c6` | E11-A、E12 固定样例、E12 真实项目、异步 API | `evidence/students/241880369/e11-e12/`（PASS，5 个文件） |
| 241880374 马海川 | PR #18，merge `b0765a0f` | E11-A、E12 固定样例、异步 API | 报告/测试已归档；<sub>证据目录未随仓库提交</sub> |
| 241880375 张海洋 | PR #17，merge `b634e12` | E11-A、E11-B、E12 固定样例、E12 真实项目、异步 API、B09 正式签收 | `evidence/students/241880375/e11-e12/`（PASS，22 个文件） |

关键运行记录（完整值见各人报告）：

| 学号 | E11-A job / trace | E12 job / trace | API job / trace |
|---|---|---|---|
| 241880089 | `job-506c114f29664c588fc17c914b39b5ab` / `trace-95ad2ec832be4b07815e703780c8c9ee` | 固定 `job-d33929c866124b9891dfda0719dc68f4`；真实 `job-ebf15bedbe6a4a26b9cc2bf594b1e1ec` | `job-f85899a7364d426e83d9d5133db80e63` / `trace-dfea29f8f40a44e8a6b570de002ced32` |
| 241880369 | `job-efc49baae58c414490f14be0275a413a` / `trace-06722428a2ab41a08b0a3ce5fa13b1f1` | 固定 `job-81be941f47fd4f8fa5a903f5a5455b6c`；真实 `job-268fc09fa76c4f8391867c2da7d950d8` | `job-045cf351d04e4b5fa6c9ffe7f4ae26c3` / `trace-ce6da84edbd7486180aa2ea0a59f1578` |
| 241880374 | `job-326071c6427745e6bfa27f14227aac96` / `trace-b1672860f5874ad1a5924c94a8560444` | 固定 `job-74aa8335bbc740dd994a5846d61e99ef` / `trace-4aedbaa50d8d4958a17de1501c70e9dc` | `job-ffc6088d56ec468086e71b318f141f1f` / `trace-96b4282d18f74dc38fd5b1d7d30efea7` |
| 241880375 | `job-1bd0ed1b449f44f293853df90440844f` / `trace-4e7c0c6afd0447f9869d2f5e1ee6f4ae` | 固定 `job-c8680b5bb961425e9d2bbb1f31054b54`；真实 `job-facd8e04f10f4c47b4ed69dfc9536182` | `job-d58d3a482586434fb03fff8329ce7490` / `trace-9ac031f363af4c30b63e8fdae7c05641` |

### 5.3 B09 对 A09 E12 的签收

B09 已核对 A09 的 E12 交付，A09 侧也已按文件字节复核：

- B09 核对时 A09 `main`：`b0765a0f990b10a28392fe6d4318b4b73a41177a`；PR #17 head：`0cd8054911a18be96900e05c3b7747c6b35a4112`。
- 证据归档 Git blob 在 b0765a0f、PR #17、当前 main `bfd2ab1` 三处均为 `5c52c1824f147019ac25f6706f0549318a1f0cec`；归档 SHA256 `19479d51…`。
- A 端 `job-1bd0ed1b449f44f293853df90440844f` / `trace-4e7c0c6afd0447f9869d2f5e1ee6f4ae`；base `3fcb7202…`，target `15c05995…`。
- B09 直接消费原始 `incremental-check.json`（SHA256 `8508d502…`），未使用 `fixed-md.json`；修复提交 `817b2459…` 父提交为 A 端 target，仅修改 `Makefile`；`candidate.patch` SHA256 `88074f66…`，`validation.json` `accepted=true`。
- 复检 MD=0，仅保留允许的 `REDUNDANT(main.o, unused.h)`；修复项目 bundle SHA256 `e6f7cd98…`。

签收目录：`evidence/students/241880375/e11-e12/b09-signoff/`。完整字段和复核结果见 `docs/reports/A09-E11-E12-audit.md`。

### 5.4 四人实验经过与结果摘要

详细命令、原始日志和失败处理见各自的 `docs/students/<学号>/e11-e12/个人报告.md` 与证据目录；下表只做团体索引，不替代个人记录。

| 成员 | 实际执行过程 | 结果 | 证据状态 |
|---|---|---|---|
| 陈玉熙 241880089 | 云主机依次执行 E11-A → E11-B（首次 `OUTPUT_EXISTS` 保留 `partial-1` 后重跑；DRAFT 600 s 超时后仅在 `data/` 候选 Dockerfile 加清华镜像源）→ E12 固定样例 → E12 真实项目 → API 健康检查/幂等/409/产物三处 SHA/重启语义 | 四条链路与 API 全部 `SUCCEEDED`；E11-B 最终仅保留 `REDUNDANT(main.o, unused.h)`；E12 两套均五阶段成功；重启后未完成任务标记 `SERVER_RESTARTED` | PASS（18 个文件，含原始日志、结果 JSON、证据包） |
| 高嘉程 241880369 | E11-A → E12 固定样例（首次 DRAFT 600 s 超时，切清华源后新 OUT 重跑）→ E12 真实项目 → API；新增边界测试，契约测试 12 → 13 | 各链路 `SUCCEEDED`；固定样例 `job-81be941f…`、真实项目 `job-268fc09f…`、API `job-045cf351…`；产物 SHA 与 `X-Content-SHA256` 一致 | PASS（5 个文件，含 artifact 与 run-summary） |
| 马海川 241880374 | E11-A → E12 固定样例五阶段 → API；首次 E12 在官方 Debian apt 源超时，仅在生成目录 `data/` 加清华源后约 30 秒成功；新增 candidate 边界测试 | E11-A `job-326071c6…`、E12 `job-74aa8335…`、API `job-ffc6088d…` 均成功；最终仅保留 `RD unused.h` | 报告/测试已归档；<sub>证据目录未随仓库提交</sub> |
| 张海洋 241880375 | E11-A → E11-B（iter-01 正常 `MISSING_MAKE`，iter-02 成功；首次 DRAFT 因 Debian 源长时间无进展手工终止）→ E12 固定样例 → E12 真实项目 → API；新增服务重启契约测试；归档 B09 正式签收 | 各链路 `SUCCEEDED`；E11-B 候选输出匹配；E12 固定/真实五阶段成功；API 幂等/409/哈希/重启查询通过；B09 `accepted=true` | PASS（22 个文件，含 Actions artifact、B09 签收与修复 bundle） |

四人共同的已知环境问题：`deb.debian.org` 在云主机上下载极慢（约 19–20 KB/s），会导致 DRAFT 阶段 600 s 超时；处理方式均为仅在生成目录 `data/integration-sample/candidate.Dockerfile` 加清华镜像源，`data/` 不入库，提交的候选模板与检测代码未改。

### 5.5 AI 使用记录（摘要）

| 学号 | 工具 / 日期 | 用途 | 人工验证 |
|---|---|---|---|
| 241880089 | Claude Code，2026-11-17 | 编排建议、独立测试与报告草稿 | 本人复跑 E11-A/B、E12 与 API，核对 job/trace/SHA |
| 241880369 | opencode，2026-11-17 | 边界测试建议、实验与报告草稿 | 本人复跑 E11-A、E12 与 API，核对产物哈希 |
| 241880374 | Codex，2026-11-16 | candidate 越界测试与文档草稿 | 本人完成 E11-A、E12 与 API，数据取自服务器运行 |
| 241880375 | OpenAI Codex，2026-11-10 | 验收项整理、排障建议与文档草稿 | 本人执行全部链路并核对签收字段 |

完整记录见 `docs/students/<学号>/e11-e12/AI_USAGE.md`；AI 输出仅用于建议和草稿，实验数值均来自真实运行。

## 6. 交付物与全量检查

- [x] 四人 E8–E10 个人材料与个人测试（14 项测试）
- [x] 四人 E11–E12 个人报告、ADR、AI_USAGE 与个人测试
- [x] 陈玉熙、高嘉程、张海洋的 E11–E12 证据归档并通过 SHA256 校验
- [x] 马海川 E11–E12 个人报告与测试归档 <sub>（证据目录未随仓库提交）</sub>
- [x] B09 对 A09 E12 签收记录的本地复核
- [x] 归档全量检查：`docs/reports/A09-E11-E12-audit.md` / `.json`
- [x] 本地提交包：由 `scripts/build_submission_package.py` 生成

审计脚本：

```bash
python3 scripts/audit_e11_e12.py
```

当前结果：**21 PASS / 1 WARN / 0 FAIL**。 <sub>WARN：241880374 证据目录未随仓库提交；报告、测试与运行记录已归档。</sub>

## 7. CI 与分支保护

- `e7-a-quality-gate`：E5–E7 BuildChecker 与门禁；
- `e8e10-quality-gate`：E8–E10 单元测试 + A/B 六条路线；
- `e11e12-integration`：E11–E12 契约测试 + E11-A/B/E12 运行 + artifact。

Ruleset `25866762`（`main`，active）已要求 `e7-a-quality-gate` 与 `e8e10-quality-gate`，规则包括禁止删除、禁止非快进推送、必须通过 PR、分支需保持最新。`e11e12-integration` 是否也已加入该 Ruleset 的必需检查，需管理员在 Settings → Rules 中确认；本仓库不把“工作流已存在”等同于“已被分支保护强制”。

P5 配置快照：`ci/A-main-protection.json`；P6 基础设施证据：`evidence/A09-E8-E10/`。

## 8. 文档索引

| 内容 | 位置 |
|---|---|
| E8–E10 目标与概述 | `docs/E8-E10-overview.md` |
| E8–E10 教学实现与测试 | `labs/e8e10/README.md` |
| E11–E12 个人材料 | `docs/students/<学号>/e11-e12/` |
| B09 签收与团队交付审计 | `docs/reports/A09-E11-E12-final-delivery.md` |
| 归档全量检查 | `docs/reports/A09-E11-E12-audit.md` |
| 个人材料模板 | `docs/students/_template/` |
| E7 摘要 | `docs/E7-summary.md` |
| P5 实验报告 | `docs/实验报告.md`、`docs/reports/` |

## 9. 前置阶段（E5–E7）

P5 的 BuildChecker 与 E7 门禁归档在 `services/buildchecker/`、`tests/e7/`、`.github/workflows/e7-quality-gate.yml`；摘要见 `docs/E7-summary.md`。
