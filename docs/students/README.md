# 个人材料目录

`main` 已包含四名成员的最终个人材料与个人测试（共 14 项：基础 `ProfileTests` 7 项 + 个人测试 7 项）。目录索引：

| 学号 | 姓名 | 个人材料目录 | 个人测试类 |
|---|---|---|---|
| 241880089 | 陈玉熙 | `241880089/e8-e10/` | `StudentE8A089`、`StudentE9A089`、`StudentE10A089`、`StudentE9A089RemovedInclude` |
| 241880369 | 高嘉程 | `241880369/e8-e10/` | `StudentE10A` |
| 241880374 | 马海川 | `241880374/e8-e10/` | `StudentE8A` |
| 241880375 | 张海洋 | `241880375/e8-e10/` | `StudentE9A` |

## 模板与新增成员

- `_template/`：个人报告、ADR、AI 使用记录的官方模板，仍保留在 `main` 作为空白模板。
- 每名成员在**自己的分支**创建 `<学号>/e8-e10/`，把三份模板复制进去后填写：

```bash
mkdir -p "docs/students/<学号>/e8-e10"
cp docs/students/_template/*.md "docs/students/<学号>/e8-e10/"
```

- 目录名使用纯数字学号（与 `student/<学号>/e8-e10` 分支、`course-e8e10:<学号>` 镜像一致）。
- 不修改他人的目录；个人材料随个人 PR 合并。
