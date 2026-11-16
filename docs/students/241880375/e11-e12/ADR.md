# ADR：E11–E12 集成接口决策

- 编号：ADR-241880375-E11E12-001
- 日期：2026-11-10
- 作者：张海洋 241880375
- 小组/轨道：A09 / A 组

## 问题

E11/E12 需要把 BuildChecker、EChecker、DRAFT、MDFixer 串成可复现链路，并保证跨阶段报告不会错版本、错提交或被替换。需要同时满足：

- E11-A 使用真实全量图建立历史缓存，再以增量方式检测目标提交。
- E11-B 消费固定 MD，补丁只能修复 MD，不能删除 RD。
- E12 必须使用本轮真实增量报告，不能用预置 fixed-md 代替。
- 服务通过异步 API 暴露，多客户端可能重复提交，产物下载必须可校验。

## 候选方案

1. 各组件各自产生非版本化 JSON，由脚本按文件路径直接拼接。
2. 每个阶段独立服务，A/B 各自部署，再由外部脚本共享文件。
3. 单一编排服务 + 四个组件适配器，所有阶段使用统一版本化 envelope 和 artifact URI。

## 采用方案与原因

采用方案 3：

- 统一 envelope：`schema_version=e11e12-1`、`job_id`、`trace_id`、`kind`、`commit`、`status`、`data`、`artifacts`。
- 每份下游报告在消费前校验 schema、kind、status、目标 commit 和 SHA256。
- 所有阶段产物位于本轮 `work/<job>/`，`artifact://<job>/<relative-path>` 只能解析到该任务目录，防止越界和跨任务替换。
- 单一 worker 串行执行，避免同一 Docker socket 上并发构建互相干扰；异步提交仍通过 `QUEUED/RUNNING/SUCCEEDED/FAILED/TIMED_OUT` 暴露。
- E11-A 将 BuildChecker `actual-graph.json` 投影到 `main.o/helper.o` 后写入历史缓存；扫描目标时仍由 GCC `-MM` 生成 actual，并要求增量发现与目标全量发现完全一致。
- E11-B 保留 `fixed-md` 输入以验证固定报告消费；E12 改为读取本轮 `incremental-check.json` 作为 MDFixer 输入。
- 幂等键映射到 `request_hash`；同键同输入返回同 job，同键不同输入返回 409 `IDEMPOTENCY_CONFLICT`。
- 产物 URI 使用相对路径，内容哈希同时写入清单和下载响应 `X-Content-SHA256`。

## 输入输出字段

请求：

```text
input.mode / repo / base / target / candidate / fixed_report / expected_output / build_timeout
idempotency_key
```

阶段报告：

```text
schema_version, job_id, trace_id, kind, commit, status, data, artifacts[]
artifact = { uri, sha256, bytes }
```

## 兼容性与测试

- 原 E8–E10 `lab.py` 的 scan/patch/validate 未修改；新增代码位于 `run_e11e12.py` 与 `labs/e11e12/`。
- 原 `run_lab.py`、E7/E8–E10 工作流保留。
- 新增测试覆盖服务重启状态恢复，原有 10 项契约测试保持通过。
- 服务重启后：未完成任务写为 `FAILED/SERVER_RESTARTED`；已完成任务保持原状态和 trace。

## 真实项目适配决策

固定生成样例无法证明真实仓库可接入，因此选用公开项目 `course-one/make-introduction`：

- 保留其 add/sub/calculate 真实逻辑和 Makefile 头文件依赖缺陷。
- 为适配课堂 EChecker 固定的双 `.c` 接口，将 add/sub/calculate 合并到 `helper.c`，并加入 `config.h` 驱动的输出验证。
- base/target 使用完整 Git SHA，target 只增加 `extra.h` include，不修改 Makefile 声明，用于产生真实增量 MD。
- 适配后的输入、提交、清单和失败条件全部归档，固定样例与真实项目分别执行。

## 代价

- 当前 scan/profile 仍限定 `main.o/helper.o` 和显式 Make 规则；其他项目需要适配目标映射。
- 单一 worker 牺牲吞吐量，换取课堂环境中的确定性和 Docker 资源安全。
- 证据包包含完整 `work/` 与真实项目 `.git`，体积约 6.9 MB，但可离线复核 job、trace、日志、补丁和提交。
