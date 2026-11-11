import pytest

import d19

PRICES = {"input": 3.0, "output": 15.0, "cache_read": 0.3}


def test_cost_usd():
    usage = {"input_tokens": 1_000_000, "output_tokens": 200_000, "cache_read_tokens": 500_000}
    assert d19.cost_usd(usage, PRICES) == pytest.approx(3.0 + 3.0 + 0.15)
    assert d19.cost_usd({"input_tokens": 1500}, PRICES) == pytest.approx(0.0045)
    assert d19.cost_usd({}, PRICES) == 0
    assert d19.cost_usd({"cache_read_tokens": 1_000_000}, {"input": 2.0, "output": 8.0}) == pytest.approx(2.0)


def test_budget():
    b = d19.Budget(1.0)
    b.add(0.4)
    b.add(0.6)
    assert b.spent == pytest.approx(1.0) and b.left == pytest.approx(0.0)
    with pytest.raises(d19.BudgetExceeded):
        b.add(0.01)
    assert b.spent == pytest.approx(1.0), "отклонённый расход не учитывается"
    with pytest.raises(ValueError):
        b.add(-1)


def test_cheapest_model():
    models = {
        "большая": {"input": 15.0, "output": 75.0},
        "средняя": {"input": 3.0, "output": 15.0},
        "быстрая": {"input": 1.0, "output": 5.0},
        "дешёвый_вход": {"input": 0.5, "output": 30.0},
    }
    assert d19.cheapest_model(models, {"input_tokens": 1000, "output_tokens": 1000}) == "быстрая"
    assert d19.cheapest_model(models, {"input_tokens": 100_000, "output_tokens": 10}) == "дешёвый_вход"
    with pytest.raises(ValueError):
        d19.cheapest_model({}, {"input_tokens": 1})
