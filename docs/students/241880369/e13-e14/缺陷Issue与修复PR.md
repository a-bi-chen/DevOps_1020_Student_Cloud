# 缺陷 Issue 与修复 PR（E13–E14 个人复跑，241880369）

## 结论

本轮个人独立复跑（C1–C8、H1–H3、E14 四容器与故障恢复、个人测试）**未发现新的阻断缺陷**，未新增 Issue/PR。

## 记录

- 用例编号与发现方：无新增（个人复跑未触发阻断）
- 组级阻断缺陷（团队已闭环，非本人新增）：
  - Issue/PR #19、#21：团队已修复并回归，证据见 `docs/students/241880375/e13-e14/缺陷Issue与修复PR.md`。
- 非阻断观察：
  - 编排层顶层 `incremental-check.json` 是阶段包装，真实被 MDFixer 消费的是 echecker 服务目录 `incremental/incremental-check.json`。个人报告与 ADR 已按“服务侧实际文件”核对报告 SHA，未改动实现，仅修正核对路径说明。
  - 复检如实保留 `REDUNDANT(main.o, unused.h)`，未为通过而删除。
- Secret：假 Key 仅用于隔离对照，扫描器输出掩码；运行日志 2820 文件 0 命中，工作区+历史 1105 文件无问题。
