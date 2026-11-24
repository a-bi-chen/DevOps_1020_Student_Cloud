# E13 跨项目检测适配（A09）

本目录用于 E13 与 B09 的交叉联调，不修改 `labs/e11e12` 的课程入口语义。

## 为什么需要适配

B09 的项目位于 `fixtures/e11e12-b1-real` 子目录，且 `CFLAGS = -std=c11 -Wall -Wextra -Werror`。A09 现有入口有两个明确约束：

1. `labs/e11e12/pipeline.py` 的 `snapshot()` 以**仓库根**为项目根，并要求根目录恰好是 `main.c` / `helper.c` / `config.h`；
2. `labs/e8e10/lab.py` 的 `scan()` 只接受 `-O0`、`-O1`、`-O0 -DMODE=1`。

因此官方入口不能直接在该子目录运行；`run_crosscheck.py` 会把两种官方尝试的真实错误写入 `official-entry-*.log` 和 `entry-probes.json`，再按同一 EChecker 算法使用 E13 flags 配置执行增量检测。BuildChecker 的 `full_check` 原实现不改。

## 运行

在 Linux 云主机上，于 A09 仓库根执行：

```bash
python3 labs/e13/run_crosscheck.py \
  --repo /root/241880089/b09-e13 \
  --subdir fixtures/e11e12-b1-real \
  --base 30ffe4c41492334478a2446a8be0662d3f31d478 \
  --target a7e3b644ca9b1b9d0b26bd41e839fcbf5ea1c293 \
  --out work/e13-b09
```

输出目录必须是 `work/` 下全新的空目录。脚本会：

- 以 `git clone` + `git checkout --detach` 精确检出两个原始提交，并用 `git rev-parse HEAD` 复核；
- 执行 `make clean`、`make`、`make test`、`./app`，记录退出码和 stdout；
- 在 Base/Target 上运行 BuildChecker `full_check`；
- 以 Base 全量结果为缓存，对 Target 执行 EChecker 增量扫描，并与 Target 全量结果对照；
- 生成 `detection-report.json`、`detection-report.md` 和 `SHA256SUMS`。

## 结果判据

- Base：无 `main.o`/`helper.o` 依赖缺陷；
- Target：恰好 `MISSING(main.o, extra.h)`；
- 两次 `make clean && make`、`make test` 均成功，`./app` 输出 `hello E3`；
- 增量 findings 与 Target 全量 findings 一致。
