# E13 B09 交叉检测报告（A09 BuildChecker / EChecker）

- 生成时间：2026-11-24T05:54:46+00:00
- 结论：**SUCCEEDED**
- 请求方：B09，仓库 <https://github.com/llxxy-cn/devops-b09>
- 项目子目录：`fixtures/e11e12-b1-real`
- Base（原始提交，未改写）：`30ffe4c41492334478a2446a8be0662d3f31d478`
- Target（原始提交，未改写）：`a7e3b644ca9b1b9d0b26bd41e839fcbf5ea1c293`
- B09 仓库当前 HEAD：`80b4dafb836365911e6e85451ee367cc874afa46`

## 1. 检测入口兼容性

| 入口 | 结果 | 证据 |
|---|---|---|
| 官方 pipeline，repo 指向子目录 | 退出码 `1`：`COMMAND_FAILED: git failed; see base-project-clone.log` | `official-entry-subdir.log` |
| 官方 pipeline，repo 指向仓库根 | 退出码 `1`：`UNSUPPORTED_PROJECT: Expected main.c/helper.c/config.h and explicit Make rules` | `official-entry-root.log` |
| 官方 EChecker scan，直接扫子目录 | `REJECTED`：ValueError: UNSUPPORTED_FLAGS | `entry-probes.json` |

官方入口不能直接以该子目录运行：E11-E12 `snapshot()` 以仓库根为项目根，EChecker `scan()` 的 flags 白名单也不含 B09 的 `-std=c11 -Wall -Wextra -Werror`。本报告使用 `GCC_LOCAL_HEADERS_EXPLICIT_MAKE_E13_B09` 适配配置：保留 BuildChecker `full_check` 原实现，按同一 EChecker 算法（Makefile 声明 vs `gcc -MM` 实际依赖、保守缓存失效、added/resolved）执行增量检测。

## 2. 原始项目命令与输出

| 项目 | make clean && make | make test | ./app | 输出 | 期望输出匹配 |
|---|---|---|---|---|---|
| Base | PASS | PASS | PASS | `hello E3` | True |
| Target | PASS | PASS | PASS | `hello E3` | True |

## 3. BuildChecker 全量检测

| 项目 | 状态 | 依赖缺陷（main.o/helper.o） |
|---|---|---|
| Base | `SUCCEEDED` | `[]` |
| Target | `SUCCEEDED` | `[('MISSING', 'main.o', 'extra.h')]` |

## 4. EChecker 增量检测

- 基线缓存：`baseline-cache.json`；目标增量：`incremental-check.json`
- 增量 findings：`[('MISSING', 'main.o', 'extra.h')]`
- 新增：`[['MISSING', 'main.o', 'extra.h']]`；解决：`[]`
- 刷新目标：`['main.o', 'helper.o']`；复用目标：`[]`
- 与目标全量结果一致：**True**

## 5. 预期核对

| 检查项 | 结果 |
|---|---|
| `base_no_findings` | True |
| `target_expected_findings` | True |
| `incremental_matches_target_full` | True |
| `incremental_only_expected_addition` | True |
| `base_commands_ok` | True |
| `target_commands_ok` | True |
| `commits_unchanged` | True |

## 6. 交付说明

- 两个原始提交号均已通过 `git checkout --detach <sha>` 与 `git rev-parse HEAD` 双重核对；未对 B09 仓库做任何提交或改写。
- BuildChecker 的全量报告、实际依赖图、声明依赖图、make 数据库和原始 trace 保存在 `baseline-full/`、`target-full/`。
- 命令日志保存在 `commands-base/`、`commands-target/`；入口兼容性原始日志保存在 `official-entry-*.log`。
- 文件校验见 `SHA256SUMS`。
