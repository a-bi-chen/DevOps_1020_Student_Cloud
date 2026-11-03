# E7 摘要

- 改动：BuildChecker 实测构建依赖，检测 Makefile 声明与实际依赖的 `MISSING` / `REDUNDANT`；加入 E7 门禁、项目根边界测试、失败-恢复 CI 演示。
- 成果：17 项测试通过；gate `8/8`；oracle 6 项通过；secret scan 无问题；CI 全绿；main 保护生效。
- 最终 main：`abaa94c`；PR #1–#5 全部合并；镜像 `course1020-buildchecker:241880369-final`。
- 详细记录：`docs/实验报告.md`、`docs/reports/`。
