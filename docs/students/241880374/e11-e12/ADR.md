# ADR：E11–E12 个人契约测试选择

编号、日期、作者：E11E12-ADR-241880374 / 2026-11-16 / 马海川

问题：现有测试只验证 `repo` 不能越出 `/course/data`，未覆盖 API 的其他文件输入。

候选方案：

1. 重复测试已有 repo 边界；
2. 测试 candidate 越界；
3. 测试 fixed_report 越界。

采用方案与原因：选择测试 candidate 越界。E11/E12 会把候选 Dockerfile 路径传给 API，若缺少边界检查，服务可能消费 `/course/data` 之外的宿主文件。该用例与现有测试不重复，预期明确，改动最小。

输入输出字段：请求 `input.candidate`；预期抛出 `candidate must be under /course/data`。

兼容性与测试：不修改生产逻辑和既有断言；新增独立测试文件。本地 12 项测试全部通过。
