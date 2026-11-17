# E13–E14 入口：交接、日志扫描与四服务编排

本目录由课程 E13–E14 实验包导入，配合已有 `labs/e11e12` 和 `run_e11e12.py` 使用。

| 文件 | 用途 |
| --- | --- |
| `handoff_a_to_b.py` | 校验 A 的 `result.json`、目标提交和产物字节哈希，生成 B 可读的 `fixed-md` 信封，并保留来源 `job_id`/`trace_id`/报告 SHA256 |
| `scan_runtime_logs.py` | 扫描 `work/` 运行日志中的疑似密钥；退出码 0 无命中、1 命中、2 扫描不完整 |
| `service.py` | 四角色 HTTP 处理器：`buildchecker`、`echecker`、`draft`、`mdfixer` |
| `orchestrate.py` | 通过 `127.0.0.1:18081–18084` 依次调用四服务，写五阶段证据 |
| `compose.yaml` | 四容器 Compose；端口只绑定宿主 `127.0.0.1`，仅 DRAFT 挂载 Docker socket |
| `tests/test_handoff.py` | 交接适配器的来源、目标提交和产物哈希篡改测试 |

## 安全边界

- 四服务只允许读写 `/course/data` 与 `/course/work` 下的路径；输出目录必须不存在。
- Compose 项目名固定为 `e14-<学号>`，关闭时只执行本项目的 `down`，不清理其他组容器。
- DRAFT 是唯一挂载 `/var/run/docker.sock` 的角色；其余角色不接触 Docker daemon。
- 日志扫描只输出命中位置、类型和遮蔽后的值，不打印完整密钥。
- 测试只使用假 Key；真实 `.env`、令牌和服务器密码不进入仓库与证据。

## 快速命令

```bash
python3 -m py_compile labs/e13e14/*.py
E14_ROOT=$PWD E14_IMAGE=course-e11e12:<学号> \
  docker compose -f labs/e13e14/compose.yaml -p e14-<学号> config --quiet
E14_ROOT=$PWD E14_IMAGE=course-e11e12:<学号> \
  docker compose -f labs/e13e14/compose.yaml -p e14-<学号> up -d
python3 labs/e13e14/orchestrate.py \
  --request data/integration-sample/e12.json --out work/e14-compose-sample-01
python3 labs/e13e14/scan_runtime_logs.py work/e14-compose-sample-01
E14_ROOT=$PWD E14_IMAGE=course-e11e12:<学号> \
  docker compose -f labs/e13e14/compose.yaml -p e14-<学号> down
```
