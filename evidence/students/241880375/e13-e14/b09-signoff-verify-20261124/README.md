# B09 E13 回传包 A09 独立复核（2026-11-24）

- 复核对象：B09 交付提交 `cbf90cce6fcb4950c6326704bd970f9ed80693bb`
- 回传包：`a09-e13-b09-server-return-20261122-195038.tar.gz`
- 字节数：154,556,278
- SHA256：`1a1419b6359448b7e39033899d287ed85fd44d0ca054299e238cc55d1645ba33`
- 结论：**签收成立**；无新增阻断项。

## 1. 分片重组

| 分片 | 字节数 | SHA256 |
| --- | ---: | --- |
| `a09-e13-b09-server-return-20261122-195038.tar.gz.part01` | 50,000,000 | `c8d772e777c81fa7bd5f095c2f001d158127c331ebf17bc21e4811518254fb07` |
| `a09-e13-b09-server-return-20261122-195038.tar.gz.part02` | 50,000,000 | `c205764128139f0aa4bfc28407d4837f58d89b2536bef5d7b4eb29d9498701e7` |
| `a09-e13-b09-server-return-20261122-195038.tar.gz.part03` | 50,000,000 | `96996c711ef5fae7d44010bfbfbfbe5c87ffb91cb86681545b3ce85c9cdb78ef` |
| `a09-e13-b09-server-return-20261122-195038.tar.gz.part04` | 4,556,278 | `5e390fd1c4260c82809f34c9fbbf19eb3ad0ffab997e5ee363cb649a1e857982` |

按 `part01 → part04` 顺序拼接后，字节数与 SHA256 均与 B09 声明一致。

## 2. 包内清单

- 包内 `SHA256SUMS` 为 CRLF；规范化行尾后 `17/17` 项通过。
- 未修改包内任何文件；规范化清单另存为 `package-SHA256SUMS.normalized`。
- 关键产物：`candidate.patch` `8634d2aa57acc132ddf21ef90fa087aca1a313aca37a7bc74bb9b5ce9bf29c6e`、`validation.json` `f9f4d6b0c2bae1dfcf1895a3eb83e6499a239c51f24e692e7d9fa38dcadb55e9`、`final-recheck.json` `85fd1aa62fbdbec19b9625e6ef559be8867a698c3541afdffa3e0abade0e2fe1`。

## 3. 修复 bundle

- `git bundle verify`：退出码 0，完整历史。
- 修复提交：`74eff064e1eae3e244b0acf80880c92fb4635e26`。
- 父提交：`ba688c40d13cd8658e554f7544f1546d35b4b397`，等于 A09 target `ba688c40…`。
- 改动：1 file changed, 2 insertions(+), 2 deletions(-)，仅 `Makefile`。

## 4. C1 / C2 / C3 / 恢复

| 项 | 状态 | job / trace | 关键结果 |
| --- | --- | --- | --- |
| C1 复检 | `SUCCEEDED` | `job-ec9901a266654aabb0f3c31ecc0fd697` / `trace-b9ce4c04ed934430815be6d7fc346aff` | MD=0，RD=1（`REDUNDANT(main.o, unused.h)`）；6/6 修复边重建且输出匹配 |
| C2 旧报告 | `FAILED` | `job-0c0a865d138f4249b2ef1c7f3e7791da` / `trace-99fd2dbb1b0a4bd084ab4d551e81dd7a` | `STALE_REPORT`；stages 为空，无 `candidate.patch` |
| C3 哈希篡改 | `FAILED` | `job-19d998dafff0457d8fa862b7bc784360` / `trace-828731512d364995b7f6b3af1e040014` | `ARTIFACT_HASH_MISMATCH`；stages 为空，无 `candidate.patch` |
| 恢复 | `SUCCEEDED` | `job-d7ff2505c71b4406aa8334467e5fb24a` / `trace-e0ac2f893d5c46018f124a3467682932` | 四阶段成功，生成 `candidate.patch` |

## 5. 来源、离线镜像与兼容信封

- A09 原始检测：job `job-131c4b1d8c34469aaa31f9e2a9da1736` / trace `trace-c224eaab92394b91bedfc2dea14ebc61`，target `ba688c40d13cd8658e554f7544f1546d35b4b397`。
- 原始增量报告 SHA256：`504a3c505c1479c990f59143926247a2deb7415375de5d957a2d4938aefff224`。
- 离线映射：原始 `sha256:70729b…678c2f` → 派生 `b09-e13-offline-python:3.13-slim@sha256:af8922…b40b4`；`offline-base.tar` OCI index 中存在该 digest。
- 兼容信封：A09 原件 2,806 字节 / `623e6854cb99904eb20e49e72436a182a83446a1e68e2218741971bca1f618a2`；补 `source_report.bytes=3052` 后 2,825 字节 / `c19a6b11675b86bd5f2bfe348b3faeb65151b4c57681a54103510f642845e5cf`，与 B09 声明 `c19a6b11…e5cf` 一致。

## 6. 2026-11-24 对 B09 项目的复跑

- 使用 `labs/e13/run_crosscheck.py`，保留 base `30ffe4c…` / target `a7e3b64…`。
- 结果 `SUCCEEDED`；增量 findings `[{'type': 'MISSING', 'target': 'main.o', 'dependency': 'extra.h'}]`；`added=[['MISSING', 'main.o', 'extra.h']]`。
- 新证据目录：`/root/241880089/devops-e11e12/work/e13-b09-reverify-20261124`。

## 7. 结论

B09 交付提交、四分片重组包、包内 17 项哈希、修复 bundle、C1/C2/C3/恢复、离线镜像映射与兼容信封均与声明一致。A09 确认签收；本复核不修改已签收包字节。
