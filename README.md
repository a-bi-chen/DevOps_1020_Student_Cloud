# A09 组 E8–E14 统一仓库（A 轨 EChecker）

小组 / 轨道：A09 / A（BuildChecker → EChecker 教学实现）

仓库：<https://github.com/a-bi-chen/DevOps_1020_Student_Cloud>

`main` 是本组 E8–E14 的统一验收版本：E8–E10 教学代码与四人个人测试（14 项）、E11–E12 轨道内集成、E13–E14 交叉测试与候选发布，以及各阶段四人个人材料均已归档。E11–E12 与 E13–E14 的个人报告见 `docs/students/<学号>/e11-e12/`、`docs/students/<学号>/e13-e14/`；团队级结果、B09 签收与候选发布记录见 `docs/reports/` 和 `docs/students/241880375/e13-e14/`。

## 1. 组员与分支

| 姓名 | 学号 | GitHub | E8–E10 分支 | E11–E12 分支 | E13–E14 分支 |
|---|---|---|---|---|---|
| 陈玉熙 | 241880089 | `a-bi-chen` | `student/241880089/e8-e10` | `student/241880089/e11-e12` | `student/241880089/e13-e14` |
| 高嘉程 | 241880369 | `Allen-Ga` | `student/241880369/e8-e10` | `student/241880369/e11-e12` | `student/241880369/e13-e14` |
| 马海川 | 241880374 | `weijige7` | `student/241880374/e8-e10` | `student/241880374/e11-e12` | `student/241880374/e13-e14` |
| 张海洋 | 241880375 | `241880375` | `student/241880375/e8-e10` | `student/241880375/e11-e12` | `student/241880375/e13-e14` |

E8–E10 个人测试类：`StudentE8A089`、`StudentE9A089`、`StudentE10A089`、`StudentE9A089RemovedInclude`、`StudentE10A`、`StudentE8A`、`StudentE9A`，合计 7 项个人测试 + 7 项基础 `ProfileTests` = **14 项**。

E11–E12 个人测试类：`StudentE11E12A241880089`、`StudentE11E12A241880369`、`StudentE11E12A241880374`、`StudentE11E12A241880375`。

E13–E14 个人测试：`labs/e13e14/tests/test_student_241880089.py`、`test_student_241880369.py`、`test_student_241880374.py`；`test_handoff.py` 为共用交接校验，`labs/e8e10/test_profile.py` 另含 `StudentE13A241880375`。

## 2. 仓库结构

| 路径 | 阶段 | 内容 |
|---|---|---|
| `run_lab.py` | P6 | E8–E10 一键入口：`build` / `e8` / `e9` / `e10` |
| `labs/e8e10/lab.py` | P6 | EChecker 教学实现（GCC 依赖观测、缓存复用/刷新、Patch） |
| `labs/e8e10/test_profile.py` | P6 | 基础 `ProfileTests` 7 项 + 四人 E8–E10 个人测试 7 项 |
| `run_e11e12.py` | E11–E12 | `build` / `prepare` / `run` / `serve` / `test` 入口 |
| `labs/e11e12/` | E11–E12 | 编排、DRAFT/MDFixer、异步任务 API、契约测试与个人测试 |
| `labs/e13/` | E13 | 交叉检测适配入口 `run_crosscheck.py`（B09 子目录 + `CFLAGS` profile） |
| `labs/e13e14/` | E13–E14 | 交接校验、四角色 Compose 编排与个人独立测试 |
| `services/buildchecker/`、`tests/e7/`、`scripts/` | P5 / E11–E14 | BuildChecker、E7 门禁、运行日志/历史密钥扫描与归档脚本 |
| `.github/workflows/e7-quality-gate.yml` | P5 | `e7-a-quality-gate` |
| `.github/workflows/e8e10.yml` | P6 | `e8e10-quality-gate`：单元测试 + A/B 六条路线 |
| `.github/workflows/e11e12.yml` | E11–E12 | `e11e12-integration`：契约测试 + E11-A/B/E12 运行 + artifact |
| `.github/workflows/e13e14.yml` | E13–E14 | `contracts` + `four-services`：契约测试、Compose 配置校验、四服务运行 |
| `docs/students/` | P6–E14 | 四人各阶段个人材料与模板 |
| `docs/reports/` | E11–E12 | 团队交付审计、B09 签收核对与全量检查 |
| `evidence/students/` | E11–E14 | 按学号归档的原始日志、JSON、trace、证据包与 SHA256 清单 |

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
| 241880374 马海川 | PR #18，merge `b0765a0f` | E11-A、E12 固定样例、异步 API | `evidence/students/241880374/e11-e12/`（PASS，3 个文件） |
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
| 马海川 241880374 | E11-A、E12 固定样例、API | 均成功；最终仅保留 RD unused.h | PASS（3 个文件，含完整证据包与 SHA256SUMS） |
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

## 6. E13–E14（P8）：交叉测试与候选发布

### 6.1 组级结果

| 范围 | 结论 | 主要证据 |
|---|---|---|
| C1 A 侧检测 B09 真实项目 | Base `30ffe4c4…` 无缺陷；Target `a7e3b644…` 精确新增 `MISSING(main.o, extra.h)`；增量 `added` 与 Target 全量一致 | `work/e13-c1-b09-01`、`docs/students/241880375/e13-e14/交叉测试记录.md` |
| C1 B09 消费 A09 报告 | B09 构建、修复、复检 `SUCCEEDED`；MD=0，仅保留 `REDUNDANT(main.o, unused.h)`；6/6 修复边 `rebuilt=true`、`output_matches=true` | B09 回传包与 `evidence/students/241880375/e13-e14/b09-signoff-verify-20261124/` |
| C2–C8 | 旧报告 `STALE_REPORT`、篡改 `ARTIFACT_HASH_MISMATCH`、受控超时无残留、错误补丁回滚、假 Key 阻断、失败隔离、幂等 202/409 全部符合预期 | `work/e13-c2*` … `work/e13-c8`、组级交叉测试记录 |
| H1–H3 | jsmn、inih、tiny-AES-c 三个未知项目均完成 `draft → full-check → incremental-check → repair → recheck` 五阶段，补丁 `accepted=true` | `work/e13-H1*` … `work/e13-H3*` |
| E14 四容器 | buildchecker / echecker / draft / mdfixer 四角色 `healthy`（仅绑定 `127.0.0.1:18081–18084`）；固定样例五阶段成功、受控超时返回 `TIMEOUT`、恢复重跑成功 | `evidence/students/241880375/e13-e14/ci-e14-result.json` 与个人 E14 证据 |
| `v0.9-rc` | 已发布并保持指向 `ee6f7da9568686c9f99ee937a223c7f77a5eb9e6`，后续文档/个人材料提交未移动标签 | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/releases/tag/v0.9-rc> |
| B09 签收复核（2026-11-24） | 四分片重组包 154,556,278 字节、SHA256 `1a1419b6…ba33`；包内 CRLF 清单规范化后 17/17 通过；修复 bundle 校验通过；Secret 全量扫描 1109 个文件 0 命中 | `evidence/students/241880375/e13-e14/b09-signoff-verify-20261124/` |

### 6.2 四名组员贡献

| 成员 | 分支 / PR | 实际完成 | 结果与证据 |
|---|---|---|---|
| 陈玉熙 241880089 | `student/241880089/e13-e14`，PR #35 | E13 C1 A 侧独立执行与 2026-11-24 复跑（B09 `fixtures/e11e12-b1-real`，Base→Target）；新增 `labs/e13/run_crosscheck.py` 适配入口与 `test_student_241880089.py`（3 项）；保留官方入口三种失败的原始日志 | `SUCCEEDED`，`MISSING(main.o, extra.h)`；证据包内 94/94 `SHA256SUMS` 通过；`evidence/students/241880089/e13-e14/` |
| 高嘉程 241880369 | `student/241880369/e13-e14`，PR #34 | 个人独立复跑 C1–C8、H1–H3 与 E14 四容器/受控超时/恢复；新增 `test_student_241880369.py`（2 项：错误补丁回滚、假 Key 扫描）；运行日志与工作区历史扫描 | C1 `job-52db0f4c…`；C2/C3 正确拒绝；H1–H3 五阶段；E14 固定样例 `job-b611b79b…`、超时 `job-f02d3c46…`、恢复 `job-5b053266…`；`evidence/students/241880369/e13-e14/` |
| 马海川 241880374 | `student/241880374/e13-e14`，PR #30 | C1、H1–H3、E14 四容器/受控超时/恢复；新增 `test_student_241880374.py`；归档完整证据包与 SHA256 清单 | H1–H3 均五阶段，H2 修复后如实保留 `REDUNDANT(main.o, unused.h)`；E14 固定样例 `job-622eff0f…`（162 产物）、超时 `job-e229f9b8…`、恢复 `job-a18d7deb…`；证据包 SHA256 `cfe14db2…f761` |
| 张海洋 241880375 | `student/241880375/e13-e14`，PR #20（入口/组级）、#29（证据归档）、#31（门禁签收）、#32（标签同步）、#33（签收复核） | 实现 E13/E14 入口、交接适配、运行日志 Secret 扫描、四角色 Compose/编排/CI；补充 `fixed_report_sha256` 传输校验与 `project_subdir`；修复 Issue #19/#21；完成 C1–C8、H1–H3、E14 与 B09 双向交换、签收复核 | `v0.9-rc` 指向 `ee6f7da9`；B09 `accepted=true`；`docs/students/241880375/e13-e14/`、`evidence/students/241880375/e13-e14/` |

组级材料由张海洋汇总（PR #20），四位组员均在各自分支保留独立运行证据；个人报告不重复声明他人执行的链路，组级结论以 `docs/students/241880375/e13-e14/交叉测试记录.md` 与 `候选发布说明.md` 为准。

### 6.3 E13–E14 文档与证据

| 内容 | 位置 |
|---|---|
| 组级交叉测试、候选发布、Issue/修复记录 | `docs/students/241880375/e13-e14/` |
| 四人个人报告、ADR、AI 使用与证据索引 | `docs/students/<学号>/e13-e14/` |
| 按学号归档的原始证据 | `evidence/students/<学号>/e13-e14/` |
| B09 签收复核证据（2026-11-24） | `evidence/students/241880375/e13-e14/b09-signoff-verify-20261124/` |
| E13 适配入口说明 | `labs/e13/README.md` |

## 7. 交付物与全量检查

- [x] 四人 E8–E10 个人材料与个人测试（14 项测试）
- [x] 四人 E11–E12 个人报告、ADR、AI_USAGE 与个人测试
- [x] 陈玉熙、高嘉程、张海洋的 E11–E12 证据归档并通过 SHA256 校验
- [x] 马海川 E11–E12 个人报告、个人测试与证据归档（3 个文件，PASS）
- [x] B09 对 A09 E12 签收记录的本地复核
- [x] E13 C1–C8 与 H1–H3 组级运行，B09 对 A09 E13 C1 独立消费并签收
- [x] E14 四容器固定样例、受控超时与恢复，`v0.9-rc` 发布且标签未移动
- [x] 四人 E13–E14 个人报告、ADR、AI_USAGE、个人测试与证据归档
- [x] 2026-11-24 B09 签收回执独立复核（`evidence/students/241880375/e13-e14/b09-signoff-verify-20261124/`）
- [x] 归档全量检查：`docs/reports/A09-E11-E12-audit.md` / `.json`
- [x] 本地提交包：由 `scripts/build_submission_package.py` 生成

审计脚本：

```bash
python3 scripts/audit_e11_e12.py
```

当前结果：以 `python3 scripts/audit_e11_e12.py` 重新生成的结果为准；四人个人材料、个人测试与证据目录均已归档。

> 提交包说明：`A09-E13-E14-final-20261124-v3.zip` 生成于 2026-11-24 14:09，早于 PR #34（241880369）与 PR #35（241880089）的 E13–E14 个人材料合入；需要提交时应在 `main` 最新提交上重新运行打包脚本，使四人 E13–E14 材料全部进入提交包。

## 8. CI 与分支保护

- `e7-a-quality-gate`：E5–E7 BuildChecker 与门禁；
- `e8e10-quality-gate`：E8–E10 单元测试 + A/B 六条路线；
- `e11e12-integration`：E11–E12 契约测试 + E11-A/B/E12 运行 + artifact；
- `contracts` / `four-services`（E13–E14 工作流）：契约与交接测试、Compose 配置校验、Secret 扫描、四服务固定样例运行。

Ruleset `25866762`（`main`，active）已要求 `e7-a-quality-gate` 与 `e8e10-quality-gate`，规则包括禁止删除、禁止非快进推送、必须通过 PR、分支需保持最新。`e11e12-integration` 与 E13–E14 检查是否也已加入该 Ruleset 的必需检查，需管理员在 Settings → Rules 中确认；本仓库不把“工作流已存在”等同于“已被分支保护强制”。

P5 配置快照：`ci/A-main-protection.json`；P6 基础设施证据：`evidence/A09-E8-E10/`。

## 9. 文档索引

| 内容 | 位置 |
|---|---|
| E8–E10 目标与概述 | `docs/E8-E10-overview.md` |
| E8–E10 教学实现与测试 | `labs/e8e10/README.md` |
| E11–E12 个人材料 | `docs/students/<学号>/e11-e12/` |
| E13–E14 个人材料 | `docs/students/<学号>/e13-e14/` |
| E13–E14 组级记录（交叉测试/候选发布） | `docs/students/241880375/e13-e14/` |
| E13 适配入口 | `labs/e13/README.md` |
| B09 签收与团队交付审计 | `docs/reports/A09-E11-E12-final-delivery.md` |
| 归档全量检查 | `docs/reports/A09-E11-E12-audit.md` |
| 个人材料模板 | `docs/students/_template/` |
| E7 摘要 | `docs/E7-summary.md` |
| P5 实验报告 | `docs/实验报告.md`、`docs/reports/` |

## 10. 前置阶段（E5–E7）

P5 的 BuildChecker 与 E7 门禁归档在 `services/buildchecker/`、`tests/e7/`、`.github/workflows/e7-quality-gate.yml`；摘要见 `docs/E7-summary.md`。
