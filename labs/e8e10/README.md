# labs/e8e10 教学实现（模板）

本目录是 A 轨 EChecker 的教学实现与实验环境，`main` 上保持**可直接运行的初始状态**。

| 文件/目录 | 作用 |
|---|---|
| `lab.py` | 教学实现：fixture、GCC 依赖观测、缓存 key、增量/全量扫描、Patch 与保护 |
| `test_profile.py` | 单元测试：基础 `ProfileTests` 7 项；“个人测试区”留给每名成员新增独立测试类 |
| `environment/` | 教学镜像：Dockerfile、依赖锁文件、BuildChecker、fixtures 与脚本 |

## 运行

在仓库根目录执行（`--out` 必须是 `work/` 下尚不存在的新目录）：

```bash
python3 run_lab.py build
python3 run_lab.py e8  --track A --out work/e8-A-run1
python3 run_lab.py e9  --track A --out work/e9-A-run1
python3 run_lab.py e10 --track A --out work/e10-A-run1
```

## 测试

```bash
cd labs/e8e10
python3 -m unittest discover -s . -p test_profile.py -v
```

## 新增个人测试

在 `test_profile.py` 底部的“个人测试区”添加独立测试类，例如：

```python
class StudentE8A2418800XX(unittest.TestCase):
    def test_<场景>_<预期>(self):
        ...
```

- 只新增，不改动 `ProfileTests` 的既有断言；
- 必须覆盖一个新的变化方向并给出独立预期，不能复制已有场景；
- 如果改为实现改动，需在个人报告中写明改动位置、动机与验证结果。
