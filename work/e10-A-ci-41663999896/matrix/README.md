# matrix/ 目录说明

本目录不是第二次运行，也不包含新增数据。它是同一 CI run `41663999896`（headSha `5312b6d985c5cbb945cb6852bf488ba3dd5c2aef`）E10 产物的重组副本，用于对齐操作手册要求的 `matrix/` 布局。

- 来源：上级目录 `work/e10-A-ci-41663999896/`。
- 复制内容：`results.csv`、`performance-summary.csv`、`gate.json`、`baseline.json`、六个场景 JSON（`unchanged/body/include/declaration/flags/header`）与 `final-buildchecker/`。
- 上级目录仍是原始归档和权威副本；本目录文件与上级对应文件逐字节相同。
- `performance-summary.csv` 由上级 `results.csv` 计算；`结论.txt` 保留在上级目录。
- CI 只保留每个场景重复 5 次后的末次 JSON，逐次记录在 `results.csv`；没有逐次成对 JSON。本目录不补造逐次文件。

核对方式（在仓库根目录）：

```bash
for f in results.csv performance-summary.csv gate.json baseline.json \
         unchanged.json body.json include.json declaration.json flags.json header.json; do
  cmp "work/e10-A-ci-41663999896/$f" "work/e10-A-ci-41663999896/matrix/$f"
done
diff -r work/e10-A-ci-41663999896/final-buildchecker \
        work/e10-A-ci-41663999896/matrix/final-buildchecker
```
