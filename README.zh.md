# easydoe

> [English](README.md) | 极简的实验设计（DOE）命令行工具，基于拉丁超立方采样（LHS）生成机器学习超参配置。

## 安装

```bash
pip install -e .
```

## 快速开始

`doe` 只需要两个东西：**配置文件** 和 **输出文件**。

```bash
# 基本用法
doe <配置文件.yaml> -o <输出文件.csv>

# 使用内置模板
doe src/easydoe/templates/default.yaml -o experiments.csv

# 或自定义配置
doe my_config.yaml -o runs/batch_001.csv --seed 42
```

## 配置文件格式

```yaml
n_samples: 30           # 采样数量
seed: 42                # 随机种子（可选）
output: experiments.csv # 输出路径（可选，也可通过 -o 指定）

params:                 # 参数定义
  lr:                   # 参数名
    type: log           # 对数均匀分布
    low: 1.0e-5         # 最小值
    high: 1.0e-2        # 最大值

  dropout:
    type: linear        # 线性均匀分布
    low: 0.1
    high: 0.5

  batch_size:
    type: choice        # 离散值
    values: [16, 32, 64]
```

## 参数类型

| 类型     | 字段         | 说明                                   |
| -------- | ------------ | -------------------------------------- |
| `linear` | `low`, `high` | 连续均匀分布（线性尺度）               |
| `log`    | `low`, `high` | 对数均匀分布（适用于学习率、权重衰减等） |
| `int`    | `low`, `high` | 整数均匀分布                           |
| `choice` | `values`      | 离散选项                               |

## 输出文件

根据文件扩展名自动判断格式：

```bash
doe cfg.yaml -o experiments.csv   # CSV 格式
doe cfg.yaml -o experiments.yaml  # YAML 格式
doe cfg.yaml -o experiments.json  # JSON 格式
```

## 完整工作流示例

- **第1步**：编写 transformer_tune.yaml

```yaml
n_samples: 30
seed: 2024

params:
  lr:
    type: log
    low: 1e-5
    high: 5e-4
  n_layers:
    type: int
    low: 2
    high: 8
  hidden_dim:
    type: choice
    values: [256, 512, 768]
  dropout:
    type: linear
    low: 0.0
    high: 0.3
```

- **第2步**：生成实验配置

```bash
doe transformer_tune.yaml -o runs/batch_1.csv
```

- **第3步**：训练模型

```python
import csv

with open('runs/batch_1.csv') as f:
    for row in csv.DictReader(f):
        lr = float(row['lr'])
        # ... 进行训练
```

## CLI 选项

| 参数        | 作用                   | 示例                             |
| ----------- | ---------------------- | -------------------------------- |
| `--seed N`  | 固定随机种子           | `doe cfg.yaml --seed 42`         |
| `--dry-run` | 预览结果，不保存文件   | `doe cfg.yaml --dry-run`         |
| `-o path`   | 覆盖输出文件路径       | `doe cfg.yaml -o /tmp/test.csv` |
