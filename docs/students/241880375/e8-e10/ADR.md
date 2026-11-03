# 决策记录

## 背景与约束

本阶段张海洋负责 A 组 E8 真实基线和 E9 C0—C3 原始复现。目标是让“实际依赖图”来自真实 BuildChecker / GCC 观测，而不是只相信 Makefile 声明；同时保留可重复、可核验的 OUT、日志、JSON 和内部 Git 提交。

约束：

- 教学实现只支持两个固定对象目标、顶层 C/H 文件、简单显式规则、简单变量和受限 CFLAGS。
- 外层学生仓库保存代码和报告；`work/project` 内部 Git 只记录被测样例 C0—C3，不用于学生提交。
- 不能把论文的 85.14× 或 MDFixer 的 62.999s 当作自己的测量值。

## 选择与替代方案

### 选择 A：保守缓存失效

缓存 key 同时包含：

- 所有本地 `.c` / `.h` 文件的预处理指令行；
- Makefile 配方行；
- CFLAGS；
- 编译器版本。

任一 key 分量变化时，刷新两个对象目标；key 不变时复用历史 actual graph。

### 替代方案 B：按目标精细失效

只刷新受变化文件直接影响的目标，或直接信任 Makefile 声明。

未采用原因：当前 Makefile 声明本身可能缺少头文件依赖（本实验正是 MISSING/REDUNDANT 场景），直接信任声明会漏掉真实读取；按目标精细失效需要更完整的 include 图和规则解析，超出本教学子集。保守刷新优先保证不漏边，代价是 C2 中 helper.o 也被刷新。

### 选择 A：观察图与声明图分离

`actual` 来自 GCC `-MM` 或 BuildChecker actual-graph；`declared` 来自 Makefile 解析。两者分开保存，再计算 MISSING/REDUNDANT。

未采用原因：把 Makefile 声明直接当作实际图会使 MD/RD 永远为零，无法复现论文要检查的问题。

## 代价与覆盖范围

- 代价：保守刷新会多刷新未受影响目标；E9 C2 中 helper.o 也被刷新，不是最小增量。
- 覆盖：两个对象目标、顶层 C/H、direct/macro/mixed 声明、`-O0`/`-O1`/`-O0 -DMODE=1`。
- 不覆盖：通配符、模式规则、自动变量、生成头文件、系统头文件、并行 Make、复杂条件分支。

## 验证命令与实际证据

E8 A：

```text
OUT=work/e8-A-manual.EnuiNJ
BuildChecker status=SUCCEEDED
actual=main.o:[config.h,main.c], helper.o:[helper.c]
findings=MISSING main.o config.h; REDUNDANT main.o unused.h
incremental: reused=[main.o,helper.o], refreshed=[]
```

E9 A：

```text
OUT=work/e9-A-manual.7C5OcS
C0 b07ac921ff4fe955ec1f05977351b69c859d9ecc
C1 9ce53cbb3fd2c438e6d83166149c7e28b56f808b  reused=[main.o,helper.o]
C2 4676950b47bed7890c5f53b5de533f7f45a4eb53  refreshed=[main.o,helper.o], added=MISSING extra.h
C3 9bbe6f805be76c69672fa7c12b53a6efe7c0769e  resolved=MISSING config.h, MISSING extra.h
```

单元测试：

```text
Ran 8 tests in 0.178s
OK
```

新增测试 `StudentE9A.test_include_inside_header_invalidates` 验证头文件内部新增 include 后缓存失效，并精确新增 MISSING extra.h。
