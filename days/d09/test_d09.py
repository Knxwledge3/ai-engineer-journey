import pytest

import d09


class FakeRetriever:
    def __init__(self, table):
        self.table = table

    def search(self, query, k=3):
        return self.table.get(query, [])[:k]


HITS = [
    {"text": "Отпуск 24 дня.", "source": "hr.md", "score": 0.82},
    {"text": "Перенос отпуска за 14 дней.", "source": "hr.md", "score": 0.41},
    {"text": "Зарплата 5 и 20 числа.", "source": "pay.md", "score": 0.12},
]


def test_grounded_answer_filters_weak_chunks():
    seen = []

    def llm(messages):
        seen.append("\n".join(m["content"] for m in messages))
        return "24 дня"

    out = d09.answer_guarded("отпуск?", FakeRetriever({"отпуск?": HITS}), llm, min_score=0.3)
    assert out == {"answer": "24 дня", "sources": ["hr.md"], "grounded": True}
    assert "Отпуск 24 дня." in seen[0] and "отпуск?" in seen[0]
    assert "Зарплата" not in seen[0], "слабые куски в промпт не попадают"


def test_says_dont_know_without_calling_model():
    def llm(messages):
        raise AssertionError("если опереться не на что, модель не вызываем")

    weak = [{"text": "что-то", "source": "x.md", "score": 0.05}]
    for table in ({"курс тенге?": weak}, {}):
        out = d09.answer_guarded("курс тенге?", FakeRetriever(table), llm, min_score=0.3)
        assert out["grounded"] is False and out["sources"] == []
        assert out["answer"].startswith("Не знаю")


def test_threshold_is_inclusive():
    hit = [{"text": "t", "source": "s.md", "score": 0.3}]
    assert d09.answer_guarded("q", FakeRetriever({"q": hit}), lambda m: "a", min_score=0.3)["grounded"] is True


def test_recall_at_k():
    r = FakeRetriever({
        "q1": [{"text": "", "source": "a.md", "score": 0.9}, {"text": "", "source": "b.md", "score": 0.5}],
        "q2": [{"text": "", "source": "c.md", "score": 0.9}, {"text": "", "source": "a.md", "score": 0.5}],
        "q3": [],
    })
    cases = [
        {"question": "q1", "expected_source": "a.md"},
        {"question": "q2", "expected_source": "a.md"},
        {"question": "q3", "expected_source": "a.md"},
        {"question": "q1", "expected_source": "b.md"},
    ]
    assert d09.recall_at_k(cases, r, k=2) == pytest.approx(0.75)
    assert d09.recall_at_k(cases, r, k=1) == pytest.approx(0.25)
    assert d09.recall_at_k([], r) == 0.0
