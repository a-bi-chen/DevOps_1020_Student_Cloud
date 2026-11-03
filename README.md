# A09 组 P5–P6 集成仓库（E5–E10）

小组/轨道：A09 / A 轨道（P5 BuildChecker → P6 EChecker）

仓库：https://github.com/a-bi-chen/DevOps_1020_Student_Cloud

本稿基线：`main@0dbf2a1`（PR #8 合并后的 main）；P5 验收基线见第 3 节。

> 本仓库同时承载两个阶段的提交物：
>
> - **P5（E5–E7）**：BuildChecker 服务、E7 质量门禁、CI 与分支保护证据；
> - **P6（E8–E10）**：EChecker 教学实现、六条参考路线、四名成员的个人报告与独立测试。
>
> 原来的 README 只描述 P5 的打包内容，且引用了仓库中不存在的 `source/`、`records/` 目录。本稿按“P5 与 P6 并存”重写，并给出两部分各自可执行的复现入口。

## 1. 小组成员与分工

| 姓名 | 学号 | GitHub | P5（E5–E7） | P6（E8–E10） |
|---|---|---|---|---|
| 张海洋 | 241880375 | `241880375` | E5 原始采集、E6 修复前后检测、E7 本地 8 项门禁 | E8 A 真实基线、E9 A C0–C3、独立测试 `StudentE9A`、PR #9 |
| 陈玉熙 | 241880089 | `a-bi-chen` | 创建仓库、Actions/Ruleset、正常 CI、PR #1 | 仓库/Actions/Ruleset/PR/artifact 管理、独立测试 `StudentE8A089`、PR #7/#8 |
| 马海川 | 241880374 | `weijige7` | E5 基线验证、PR #2 证据整合、PR #3 失败/恢复闭环 | P6 代码导入、E8/E10 个人路线、独立测试 `StudentE8A`、PR #10 |
| 高嘉程 | 241880369 | `Allen-Ga` | 边界测试 PR #4、Review、合并 PR #2–#5、最终记录 | E10 A 扩展测试、独立测试 `StudentE10A`、PR #11 |

## 2. 目录结构与两阶段对应关系

| 路径 | 阶段 | 内容 |
|---|---|---|
| `services/buildchecker/` | P5 | BuildChecker 服务、Dockerfile、单元测试 |
| `tests/e7/` | P5 | E7 独立 oracle 测试 |
| `scripts/` | P5 | `doctor.py`、`lab_cloud.py`、`run_e7_a_gate.py`、`secret_scan.py`、`verify_e6_evidence.py` |
| `ci/` | P5 | `A-main-protection.json` 与 E7 拒绝合并演示 |
| `docs/实验报告.md`、`docs/reports/` | P5 | E5–E7 实验报告、验收/边界/失败恢复/贡献记录 |
| `.github/workflows/e7-quality-gate.yml` | P5 | `e7-a-quality-gate` CI |
| `run_lab.py` | P6 | E8–E10 一键入口（`build` / `e8` / `e9` / `e10`） |
| `labs/e8e10/lab.py` | P6 | EChecker 教学实现（GCC 依赖观测、缓存复用/刷新、Patch） |
| `labs/e8e10/test_profile.py` | P6 | P6 单元测试 11 项（原 7 项 + 四名成员各 1 项） |
| `labs/e8e10/environment/` | P6 | 教学实验镜像（Dockerfile、锁文件、BuildChecker、fixtures） |
| `.github/workflows/e8e10.yml` | P6 | `e8e10-quality-gate` CI（A/B 六条路线） |
| `docs/students/<学号>/e8-e10/` | P6 | 各成员 `个人报告.md`、`ADR.md`、`AI_USAGE.md` |
| `evidence/A09-E8-E10/` | P6 | GitHub 基础设施证据（Ruleset、Actions、截图） |
| `work/` | 共用 | 本地运行产物，已被 `.gitignore` 忽略，按需单独归档 |

## 3. P5（E5–E7）交付摘要

P5 验收时的 main：`abaa94c3c4fb022ff404b503f71fe39e88fdc20c`（PR #5 合并提交）。

| PR | 作者 | 标题 | Merge commit |
|---:|---|---|---|
| #1 | 陈玉熙 | Merge fix | `ffef5ba95357e084485fb8bf209b97843a0b9b90` |
| #2 | 马海川 | chore: consolidate A09 E5-E7 evidence and baseline | `614eecaef6bd6ad8ada43f37ac022828408f1773` |
| #3 | 马海川 | test: demonstrate E7 merge rejection | `fb913a723b56eedbd0f0dcfebc7b290d9dcfb345` |
| #4 | 高嘉程 | test: add E7 project-root boundary test | `c81c1937171b1d4587300751195b7a3586988507` |
| #5 | 高嘉程 | docs: finalize A09 E7 acceptance records | `abaa94c3c4fb022ff404b503f71fe39e88fdc20c` |

P5 验收结果（历史记录，详细路径见 `docs/reports/`）：

- 构建/测试：`17 passed`（原 15 项 + 失败演示 + 边界测试）；
- E7 gate：`8/8 passed`，`gate-result.json` 中 `"passed": true`；
- 独立 oracle：`6 tests OK`；
- 最终镜像：`course1020-buildchecker:241880369-final`，digest `sha256:6e12e90adbe1d3ff47d8f7f38e54186da0e4bf4411348d6db56e3dfe30eb332b`；
- 环境自检记录主机内存 3.5 GiB，低于课程脚本 4 GiB 最低值，已在 `docs/实验报告.md` 中披露。

### P5 复现命令

```bash
# 服务器/容器环境（需要 Docker）
make all                      # doctor + build + test + smoke + scan
python3 -m unittest discover -s tests/e7 -v
python3 scripts/secret_scan.py . --history
```

## 4. P6（E8–E10）交付摘要

### 4.1 代码与 CI 入口

- 教学实现位于仓库根目录 `labs/e8e10/`，入口 `run_lab.py`；不覆盖 P5 的 `services/buildchecker/`。
- `run_lab.py` 读取本仓库 `git config --local user.name` 作为学号，镜像名 `course-e8e10:<学号>`。
- CI `.github/workflows/e8e10.yml` 在 `ubuntu-24.04` 上构建教学镜像，运行单元测试，并执行 A/B 两轨各 E8/E9/E10 共六条路线。

### 4.2 组员个人提交

| 成员 | 个人分支 | PR | 个人文档 | 独立测试 |
|---|---|---|---|---|
| 张海洋 241880375 | `student/241880375/e8-e10` | #9 | `docs/students/241880375/e8-e10/` | `StudentE9A.test_include_inside_header_invalidates` |
| 马海川 241880374 | `student/241880374/e8-e10` | #10 | `docs/students/241880374/e8-e10/` | `StudentE8A.test_declaration_change_reuses_actual_graph` |
| 高嘉程 241880369 | `student/241880369/e8-e10` | #11 | `docs/students/241880369/e8-e10/` | `StudentE10A.test_transitive_include_matches_full_scan` |
| 陈玉熙 241880089 | `student/241880089/e8-e10` | #7、#8（已合并） | `docs/students/241880089/e8-e10/` | `StudentE8A089.test_delete_include_invalidates_and_resolves` |

本稿分支 `draft/e8-e10-group` 已依次合并 241880369/374/375 三个个人分支，并在本稿中补充 241880089 的个人文档与测试；冲突仅出现在 `labs/e8e10/test_profile.py`，按“保留全部测试类”解决。

### 4.3 当前集成状态

- `labs/e8e10/test_profile.py` 共 11 项测试：原 7 项 + 组员 3 项 + 陈玉熙 1 项。
- 本地验证：`Ran 11 tests ... OK`。
- 组员 PR #9/#10/#11 仍为打开状态；本稿经 PR 合并后，应关闭或标记这些个人 PR，避免重复合并。

### 4.4 P6 复现命令

```bash
# 构建教学镜像（镜像名取本仓库 git user.name）
python3 run_lab.py build

# 单条路线；--out 必须是 work/ 下尚不存在的新目录
python3 run_lab.py e8  --track A --out work/e8-A-draft
python3 run_lab.py e9  --track A --out work/e9-A-draft
python3 run_lab.py e10 --track A --out work/e10-A-draft

# Makefile 一键入口（与 P5 共用同一个 Makefile）
make e8e10-build
make e8e10-test        # P6 全部单元测试 → work/e8e10-test-<时间>.log
make e8e10-lab         # A 轨 E8/E9/E10 → work/e8e10-<时间>/{e8,e9,e10}/
```

## 5. CI 与 main 分支保护

- Ruleset：`25866762`（名称 `main`，`enforcement: active`），快照见 `ci/A-main-protection.json` 与 `evidence/A09-E8-E10/241880089-github-infrastructure/`。
- 必需检查（均为 GitHub Actions，`integration_id: 15368`）：
  1. `e7-a-quality-gate`（P5，保留不删）；
  2. `e8e10-quality-gate`（P6，新增）。
- 其他规则：禁止删除、禁止非快进推送、必须通过 PR、分支需保持最新（strict）。
- 管理员同样受约束，因此本稿也必须经 PR 合并，不能直接推送 `main`。

## 6. 文档与证据索引

| 内容 | 位置 |
|---|---|
| P5 实验报告 | `docs/实验报告.md` |
| P5 详细报告/验收/贡献 | `docs/reports/` |
| P6 个人报告与 ADR | `docs/students/<学号>/e8-e10/` |
| P6 GitHub 基础设施证据 | `evidence/A09-E8-E10/241880089-github-infrastructure/` |
| 分支保护配置 | `ci/A-main-protection.json` |
| 课程操作手册 | `docs/00_开始与目录.md` … `docs/06_常见问题.md` |

## 7. 已知边界与未尽事项

- E11–E12 的跨组联调不在本阶段范围内；与课程 B 组的接口交接记录尚未完成，因此本仓库不声称已实现 E12。
- 教学实现只覆盖两个固定对象目标、顶层 C/H、显式规则、简单变量与受限 CFLAGS；E10 的 include/flags/header 场景采用保守刷新，不引用论文的 `85.14×` 作为本组实测。
- P5 的镜像 ID、digest 与运行日志属于 `abaa94c` 验收时的历史记录；当前 `main` 已前进到 `0dbf2a1`，P5 服务代码未在本稿中改动。
- `work/` 为 Git 忽略目录；需要提交的运行产物应按验收要求单独打包归档。
- 本 README 为 P5+P6 合并初稿，组员可在此基础补充本地实验镜像 ID、artifact 链接与 B 组往返记录。
