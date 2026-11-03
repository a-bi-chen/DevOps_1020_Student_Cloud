# E7 改动与成果摘要

阶段：P5（E5–E7）　小组/轨道：A09 / A（BuildChecker）

最终 P5 main：`abaa94c3c4fb022ff404b503f71fe39e88fdc20c`　代码验证提交：`c81c1937171b1d4587300751195b7a3586988507`

## 1. 改动

| 改动 | 位置 / 证据 |
|---|---|
| 实现 BuildChecker 服务：真实构建采样、修复前后检测、E7 质量门禁 | `services/buildchecker/`、`scripts/run_e7_a_gate.py` |
| 新增项目根边界测试：`../project-other/secret.h` 不得被当作项目内文件 | `services/buildchecker/tests/test_fullcheck.py`；PR #4；`docs/reports/A09-E7-boundary-test.md` |
| 新增故意失败 CI 演示与恢复：失败阻止合并，修复后恢复通过 | PR #3；`docs/reports/A09-E7-failure-recovery.md` |
| 配置 `main` 保护与必需检查 `e7-a-quality-gate` | Ruleset `25866762`；`ci/A-main-protection.json` |
| 汇总验收记录、贡献与最终状态 | PR #5；`docs/reports/A09-acceptance.csv`、`A09-contributions.md`、`A09-final-status.md` |

## 2. 成果

| 检查项 | 结果 |
|---|---|
| 构建与测试 | `17 passed`（原 15 项 + 失败演示 + 边界测试） |
| E7 gate | `8/8 passed`，`gate-result.json` 中 `"passed": true` |
| 独立 oracle | `6 tests OK` |
| secret scan | 源码、镜像两次扫描均未发现问题 |
| 最终镜像 | `course1020-buildchecker:241880369-final` |
| 镜像 digest | `sha256:6e12e90adbe1d3ff47d8f7f38e54186da0e4bf4411348d6db56e3dfe30eb332b` |
| 最终 main CI | run `40503459188`（`abaa94c`），success |

## 3. PR 记录

| PR | 作者 | 内容 | Merge commit |
|---:|---|---|---|
| #1 | 陈玉熙 | Merge fix | `ffef5ba` |
| #2 | 马海川 | E5–E7 证据与基线整合 | `614eeca` |
| #3 | 马海川 | E7 拒绝合并演示 | `fb913a7` |
| #4 | 高嘉程 | E7 项目根边界测试 | `c81c193` |
| #5 | 高嘉程 | E7 验收记录 | `abaa94c` |

## 4. 备注

- 环境自检记录主机内存 3.5 GiB，低于课程脚本 4 GiB 最低值；实验仍全部完成，已在 `docs/实验报告.md` 中披露。
- 详细过程见 `docs/实验报告.md` 与 `docs/reports/`。
