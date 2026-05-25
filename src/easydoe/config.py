import yaml
from pathlib import Path


def load_config(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(p, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # Validation
    if "params" not in cfg:
        raise ValueError("Config must contain a 'params' section")
    if not isinstance(cfg["params"], dict):
        raise ValueError("'params' must be a dictionary")

    for name, spec in cfg["params"].items():
        if "type" not in spec:
            raise ValueError(f"Parameter '{name}' missing 'type'")

        ptype = spec["type"]
        if ptype in ("linear", "log", "int"):
            if "low" not in spec or "high" not in spec:
                raise ValueError(f"Parameter '{name}' (type={ptype}) requires 'low' and 'high'")
            if ptype == "log" and (spec["low"] <= 0 or spec["high"] <= 0):
                raise ValueError(f"Parameter '{name}' log bounds must be > 0")
        elif ptype == "choice":
            if "values" not in spec or not isinstance(spec["values"], list):
                raise ValueError(f"Parameter '{name}' (type=choice) requires 'values' list")
        else:
            raise ValueError(f"Parameter '{name}': unknown type '{ptype}'")

    return cfg
