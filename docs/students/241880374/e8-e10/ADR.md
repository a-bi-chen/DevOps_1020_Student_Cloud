# 决策记录

## 背景与约束

E8—E10 要求每个人独立完成 A 组 EChecker 教学实验，并保留可复核证据。教学 profile 只覆盖两个固定对象目标、顶层 C/H 文件、显式 Make 规则和简单变量。

## 选择与替代方案

### A：缓存失效策略

选择：当所有本地 C/H 文件预处理指令、Makefile recipe、CFLAGS 或编译器版本变化时，保守刷新全部对象目标；签名相同时复用实际图，但仍重新计算声明图和 findings。

替代方案：仅精细刷新受影响目标。该方案更接近论文完整能力，但需要更完整的命令、目标归属和系统调用归并，不适合当前受限样例。

代价：存在保守刷新，部分未受影响目标也会重新执行 `gcc -MM`。

### B：源文件保护

本次个人实验只运行 A 组扫描和验证，不自动修改源 Makefile。E10 B 的接受、拒绝和回滚语义只作为参考范围，不在本轮个人路线中冒充已完成。

## 验证命令与实际证据

```text
python3 run_lab.py e8 --track A --out work/e8-A-ma-20261103-100326
python3 run_lab.py e9 --track A --out work/e9-A-ma-20261103-184632
python3 run_lab.py e10 --track A --out work/e10-A-ma-20261103-184708
```

证据：

```text
work/e8-A-ma-20261103-100326/
work/e9-A-ma-20261103-184632/
work/e10-A-ma-20261103-184708/
work/unit-tests-personal-20261103-184825.log
```
