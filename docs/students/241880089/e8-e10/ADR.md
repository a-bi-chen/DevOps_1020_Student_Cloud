# 决策记录

背景与约束：

- A 轨 E8 要求用真实 BuildChecker（strace + Make 数据库）建立对象依赖基线，并与 Makefile 声明比较；不能只用 GCC `-MM` 投影冒充真实基线。
- A 轨 E9/E10 还要求连续提交下的增量更新、六场景一致性，以及同一提交的独立复验；单次 CI 结果不足以排除偶发差异。
- 本机为 Windows，未安装 Docker/ WSL，且课程 SSH 服务器当前不可达；教学镜像与 `strace -ff` 只能在 Linux 上运行。
- 个人提交必须落在 `student/241880089/e8-e10`，不能直接改 `main`。

选择与替代方案：

- **选择**：在个人分支推送提交，触发 `.github/workflows/e8e10.yml`，在 `ubuntu-24.04` 上构建 `course-e8e10:ci` 并在容器内执行 E8/E9/E10 A 轨；下载 artifact 后把 `A-e8`、`A-e9`、`A-e10` 分别归档到 `work/`。
- **第二次运行**：在 `5312b6d` 上用 `workflow_dispatch` 再跑一次同一 workflow，只比较语义字段，用于运行独立复核。
- **替代方案 A**：本机只用 `scan()` 的 GCC `-MM` 结果。拒绝原因：无法满足 A 轨“真实 BuildChecker 基线”的要求，只能作为单元测试或独立复核，不作为 E8/E10 的 BuildChecker 证据。
- **替代方案 B**：先安装 Docker Desktop / WSL 再本地重跑。拒绝原因：当前环境不具备安装与重启条件，且 CI 已提供同一镜像与同一脚本。
- **替代方案 C**：引用旧 CI 运行或他人结果。拒绝原因：证据必须对应当前分支提交（E8 为 `77e891c`，E9/E10 为 `5312b6d`）。

A：缓存何时失效、配置身份如何绑定：

- 缓存 key 由项目内 C/H 的预处理指令、Makefile 配方、CFLAGS 与编译器版本组成；任一变化则保守刷新 `main.o`、`helper.o` 两个目标。
- 身份绑定：外层学生源码用分支 headSha `77e891c…`；样例内部用 C0 提交 `f4d0e19…`；镜像用 tag `course-e8e10:ci` 与 ID `sha256:c76ea6c…`。三者分别写入 `student-source-commit.txt`、`baseline.json` 与 `environment-image-id.txt`。
- 个人测试额外验证配方变化、头文件宏值变化、无关头文件新增都会改变 key，从而触发刷新；其中后两项同时验证依赖图/findings 不变。第四个测试按 A09 分工要求验证“删除已有 include”：缓存失效、两个目标刷新、`resolved` 精确包含 `["MISSING","main.o","config.h"]`，且 `added` 为空。

E9/E10 的增量策略与复核：

- E9 C1 只改函数体，key 不变，`main.o`/`helper.o` 都复用历史图；C2 新增 `#include "extra.h"`，预处理指令变化触发两个目标刷新，并计算 `added`；C3 只改 Makefile 声明，配方不变，继续复用，并计算 `resolved`。
- E10 对六个场景各重复 5 次；每行都同时运行 `scan(p, prev)` 与 `scan(p)`，要求 `actual`/`declared`/`findings` 完全相等，否则 `assert` 失败、`gate.json` 不可能为通过。
- 独立复核分两层：方法层用真实 BuildChecker 对照 GCC 投影、用全量扫描对照增量扫描；运行层在同一 headSha 上做两次 CI，去掉 commit/timing/trace-id 后逐字段比较。

B：共享变量怎样处理、失败怎样保证原目录不变（**课程参考实现说明，本人未执行 B 轨**）：

- 以下内容来自课程参考实现的阅读，用于理解 A 轨接口和边界，不是本人 B 轨实验结果；仓库内也没有 B 组返回或签收证据。
- `declarations()` 只展开 Makefile 中的简单变量（最多 8 层），遇到 `$`、`%`、`|` 等未支持形式显式报错。
- `patch()` 先校验报告 commit 与当前 C0 一致（`STALE_REPORT`）、路径不越界（`UNSAFE_PATH`）、输入存在；`validate()` 在 evidence/sandbox 副本中构建与测试，全部通过后才把 Makefile 写回原项目，失败时原目录不变。
- E8 只读取与扫描，不修改受测项目；未变化扫描复用历史图，避免误报新增/消除。

代价与覆盖范围：

- 证据生成依赖 GitHub Actions 网络与 runner；artifact 只保留 14 天，因此关键文件已复制进仓库归档。
- 教学 BuildChecker 只支持单 Make 进程、每个 recipe 一个最终输出、项目内路径与受限配置；不能外推到任意构建系统。
- 未在本机执行 BuildChecker，报告中明确标注为 CI 运行，不把 CI 结果写成“本机实测”。

验证命令与实际证据：

```bash
# CI 中实际执行（容器内）
python3 labs/e8e10/lab.py e8 --track A --out /course/work/A-e8
python3 labs/e8e10/lab.py e9 --track A --out /course/work/A-e9
python3 labs/e8e10/lab.py e10 --track A --out /course/work/A-e10

# 本地单元测试
cd labs/e8e10
python3 -m unittest discover -s . -p test_profile.py -v   # Ran 11 tests, OK（本地；CI 41667606590 时为 10 项）

# 两次独立检验
python3 -I work/e8e10-A-verification/scripts/e9_method_check.py . /tmp/e9-check
python3 -I work/e8e10-A-verification/scripts/e8_e10_method_check.py . <artifact>/all /tmp/e8e10-check
python3 -I work/e8e10-A-verification/scripts/rerun_compare.py <run1>/all <run2>/all /tmp/rerun-check
```

- `work/e8-A-ci-41662015872/baseline.json`：`actual`、`declared`、两条 findings。
- `work/e8-A-ci-41662015872/incremental.json`：`reused=[main.o,helper.o]`、`refreshed=[]`。
- `work/e8-A-ci-41662015872/buildchecker/findings.json`：`status=SUCCEEDED`。
- `work/e8-A-ci-41662015872/buildchecker/trace/t.28:579`：`openat(... "config.h" ... O_RDONLY ...) = 4`。
- `work/e9-A-ci-41663999896/C1.json`、`C2.json`、`C3.json`：复用/刷新/新增/消除集合。
- `work/e10-A-ci-41663999896/results.csv`：30 行全部 `equal=True`；`gate.json` 通过；`performance-summary.csv` 给出六场景中位数/极值/比值，`结论.txt` 为文字汇总。
- `work/e8e10-A-verification/check1-method/` 与 `check2-rerun/`：两次独立检验均通过（`passed=true`、`differences=[]`）。
- Actions：E8 https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/41662015872；E9/E10 https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/41663999896；第二次运行 https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/41666559898；最终推送门禁 https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/41667606590（headSha `3afc345`）。
- PR #12：https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/pull/12；PR 检查 run `41669789469`（E8–E10）、`41669789798`（E7 A）；合并提交 `1fe05f4c7024057b56b713ea1d911575824c2ed2`。
- A→B 交接：**未执行**，见 `A-B交接状态.md`；仓库内没有可填写的 B 组返回、dry-run PR/commit 或交换时间/参与人。

## 最终状态与未完成项

- `main` 已合并 PR #12（`1fe05f4`），原 `e7-a-quality-gate` 与 `e8e10-quality-gate` 均保留并成功。
- 第 4 个个人测试（删除已有 include）在最终 CI 后新增，当前仅本地 11 项通过；最终 CI `41667606590` 仍为 10 项。
- 已下载的 CI artifact 缺少 `project/.git`（生成时 `e8e10.yml` 未设置 `include-hidden-files: true`）；工作区已补该设置，但尚未重跑，现有归档仍不足以单独证明样例内部完整历史。
- E10 CI 原始产物为扁平布局；`matrix/` 是同一 run 的重组副本，不是第二次运行，也没有逐次成对 JSON。本地已补 `performance-summary.csv` 与 `结论.txt`，但不冒充 CI 原生产物。
- A→B 交接未执行，不能声称完成。
