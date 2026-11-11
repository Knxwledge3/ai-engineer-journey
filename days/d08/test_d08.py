import d08

VOCAB = ["отпуск", "дней", "зарплата", "выплата", "ремонт", "смета"]


def embed(text):
    t = text.lower()
    return [t.count(w) for w in VOCAB]


def make():
    r = d08.Retriever(embed)
    r.add("1", "Отпуск составляет 24 календарных дней в году.", "hr.md")
    r.add("2", "Выплата зарплаты: зарплата приходит 5 и 20 числа.", "pay.md")
    r.add("3", "Смета на ремонт согласуется до начала работ. Ремонт без сметы запрещён.", "build.md")
    r.add("4", "Перенос отпуска согласуется за 14 дней.", "hr.md")
    return r


def test_embed_called_once_per_added_text():
    calls = []

    def counting(text):
        calls.append(text)
        return embed(text)

    r = d08.Retriever(counting)
    r.add("1", "отпуск", "a.md")
    r.add("2", "смета", "b.md")
    assert len(calls) == 2
    r.search("отпуск")
    assert len(calls) == 3, "при поиске считаем вектор только для запроса"


def test_search_order_and_shape():
    hits = make().search("Когда приходит зарплата?", k=2)
    assert len(hits) == 2
    assert hits[0]["id"] == "2" and hits[0]["source"] == "pay.md"
    assert set(hits[0]) >= {"id", "text", "source", "score"}
    assert hits[0]["score"] >= hits[1]["score"]
    assert d08.Retriever(embed).search("что угодно") == []


def test_answer_uses_context_and_returns_sources():
    seen = []

    def llm(messages):
        seen.append("\n".join(m["content"] for m in messages))
        return "24 дня"

    out = d08.answer("Сколько дней отпуск?", make(), llm, k=2)
    assert out["answer"] == "24 дня"
    assert out["sources"] == ["hr.md"], "источники без повторов"
    assert "24 календарных" in seen[0] and "Сколько дней отпуск?" in seen[0]
    assert "зарплата приходит" not in seen[0], "в промпт идут только найденные k кусков"


def test_answer_sources_order():
    out = d08.answer("смета на ремонт и отпуск", make(), lambda m: "ок", k=3)
    assert out["sources"][0] == "build.md"
    assert len(out["sources"]) == len(set(out["sources"]))
