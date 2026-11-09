# E8 A 轨证据（CI run 41662015872）

- 来源：GitHub Actions `E8-E10 teaching validation`，run [41662015872](https://github.com/a-bi-chen/DevOps_1020_Student_Cloud/actions/runs/41662015872)，headSha `77e891c4da81b40f14a75045829b637e1444dbe7`。
- 运行环境：`ubuntu-24.04` + 镜像 `course-e8e10:ci`（`sha256:c76ea6c17331defaa9c67302b1ebcfa0510706e0df2dbd52bcffb4db1c197894`）。
- 实际命令：容器内 `python3 labs/e8e10/lab.py e8 --track A --out /course/work/A-e8`，即本目录的原 `work/A-e8`。
- 文件：
  - `baseline.json`：首次扫描；`actual` 已由 BuildChecker `actual-graph.json` 投影覆盖。
  - `incremental.json`：对未变化 C0 再次扫描，复用两个对象目标。
  - `buildchecker/`：clean build、Make 数据库、strace trace、实际/声明图与 findings。
  - `student-source-commit.txt`：外层分支提交与样例内部 C0 提交（两者用途不同）。
  - `environment-image-id.txt`：镜像标签、镜像 ID、runner 与编译器。
  - `结论.txt`：本次 E8 结论。
- 说明：`student-source-commit.txt`、`environment-image-id.txt`、`结论.txt` 由下载 artifact 后补充；其余文件为 CI 原始产物。artifact 名 `e8e10-evidence-41662015872`，保留 14 天。
- artifact 限制：下载的 `project/` 中没有 `.git`。生成该 artifact 时，`e8e10.yml` 的 `upload-artifact` 未设置 `include-hidden-files: true`，GitHub Actions 默认排除隐藏文件；因此本目录不能单独证明样例内部的完整 git 历史。工作区已补该设置，但尚未重跑；`baseline.json` 仍保留 C0 提交值，但“完整历史”需重跑并归档，不能用现有文件补造。
