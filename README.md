# A09 BuildChecker：论文方法复现、MVP 与验证

本仓库是 DevOps 课程 A09 小队的 BuildChecker（TSE 论文）交付仓库，覆盖 E5–E7。

## 团队成员

| 姓名 | 学号 | GitHub/身份 | 主要职责 |
|---|---|---|---|
| 马海川 | 241880374 | `weijige7` | 团队证据整合、剩余测试与故障闭环、最终报告与验收 |
| 张海洋 | 241880375 | GitHub 账号待确认 | E5–E7 基线运行、依赖检测、修复复检和本地门禁 |
| 陈玉熙 | 241880089 | `a-bi-chen`，仓库创建者 | GitHub 仓库、Actions、Ruleset 和正常 CI 闭环 |
| 高嘉程 | 241880369 | 待本人补充 | 由本人完成其中一项独立贡献和 Review |

## 当前状态

| 阶段 | 状态 | 主要证据 |
|---|---|---|
| E5：原始复现 | PASS | `evidence/A09-E5-E7/241880375-work/e5-01/` |
| E6：自动检测与修复复检 | PASS | `evidence/A09-E5-E7/241880375-work/e6-before/`、`e6-after/` |
| E7：本地完整门禁 | PASS，8/8 场景 | `evidence/A09-E5-E7/241880375-work/e7-01/gate/` |
| E7：GitHub Actions 正常路径 | PASS | `evidence/CI-A/run-40298566040/` |
| 自主扩展测试 | PENDING | 将新增至少 1 项边界测试 |
| E7：失败 PR 与恢复合并 | PENDING | 将保存 BLOCKED、拒绝合并、CLEAN 和 MERGED 记录 |

当前结论：核心检测功能、修复复检、故障门禁和正常 CI 已经跑通；最终验收仍需要新增测试以及失败 PR 闭环。

## 唯一代码入口

本仓库以根目录为唯一实现：

```text
services/buildchecker/   BuildChecker 核心实现和测试
fixtures/md-rd/          固定 MD/RD 实验项目
scripts/                 doctor、实验入口、门禁和证据校验
tests/e7/                独立判定测试
evidence/                已归档原始证据和 CI artifact
docs/                    接口、操作和验收文档
```

不再维护 `labs/A-buildchecker` 或 `labs/B-draft` 副本。A09 只负责 A 轨道；B09 的 DRAFT 与 MDFixer 由 B09 仓库维护，A/B 技术联调从 E12 开始。

## 快速验证

在 Ubuntu 云服务器或具有 Docker 的 Linux 环境中，从仓库根目录执行：

```bash
python3 scripts/lab_cloud.py doctor

python3 scripts/lab_cloud.py build \
  --image course1020-buildchecker:local \
  --out work/build-01 \
  --build-timeout 1200

python3 scripts/lab_cloud.py e5 \
  --image course1020-buildchecker:local \
  --out work/e5-01

python3 scripts/lab_cloud.py e6 \
  --image course1020-buildchecker:local \
  --out work/e6-before

python3 scripts/lab_cloud.py e6 --fixed \
  --image course1020-buildchecker:local \
  --out work/e6-after

python3 scripts/verify_e6_evidence.py \
  --before work/e6-before/evidence/findings.json \
  --after work/e6-after/evidence/findings.json

python3 -m unittest discover -s tests/e7 -v

python3 scripts/lab_cloud.py gate \
  --image course1020-buildchecker:local \
  --out work/e7-01
```

E5/E6 预期错误集合：

```text
MISSING   main.o -> config.h
REDUNDANT main.o -> unused.h
```

E6 修复后预期 `findings=[]`，且输入哈希只改变 `Makefile`。

## 证据

详细索引见：

- `evidence/README.md`
- `docs/reports/A09-E5-E7-report.md`
- `docs/reports/A09-acceptance.csv`

自动证据由 `work/` 生成；已冻结的重要证据归档在 `evidence/`。大日志和 artifact 不会通过服务接口直接传递。

成员证据映射：

| 成员 | 证据目录 |
|---|---|
| 张海洋（241880375） | `evidence/A09-E5-E7/241880375-work/` |
| 陈玉熙（241880089） | `evidence/CI-A/run-40298566040/` 及 GitHub PR/Ruleset |
| 马海川（241880374） | 后续整合 PR、测试和故障恢复证据 |
| 高嘉程（241880369） | 最终由本人提交的 PR 或 Review |

## 安全要求

- 不提交 `.env`、Token、SSH 私钥或服务器密码。
- LLM Key 只能通过环境变量或密钥管理注入。
- 提交前运行：

```bash
python3 scripts/secret_scan.py . --history
```

## 参考边界

本仓库实现的是课程教学 profile：单 Make 进程、单最终输出、项目目录内路径。它验证 BuildChecker 的核心方法与证据链，不等同于论文全部 30 个开源项目的性能和误报实验。
