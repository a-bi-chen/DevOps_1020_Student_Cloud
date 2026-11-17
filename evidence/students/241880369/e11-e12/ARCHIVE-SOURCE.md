# E11–E12 证据归档说明（241880369）

- 学生：高嘉程 / 241880369 / A09 A 组
- 仓库：<https://github.com/a-bi-chen/DevOps_1020_Student_Cloud>
- 分支：`student/241880369/e11-e12`
- PR：[#23](https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/pull/23)
- 首推代码/测试 head：`d4c3a62936c9af5d089fdc3215c9f185f827c5e5`
- PR base：`main @13c0f8d0ef265580de4b1063aeafde62061b7437`
- 服务器：`iZbp106a3t3mzz3nfabub1Z`（Ubuntu 22.04.5 LTS，x86_64）
- 镜像：`course-e11e12:241880369`
- 镜像 ID：`sha256:ba4e7393b9fbc9ecd1a8ed1b3daca8aceafa7dc8a54528ae7ffd34d4aacd2949`

## Actions 与 artifact

| 检查 | Run | 结果 |
|---|---|---|
| E7 A quality gate | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/44050562165> | success |
| E8–E10 teaching validation | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/44050562157> | success |
| E11–E12 integration | <https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/44050562100> | success |

push 触发的重复 run：E7 `44050537419`、E8–E10 `44050537363`、E11–E12 `44050537445`，同样 success。

Actions artifact：

- 名称：`e11e12-evidence-44050562100`
- 原始大小：343,396 B
- 仓库归档：`actions-artifacts/e11e12-evidence-44050562100.zip`
- 归档 zip SHA256：`cddefe63b0f74d767b10781a7541cd3bbaecc355e369db4f71e86f88f74cd4ac`
- 归档 zip 大小：335,672 B
- 说明：zip 由 `gh run download` 解包后重新压缩；GitHub API 未直接暴露原始 artifact 的 SHA256，因此以本地归档 zip 的 SHA256 为准。

## 本地证据包

- 文件：`e11e12-evidence-241880369.tar.gz`
- SHA256：`34d282cdf0760883c6c927abd512161fd034156ff49a954276d45b7b41aac51e`
- 大小：约 272 KB（压缩后）
- 内容：
  - `work/e11-a-241880369/`：E11-A 全量/增量图、Make DB、trace、result
  - `work/e12-241880369/`：E12 首次失败证据（DRAFT 超时）
  - `work/e12-241880369-r2/`：E12 固定样例五阶段
  - `work/e12-real-241880369/`：E12 真实项目五阶段
  - `work/api-client-241880369/`：API 提交、轮询、产物、哈希、409
  - `work/api-jobs/job-045cf351d04e4b5fa6c9ffe7f4ae26c3/`：API 任务状态与证据
  - 构建/测试/prepare/E11-A/E12/API 日志
  - `work/e11e12-personal-summary.json`
  - `data/real-project`、`data/real-request.json`、`data/real-candidate.Dockerfile`、`data/real-dataset.json`
  - `data/integration-sample/candidate.Dockerfile`、`dataset.json`
- 为控制体积，tar 包排除了各工作副本中的 `.git/` 目录；真实项目的 base/target SHA 和数据清单已保留。

## SHA256 清单

见同目录 `artifacts.sha256`。补充：

- `run-summary.json` SHA256：`9d0b7a0e528d11352129780ed3f1e545bfbd3e476635f562a4f94002c5984242`

## 说明

- 本归档只记录本人实际运行结果，不包含队友的 `job_id/trace_id`。
- E11-B 与 B09 正式签收引用团队证据：`evidence/students/241880375/e11-e12/b09-signoff/`。
- 未包含密码、Token、私钥。
