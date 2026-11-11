import pytest

import d03


def test_build_prompt():
    assert d03.build_prompt("Переведи на {lang}: {text}", lang="английский", text="привет", extra=1) == \
        "Переведи на английский: привет"
    with pytest.raises(KeyError) as e:
        d03.build_prompt("Переведи на {lang}: {text}", text="привет")
    assert "lang" in str(e.value)


def test_few_shot_exact_format():
    got = d03.few_shot([("отлично", "позитив"), ("ужасно", "негатив")], "нормально")
    assert got == "Вход: отлично\nВыход: позитив\n\nВход: ужасно\nВыход: негатив\n\nВход: нормально\nВыход:"
    assert d03.few_shot([], "x") == "Вход: x\nВыход:"


def test_run_eval_counts():
    cases = [
        {"input": "отлично", "expected": "позитив"},
        {"input": "ужасно", "expected": "негатив"},
        {"input": "супер", "expected": "позитив"},
        {"input": "бум", "expected": "негатив"},
    ]

    def fn(text):
        if text == "бум":
            raise RuntimeError("упало")
        return " Позитив " if text in ("отлично", "ужасно") else "позитив"

    r = d03.run_eval(cases, fn)
    assert (r["total"], r["passed"]) == (4, 2)
    assert r["accuracy"] == 0.5
    assert [f["input"] for f in r["failed"]] == ["ужасно", "бум"]
    assert r["failed"][0]["expected"] == "негатив"
    assert str(r["failed"][1]["got"]).startswith("error:")


def test_run_eval_empty():
    assert d03.run_eval([], lambda x: x) == {"total": 0, "passed": 0, "accuracy": 0.0, "failed": []}
