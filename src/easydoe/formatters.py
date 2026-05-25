import csv
import json
import yaml
from pathlib import Path


def save_experiments(experiments: list[dict], path: str):
    """Auto-detect format by extension and save."""
    path = Path(path)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        _save_csv(experiments, path)
    elif suffix in (".yaml", ".yml"):
        _save_yaml(experiments, path)
    elif suffix == ".json":
        _save_json(experiments, path)
    else:
        # Default to CSV
        csv_path = path.with_suffix(".csv")
        _save_csv(experiments, csv_path)
        print(f"Unknown extension '{suffix}', saved as CSV: {csv_path}")


def _save_csv(data: list[dict], path: Path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)


def _save_yaml(data: list[dict], path: Path):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump({"experiments": data}, f, default_flow_style=False, sort_keys=False)


def _save_json(data: list[dict], path: Path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
