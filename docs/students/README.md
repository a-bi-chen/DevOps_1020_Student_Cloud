# 个人材料目录

- `_template/`：个人报告、ADR、AI 使用记录的官方模板，只在 `main` 保留这一份。
- 每名成员在**自己的分支**创建 `<学号>/e8-e10/`，把三份模板复制进去后填写：

```bash
mkdir -p docs/students/<学号>/e8-e10
cp docs/students/_template/*.md docs/students/<学号>/e8-e10/
```

- 目录名使用纯数字学号（与 `student/<学号>/e8-e10` 分支、`course-e8e10:<学号>` 镜像一致）。
- 不修改他人的目录；个人材料随个人 PR 合并，`main` 不预置完成稿。
