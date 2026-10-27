# A09 组 E5–E7 最终提交物

小组/轨道：A09 / A 轨道 BuildChecker

提交日期：2026-10-27

仓库：https://github.com/a-bi-chen/DevOps_1020_Student_Cloud

最终 main：`abaa94c3c4fb022ff404b503f71fe39e88fdc20c`

代码验证提交（PR #4 合并后）：`c81c1937171b1d4587300751195b7a3586988507`

## 1. 小组成员与分工

| 姓名 | 学号 | GitHub/身份 | 分工 |
|---|---|---|---|
| 张海洋 | 241880375 | `241880375` | E5 原始采集、E6 修复前后检测、E7 本地 8 项门禁；初始化提交与冲突解决提交经 PR #1 合并 |
| 陈玉熙 | 241880089 | `a-bi-chen` | 创建仓库、配置 Actions/Ruleset、正常 CI、PR #1；2026-10-27 修正 Ruleset 检查名 |
| 马海川 | 241880374 | `weijige7` | E5 基线验证、PR #2 证据整合、PR #3 失败/恢复闭环、交接文档 |
| 高嘉程 | 241880369 | `Allen-Ga` | 边界测试 PR #4、Review PR #2、合并 PR #2/#3/#4/#5、最终记录 PR #5 |

## 2. 目录说明

| 路径 | 内容 |
|---|---|
| `docs/实验报告.md` | 按 `templates/实验报告.md` 填写的 A09 组 E5–E7 实验报告 |
| `docs/reports/` | A09 详细报告、逐人贡献、验收记录、边界测试、失败恢复、最终状态 |
| `templates/验收记录.csv` | 按官方模板填写的全组验收记录 |
| `templates/实验报告.md` | 官方报告模板（参考） |
| `work/` | 完整运行结果：E5/E6/E7、boundary、final、CI 拒绝/恢复、final-records/artifacts |
| `source/` | 最终 main 的 `git archive` 源码快照（不含 `.git`、`work/`） |
| `evidence/` | 从最终 main 源码快照中提取的证据副本，供验收表直接引用 |
| `records/` | 全组提交历史、贡献者、PR #1–#5、CI 运行、Ruleset、MERGED、拒绝合并日志 |

## 3. 全组 PR 记录

| PR | 作者 | 标题 | 状态 | Merge commit |
|---:|---|---|---|---|
| #1 | 陈玉熙 | Merge fix | MERGED | `ffef5ba95357e084485fb8bf209b97843a0b9b90` |
| #2 | 马海川 | chore: consolidate A09 E5-E7 evidence and baseline | MERGED | `614eecaef6bd6ad8ada43f37ac022828408f1773` |
| #3 | 马海川 | test: demonstrate E7 merge rejection | MERGED | `fb913a723b56eedbd0f0dcfebc7b290d9dcfb345` |
| #4 | 高嘉程 | test: add E7 project-root boundary test | MERGED | `c81c1937171b1d4587300751195b7a3586988507` |
| #5 | 高嘉程 | docs: finalize A09 E7 acceptance records | MERGED | `abaa94c3c4fb022ff404b503f71fe39e88fdc20c` |

PR #1 的发起者是陈玉熙；张海洋的 `9165f37`、`e12237` 是通过该 PR 合并的代码贡献，详细映射见 `records/group/pr1-contributions.json`。

## 4. 最终验证

- 构建：`17 passed`（原 15 项 + PR #3 演示测试 + PR #4 边界测试）
- E7 gate：`8/8 passed`，`gate-result.json` 中 `"passed": true`
- 独立 oracle：`6 tests OK`
- secret scan：source 和 image 两次扫描均未发现问题（见 `work/secret-scan*.txt`）
- 最终镜像：`course1020-buildchecker:241880369-final`
- 镜像 digest：`sha256:6e12e90adbe1d3ff47d8f7f38e54186da0e4bf4411348d6db56e3dfe30eb332b`
- 最终 main CI：run `40503459188`，提交 `abaa94c`，结果 success

## 5. 提交完整性说明

- E5–E7 的技术结果、E7 门禁、CI 正常/失败/恢复闭环和最终合并记录均已归档。
- 环境自检记录显示主机内存为 3.5 GiB，低于课程脚本的 4 GiB 最低值；Docker 和全部实验仍成功完成。该限制已在实验报告中明确披露，不再写成 `problems=[]`。
- 课程原文中的个人最低门槛属于建议性评分要求。当前高嘉程和马海川已有 GitHub 正式 Review 记录；张海洋、陈玉熙的 Review 项保留为 PENDING，不伪造记录。张海洋通过 PR #1 合并的提交已作为被合并贡献记录。
- `source/` 是 `abaa94c` 的原样快照；包内顶层 `README.md` 和报告反映本次重新核验后的提交状态。

## 6. 官方验收清单对应

| 官方要求 | 本包位置 |
|---|---|
| 学号、小组、轨道、环境 | `docs/实验报告.md` 顶部 |
| 仓库、提交 SHA、镜像 ID、依赖锁文件 | `docs/实验报告.md` 顶部；`source/` 中 `requirements-dev.lock` |
| E5 复现说明和原始日志 | `docs/实验报告.md`；`work/e5-01/`；`evidence/A09-E5-E7/241880375-work/e5-01/` |
| E6 输入副本、哈希、JSON 报告、运行日志 | `work/e6-before/`、`work/e6-after/`；`evidence/A09-E5-E7/241880375-work/e6-*` |
| E7 单元测试日志、gate-result.json、results.csv | `work/build-final/unit-tests/`；`work/e7-final/gate/` |
| 自己补充的一项测试、修改说明、运行结果 | `docs/reports/A09-E7-boundary-test.md`；`services/buildchecker/tests/test_fullcheck.py` |
| CI 正常、失败、恢复运行链接及 artifact | `docs/实验报告.md`；`work/final-records/artifacts/` |
| main 分支保护、合并拒绝日志、最终合并记录 | `records/ci/A-main-protection.json`；`records/ruleset-main.json`；`work/ci-rejection/merge-rejection.log`；`work/ci-boundary/merge-rejection.log`；`records/pr*-merged.json` |
| 实验报告与结果备份 | 本压缩包；`source/`；`work/` |

## 7. 复现命令

```bash
git clone https://github.com/a-bi-chen/DevOps_1020_Student_Cloud.git
cd DevOps_1020_Student_Cloud
python3 scripts/lab_cloud.py build --image course1020-buildchecker:241880369-final --out work/build-final --build-timeout 1200
python3 scripts/lab_cloud.py gate --image course1020-buildchecker:241880369-final --out work/e7-final
python3 -m unittest discover -s tests/e7 -v
python3 scripts/secret_scan.py . --history
```

## 8. 排除项

本包不包含 `.env`、Token、SSH 私钥或 GitHub 登录文件。`work/` 是服务器运行结果，`source/` 是 Git 跟踪文件的快照。
