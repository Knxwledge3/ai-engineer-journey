import json

import pytest

import diag


def test_1_total_by_category():
    rows = [{"cat": "еда", "amount": 1000}, {"cat": "такси", "amount": 500}, {"cat": "еда", "amount": 250.5}]
    assert diag.total_by_category(rows) == {"еда": 1250.5, "такси": 500}
    assert diag.total_by_category([]) == {}


def test_2_parse_kv():
    assert diag.parse_kv("model = haiku; temp=0.2 ;; lang=ru") == {"model": "haiku", "temp": "0.2", "lang": "ru"}
    assert diag.parse_kv("") == {}
    with pytest.raises(ValueError):
        diag.parse_kv("a=1;oops")


def test_3_to_float():
    assert diag.to_float("1 234,5") == 1234.5
    assert diag.to_float("42") == 42.0
    assert diag.to_float(" 3.14 ") == 3.14
    assert diag.to_float("abc") is None
    assert diag.to_float("") is None
    assert diag.to_float(None) is None


def test_4_load_json(tmp_path):
    assert diag.load_json(tmp_path / "нет.json", default=[]) == []
    bad = tmp_path / "bad.json"
    bad.write_text("{сломано", encoding="utf-8")
    assert diag.load_json(bad, default={"x": 1}) == {"x": 1}
    good = tmp_path / "good.json"
    good.write_text(json.dumps({"город": "Алматы"}, ensure_ascii=False), encoding="utf-8")
    assert diag.load_json(good, default=None) == {"город": "Алматы"}


def test_5_budget():
    b = diag.Budget(100)
    b.spend(30)
    assert b.left == 70
    with pytest.raises(ValueError):
        b.spend(80)
    with pytest.raises(ValueError):
        b.spend(-1)
    assert b.left == 70
    b.spend(70)
    assert b.left == 0


def test_6_retry():
    calls = []

    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise ConnectionError("сеть")
        return "ok"

    assert diag.retry(flaky, attempts=3) == "ok"
    assert len(calls) == 3

    calls2 = []

    def broken():
        calls2.append(1)
        raise KeyError("всегда")

    with pytest.raises(KeyError):
        diag.retry(broken, attempts=4)
    assert len(calls2) == 4


def test_7_top_k():
    scores = {"c": 0.5, "b": 0.9, "a": 0.5, "d": 0.1}
    assert diag.top_k(scores, 3) == ["b", "a", "c"]
    assert diag.top_k(scores, 10) == ["b", "a", "c", "d"]
    assert diag.top_k(scores, 0) == []


def test_8_chat_turn():
    history = [{"role": "system", "content": "Ты помощник"}]
    llm = lambda msgs: f"ответ на {msgs[-1]['content']} ({len(msgs)})"  # noqa: E731
    reply, new = diag.chat_turn(history, "привет", llm)
    assert reply == "ответ на привет (2)"
    assert len(history) == 1, "исходную историю менять нельзя"
    assert new[-2] == {"role": "user", "content": "привет"}
    assert new[-1] == {"role": "assistant", "content": reply}
    assert len(new) == 3
