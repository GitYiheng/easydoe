import numpy as np
from pyDOE2 import lhs


def _lhs_deterministic(n_params: int, n_samples: int, seed: int | None = None):
    """Deterministic Latin Hypercube Sampling using RandomState."""
    rng = np.random.RandomState(seed)
    samples = np.zeros((n_samples, n_params))
    for i in range(n_params):
        perm = rng.permutation(n_samples)
        samples[:, i] = (perm + rng.rand(n_samples)) / n_samples
    return samples


def _map_one(value: float, spec: dict):
    """Map a single [0,1] LHS sample to actual parameter value."""
    ptype = spec["type"]

    if ptype == "linear":
        return float(value * (spec["high"] - spec["low"]) + spec["low"])

    if ptype == "log":
        log_low, log_high = np.log10(spec["low"]), np.log10(spec["high"])
        return float(10 ** (value * (log_high - log_low) + log_low))

    if ptype == "int":
        raw = value * (spec["high"] - spec["low"]) + spec["low"]
        return int(np.round(raw))

    if ptype == "choice":
        values = spec["values"]
        idx = min(int(np.floor(value * len(values))), len(values) - 1)
        return values[idx]

    raise ValueError(f"Unknown parameter type: {ptype}")


def generate_lhs(cfg: dict) -> list[dict]:
    params = cfg["params"]
    n_samples = cfg.get("n_samples", 30)
    n_params = len(params)
    seed = cfg.get("seed")

    # 有 seed 时用确定性实现，保证可复现；无 seed 时回退到 pyDOE2
    if seed is not None:
        samples = _lhs_deterministic(n_params, n_samples, seed=seed)
    else:
        samples = lhs(n_params, samples=n_samples)

    names = list(params.keys())
    experiments = []
    for i in range(n_samples):
        exp = {
            name: _map_one(samples[i, j], params[name])
            for j, name in enumerate(names)
        }
        experiments.append(exp)

    return experiments