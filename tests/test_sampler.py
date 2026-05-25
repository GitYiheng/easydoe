import pytest
import numpy as np
from easydoe.sampler import generate_lhs, _map_one


def test_map_one_linear():
    spec = {"type": "linear", "low": 0.0, "high": 10.0}
    assert _map_one(0.0, spec) == 0.0
    assert _map_one(1.0, spec) == 10.0
    assert _map_one(0.5, spec) == 5.0


def test_map_one_log():
    spec = {"type": "log", "low": 1e-5, "high": 1e-2}
    assert _map_one(0.0, spec) == 1e-5
    assert _map_one(1.0, spec) == 1e-2


def test_map_one_int():
    spec = {"type": "int", "low": 128, "high": 512}
    val = _map_one(0.5, spec)
    assert isinstance(val, int)
    assert 128 <= val <= 512


def test_map_one_choice():
    spec = {"type": "choice", "values": [16, 32, 64]}
    assert _map_one(0.0, spec) == 16
    assert _map_one(0.99, spec) == 64


def test_generate_lhs_shape():
    cfg = {
        "n_samples": 20,
        "seed": 42,
        "params": {
            "a": {"type": "linear", "low": 0, "high": 1},
            "b": {"type": "choice", "values": ["x", "y"]},
        },
    }
    exps = generate_lhs(cfg)
    assert len(exps) == 20
    assert all(isinstance(e["a"], float) for e in exps)
    assert all(e["b"] in ("x", "y") for e in exps)


def test_generate_lhs_reproducible():
    cfg = {
        "n_samples": 10,
        "seed": 123,
        "params": {"a": {"type": "linear", "low": 0, "high": 1}},
    }
    a = generate_lhs(cfg)
    b = generate_lhs(cfg)
    assert [e["a"] for e in a] == [e["a"] for e in b]