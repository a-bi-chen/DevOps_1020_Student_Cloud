# B09 补充回归包取样核验（2026-11-25）

- 对象：B1 专项补充回归包 `e13-b1-server-formal-20261124-101140.tar.gz`
- 下载：https://github.com/llxxy-cn/devops-b09/releases/download/v0.9-rc/e13-b1-server-formal-20261124-101140.tar.gz
- GitHub Release asset digest：`sha256:23753210e75b0892663c35e052d7575cd5d00c042ef6ed82c606b9bbdb2abe89`
- 本地复算：`23753210e75b0892663c35e052d7575cd5d00c042ef6ed82c606b9bbdb2abe89`，字节数 22,261,646
- 被测提交：`298ff1366cdd2f4314cce625492fa813f484893f`
- 修复提交：`7eefa00176b6a718347e94da6a8089f8dc091a88`（父 `ba688c40d13cd8658e554f7544f1546d35b4b397`）
- 结论：C1 `SUCCEEDED`（153 产物）、6/6 修复边重建且输出匹配、MD=0 / RD=1；C2 `STALE_REPORT`、C3 `ARTIFACT_HASH_MISMATCH` 且无补丁；恢复 `SUCCEEDED`
- 范围：单份补充回归，不替换 2026-11-23 已签收包（`1a1419b6...`）
- 说明：本目录只保存核验摘要，不保存 22 MB 原始包；原始包以上述公开地址为准，哈希见 `verification.json`
