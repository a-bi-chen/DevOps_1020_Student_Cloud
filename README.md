# A09 组 E8–E10 范本仓库（A 轨 EChecker）

小组 / 轨道：A09 / A（EChecker 教学实现）

仓库：https://github.com/a-bi-chen/DevOps_1020_Student_Cloud

`main` 是本组 P6 的**起点模板**：E8–E10 教学代码、实验镜像、CI 门禁和个人材料模板均已就位，克隆后即可开跑。每名成员必须在自己的 `student/<学号>/e8-e10` 分支上完成实验、报告与个人测试，再通过 PR 提交；`main` 不预置任何人的实验结果。

## 1. 组员与个人分支

| 姓名 | 学号 | GitHub | 个人分支 |
|---|---|---|---|
| 陈玉熙 | 241880089 | `a-bi-chen` | `student/241880089/e8-e10` |
| 高嘉程 | 241880369 | — | `student/241880369/e8-e10` |
| 马海川 | 241880374 | `weijige7` | `student/241880374/e8-e10` |
| 张海洋 | 241880375 | — | `student/241880375/e8-e10` |

个人分支从最新 `main` 创建，分支内的提交、报告与测试只属于本人。

## 2. 仓库结构

| 路径 | 阶段 | 内容 |
|---|---|---|
| `run_lab.py` | P6 | E8–E10 一键入口：`build` / `e8` / `e9` / `e10`，学号取 `git config --local user.name` |
| `labs/e8e10/lab.py` | P6 | EChecker 教学实现（GCC 依赖观测、缓存复用/刷新、Patch） |
| `labs/e8e10/test_profile.py` | P6 | 单元测试：基础 `ProfileTests` 7 项 + 个人测试区（模板） |
| `labs/e8e10/environment/` | P6 | 教学镜像（Dockerfile、锁文件、BuildChecker、fixtures） |
| `labs/e8e10/README.md` | P6 | 教学实现与测试编写说明 |
| `.github/workflows/e8e10.yml` | P6 | `e8e10-quality-gate`：单元测试 + A/B 六条路线 |
| `docs/students/_template/` | P6 | 个人材料模板（个人报告、ADR、AI 使用记录） |
| `docs/E8-E10-overview.md` | P6 | E8–E10 目标、场景与交付物说明 |
| `services/buildchecker/`、`tests/e7/`、`scripts/` | P5 | E5–E7 BuildChecker 与 E7 门禁 |
| `.github/workflows/e7-quality-gate.yml` | P5 | `e7-a-quality-gate`（保留） |
| `docs/E7-summary.md` | P5 | E7 改动与成果摘要（归档） |

## 3. 快速开始（每名成员）

### 3.1 准备分支

本地需要 Python 3.11+ 与 Docker（或课程提供的远端环境）。

```bash
git clone https://github.com/a-bi-chen/DevOps_1020_Student_Cloud.git
cd DevOps_1020_Student_Cloud
git config --local user.name 2418800XX          # 必须是纯数字学号
git config --local user.email <你的 GitHub 邮箱>
git switch -c student/2418800XX/e8-e10 origin/main
```

`run_lab.py` 用 `git config --local user.name` 作为学号，镜像名固定为 `course-e8e10:<学号>`。

### 3.2 跑通 E8 / E9 / E10

```bash
python3 run_lab.py build
python3 run_lab.py e8  --track A --out work/e8-A-run1
python3 run_lab.py e9  --track A --out work/e9-A-run1
python3 run_lab.py e10 --track A --out work/e10-A-run1
```

- `--out` 必须是 `work/` 下**尚不存在**的新目录，每个阶段单独使用。
- 保留每个阶段的命令、日志、JSON、OUT、被测源码 SHA 与镜像 ID；`work/` 被 `.gitignore` 忽略，需要提交的结果另行归档或 `git add -f`。
- 也可以用 Makefile：`make e8e10-build`、`make e8e10-test`、`make e8e10-lab`。

### 3.3 写个人材料

```bash
mkdir -p "docs/students/<学号>/e8-e10"
cp docs/students/_template/*.md "docs/students/<学号>/e8-e10/"
```

在该目录填写：

- `个人报告.md`：环境与镜像 ID、E8/E9/E10 的命令与预期/实际、个人贡献、Actions/PR/artifact。
- `ADR.md`：缓存何时失效、身份绑定、共享变量与失败保护等决策及代价。
- `AI_USAGE.md`：模型建议、采纳/拒绝理由、人工修改与实际验证；未调用模型时也要写明。

### 3.4 加一个个人测试（或一项实现改动）

在 `labs/e8e10/test_profile.py` 底部的“个人测试区”新增**独立测试类**：

```python
class StudentE8A2418800XX(unittest.TestCase):
    def test_<场景>_<预期>(self):
        ...
```

要求：

- 至少覆盖一个新的变化方向（如删除已有 include、头文件内再包含、声明变化、flags 变化等），必须有独立预期；
- 不修改上方 `ProfileTests` 的既有断言，不复制他人用例；
- 本地先跑通：

```bash
cd labs/e8e10
python3 -m unittest discover -s . -p test_profile.py -v
```

若选择实现改动而不是加测试，需在个人报告中说明改动位置、动机、验证命令与结果。

### 3.5 提交 PR 并保留证据

```bash
git add labs/e8e10/test_profile.py labs/e8e10/lab.py "docs/students/<学号>/e8-e10"
git commit -m "E8-E10: <学号> 实验、报告与个人测试"
git push -u origin "student/<学号>/e8-e10"
```

在 GitHub 上向 `main` 发起 PR，等待 `e7-a-quality-gate` 与 `e8e10-quality-gate` 均通过，下载 artifact（`e8e10-evidence-<run_id>`），并把 PR 链接、headSha、Actions 链接、artifact 名称写入个人报告。

## 4. E8–E10 目标

| 实验 | 目标 |
|---|---|
| E8 | 在参考样例 C0 上建立真实基线：真实观测实际依赖并与 Makefile 声明比较，得到 `MISSING` / `REDUNDANT`；输入未变化时复用历史图 |
| E9 | 跑通 C0→C1→C2→C3：函数体变化复用缓存；新增 include 触发刷新并新增 `MISSING`；补齐声明后相应 `MISSING` 进入 `resolved` |
| E10 | 六类变化（unchanged / body / include / declaration / flags / header）各 5 次，校验增量与全量的 `actual`、`declared`、`findings` 完全一致，并记录逐场景耗时中位数 |

详细场景、命令与产出见 `docs/E8-E10-overview.md`。

## 5. 交付物与验收

- [ ] 个人分支 `student/<学号>/e8-e10`
- [ ] E8 / E9 / E10 完整运行结果（命令、日志、JSON、OUT、源码 SHA、镜像 ID）
- [ ] `docs/students/<学号>/e8-e10/个人报告.md`、`ADR.md`、`AI_USAGE.md`
- [ ] 一个有独立预期的个人测试，或一项实现改动
- [ ] 通过两项必需检查的 PR，以及对应 Actions 链接与 artifact

## 6. CI 与分支保护

- Ruleset `25866762`（`main`，active）要求两项必需检查：`e7-a-quality-gate` 与 `e8e10-quality-gate`，均来自 GitHub Actions（`integration_id: 15368`）。
- 规则包括：禁止删除、禁止非快进推送、必须通过 PR、分支需保持最新（strict）。
- P5 配置快照：`ci/A-main-protection.json`；P6 基础设施证据：`evidence/A09-E8-E10/`。

## 7. 前置阶段（E5–E7）

P5 的 BuildChecker 与 E7 门禁已归档在 `services/buildchecker/`、`tests/e7/`、`.github/workflows/e7-quality-gate.yml`。摘要见 `docs/E7-summary.md`；本仓库当前以 E8–E10 为主。

## 8. 文档索引

| 内容 | 位置 |
|---|---|
| E8–E10 目标与概述 | `docs/E8-E10-overview.md` |
| 教学实现与测试说明 | `labs/e8e10/README.md` |
| 个人材料模板 | `docs/students/_template/` |
| E7 摘要 | `docs/E7-summary.md` |
| P5 实验报告 | `docs/实验报告.md`、`docs/reports/` |
