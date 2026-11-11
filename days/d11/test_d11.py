import pytest

import d11


@pytest.mark.parametrize("text, expected", [
    ("/ask что такое RAG", ("ask", "что такое RAG")),
    ("/start@MyBot", ("start", "")),
    ("/HELP", ("help", "")),
    ("  /ask@MyBot   привет  ", ("ask", "привет")),
    ("просто текст", ("", "просто текст")),
    ("  текст с / слэшем ", ("", "текст с / слэшем")),
])
def test_parse_command(text, expected):
    assert d11.parse_command(text) == expected


def test_split_message():
    text = "\n".join(f"строка номер {i}" for i in range(400))
    parts = d11.split_message(text, limit=500)
    assert len(parts) > 1
    assert all(0 < len(p) <= 500 for p in parts)
    assert "".join(parts) == text
    assert d11.split_message("коротко") == ["коротко"]
    assert d11.split_message("") == []
    assert d11.split_message("a" * 10, limit=4) == ["aaaa", "aaaa", "aa"]
    with pytest.raises(ValueError):
        d11.split_message("abc", limit=0)


def test_digest_empty_does_not_call_model():
    def llm(messages):
        raise AssertionError("модель не вызываем")

    assert d11.build_digest([], llm) == "Сегодня новостей нет."


def test_digest():
    items = [{"title": f"Новость {i}", "url": f"https://news/{i}"} for i in range(1, 8)]
    seen = []

    def llm(messages):
        seen.append("\n".join(m["content"] for m in messages))
        return "Главное за день: вышли новые модели.\n"

    out = d11.build_digest(items, llm, max_items=5)
    assert len(seen) == 1
    assert "Новость 5" in seen[0] and "Новость 6" not in seen[0]
    assert out.startswith("Главное за день: вышли новые модели.\n\nИсточники:\n")
    assert out.split("Источники:\n")[1].split("\n") == [f"https://news/{i}" for i in range(1, 6)]
