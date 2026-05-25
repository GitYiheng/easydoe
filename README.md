# easydoe

> [中文文档](README.zh.md) | A minimal CLI for generating design-of-experiments configs via Latin Hypercube Sampling.

## Install

```bash
pip install -e .
```

## Quick Start

`doe` takes two things: a **config file** and an **output file**.

```bash
# Basics
doe <config.yaml> -o <output.csv>

# Use the built-in template
doe src/easydoe/templates/default.yaml -o experiments.csv

# Or write your own config
doe my_config.yaml -o runs/batch_001.csv --seed 42
```

## Config Format

```yaml
n_samples: 30
seed: 42
output: experiments.csv

params:
  lr:
    type: log
    low: 1.0e-5
    high: 1.0e-2

  dropout:
    type: linear
    low: 0.1
    high: 0.5

  batch_size:
    type: choice
    values: [16, 32, 64]
```

## Parameter Types

| Type     | Fields        | Example                  |
| -------- | ------------- | ------------------------ |
| `linear` | `low`, `high` | Continuous uniform       |
| `log`    | `low`, `high` | Log-uniform (for lr, wd) |
| `int`    | `low`, `high` | Integer uniform          |
| `choice` | `values`      | Discrete options         |

## Output File

Format auto-detected by extension:

```bash
doe cfg.yaml -o experiments.csv    # CSV
doe cfg.yaml -o experiments.yaml   # YAML
doe cfg.yaml -o experiments.json   # JSON
```

## Full Workflow Example

- **Step 1**: Write `transformer_tune.yaml`

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

- **Step 2**: Generate

```bash
doe transformer_tune.yaml -o runs/batch_1.csv
```

- **Step 3**: Train

```python
import csv

with open('runs/batch_1.csv') as f:
    for row in csv.DictReader(f):
        lr = float(row['lr'])
        # ... train
```

## CLI Options

| Flag        | Purpose                | Example                         |
| ----------- | ---------------------- | ------------------------------- |
| `--seed N`  | Fix random seed        | `doe cfg.yaml --seed 42`        |
| `--dry-run` | Preview without saving | `doe cfg.yaml --dry-run`        |
| `-o path`   | Override output path   | `doe cfg.yaml -o /tmp/test.csv` |
