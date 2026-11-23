# A09 → B09 E13 交换项目与检测报告

- 提供方：A09 / 241880375 张海洋
- 接收方：B09
- 日期：2026-11-17
- A09 仓库：<https://github.com/a-bi-chen/DevOps_1020_Student_Cloud>
- A09 分支：`student/241880375/e13-e14`

## 1. 项目来源

- 上游项目：<https://github.com/course-one/make-introduction>
- 上游提交：`a789b2f4f09675fd882ed57c88a1677ec852fc48`
- A09 在 E11–E12 中完成课程适配的独立 Git 项目：本目录 `a09-e13-project.bundle`
- bundle SHA256：`40510b4c02a05b0ce372ee7870c53ca4d4f32978599e93d8c7ac1b3a2e319072`
- 项目子目录：`.`（bundle 仓库根目录即项目根目录）

克隆：

```bash
git clone -b a09-e11-adapted-base a09-e13-project.bundle a09-project
cd a09-project
git checkout ba688c40d13cd8658e554f7544f1546d35b4b397
```

## 2. 交换提交

| 角色 | 完整 SHA | 说明 |
|---|---|---|
| Base | `e825395a5f8006f1c57a115cc25ea5c7802863ee` | 课程适配基线 |
| Target | `ba688c40d13cd8658e554f7544f1546d35b4b397` | `main.c` 新增 `#include "extra.h"`，Makefile 头文件声明保持不变 |

适配说明：上游 `add/sub/calculate` 合并为 `helper.c`；保留 `calculate.o` 头文件依赖缺陷；`config.h` 的 `VALUE` 和 `extra.h` 的 `EXTRA` 共同保持输出为 `1`。

## 3. 构建、运行和测试

```bash
make clean
make app
./app
test "$(./app)" = "1"
```

- 预期标准输出：`1`
- 预期退出码：`0`
- `Makefile` 没有独立 `test` 目标；测试命令以上述输出断言为准。

## 4. 候选 Dockerfile

本目录 `candidate.Dockerfile`：

- SHA256：`6f0e3980c609a683d727c271bdd3a8d5f12b46df21f1fcc402e0d8420ce06c28`
- 已从 `python:3.13-slim` 安装 `build-essential`，执行 `make app`，容器入口为 `./app`。

## 5. A09 E13 原始检测结果

- 请求：`request.json`
- 状态：`SUCCEEDED`
- job_id：`job-131c4b1d8c34469aaa31f9e2a9da1736`
- trace_id：`trace-c224eaab92394b91bedfc2dea14ebc61`
- base：`e825395a5f8006f1c57a115cc25ea5c7802863ee`
- target：`ba688c40d13cd8658e554f7544f1546d35b4b397`
- `result.json` SHA256：`3fd3be33d41b95e9fff9762fac1b2413c649f68714f06c4b4520f3e52e769015`
- `full-check.json` SHA256：`c9de4bb36f114f9caad7111d918dde2475a080667f401f8ec707f7772686d549`
- `incremental-check.json` SHA256：`504a3c505c1479c990f59143926247a2deb7415375de5d957a2d4938aefff224`
- 完整检测证据（原始报告、日志、make DB 与 trace）：`a09-e13-detection-evidence.tar.gz`
- 检测证据包 SHA256：`ee7a35a373e5e5e5a7b3d95d7533d671d9d75858494e2aeafc51f70c2e73c128`

Target 的增量发现：

```text
MISSING(main.o, calculate.h)
MISSING(main.o, config.h)
MISSING(main.o, extra.h)
REDUNDANT(main.o, unused.h)
MISSING(helper.o, add.h)
MISSING(helper.o, calculate.h)
MISSING(helper.o, sub.h)
```

相对 Base，本轮新增的是 `MISSING(main.o, extra.h)`；其余为适配项目保留的既有发现。

## 6. 给 B09 消费的 handoff 信封

- 文件：`../handoff/fixed-md-a09-project.json`
- SHA256：`623e6854cb99904eb20e49e72436a182a83446a1e68e2218741971bca1f618a2`
- source job_id：`job-131c4b1d8c34469aaa31f9e2a9da1736`
- source trace_id：`trace-c224eaab92394b91bedfc2dea14ebc61`
- source report URI：`artifact://job-131c4b1d8c34469aaa31f9e2a9da1736/incremental-check.json`
- source report SHA256：`504a3c505c1479c990f59143926247a2deb7415375de5d957a2d4938aefff224`

B09 使用 `fixed_report_sha256=623e6854cb99904eb20e49e72436a182a83446a1e68e2218741971bca1f618a2` 消费 handoff 文件；不得改写报告字节。
