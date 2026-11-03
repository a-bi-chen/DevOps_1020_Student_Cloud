# 决策记录

背景与约束：

- A 轨 E8 要求用真实 BuildChecker（strace + Make 数据库）建立对象依赖基线，并与 Makefile 声明比较；不能只用 GCC `-MM` 投影冒充真实基线。
- 本机为 Windows，未安装 Docker/ WSL，且课程 SSH 服务器当前不可达；教学镜像与 `strace -ff` 只能在 Linux 上运行。
- 个人提交必须落在 `student/241880089/e8-e10`，不能直接改 `main`。

选择与替代方案：

- **选择**：在个人分支推送提交，触发 `.github/workflows/e8e10.yml`，在 `ubuntu-24.04` 上构建 `course-e8e10:ci` 并在容器内执行 E8 A 轨；下载 artifact 后把 `A-e8` 归档到 `work/e8-A-ci-41662015872/`。
- **替代方案 A**：本机只用 `scan()` 的 GCC `-MM` 结果。拒绝原因：无法满足 A 轨“真实 BuildChecker 基线”的要求，只能作为单元测试，不作为 E8 证据。
- **替代方案 B**：先安装 Docker Desktop / WSL 再本地重跑。拒绝原因：当前环境不具备安装与重启条件，且 CI 已提供同一镜像与同一脚本。
- **替代方案 C**：引用旧 CI 运行或他人结果。拒绝原因：证据必须对应当前分支提交 `77e891c`。

A：缓存何时失效、配置身份如何绑定：

- 缓存 key 由项目内 C/H 的预处理指令、Makefile 配方、CFLAGS 与编译器版本组成；任一变化则保守刷新 `main.o`、`helper.o` 两个目标。
- 身份绑定：外层学生源码用分支 headSha `77e891c…`；样例内部用 C0 提交 `f4d0e19…`；镜像用 tag `course-e8e10:ci` 与 ID `sha256:c76ea6c…`。三者分别写入 `student-source-commit.txt`、`baseline.json` 与 `environment-image-id.txt`。
- 个人测试额外验证配方变化会改变 key，从而触发刷新。

B：共享变量怎样处理、失败怎样保证原目录不变：

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

# 本地单元测试
cd labs/e8e10
python3 -m unittest discover -s . -p test_profile.py -v   # Ran 8 tests, OK
```

- `work/e8-A-ci-41662015872/baseline.json`：`actual`、`declared`、两条 findings。
- `work/e8-A-ci-41662015872/incremental.json`：`reused=[main.o,helper.o]`、`refreshed=[]`。
- `work/e8-A-ci-41662015872/buildchecker/findings.json`：`status=SUCCEEDED`。
- `work/e8-A-ci-41662015872/buildchecker/trace/t.28:579`：`openat(... "config.h" ... O_RDONLY ...) = 4`。
- Actions：https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/41662015872
- 加入个人测试与报告后的验证：https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/41663498413（容器内 8 项测试通过）
