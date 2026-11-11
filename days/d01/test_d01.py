import pytest

import d01


def test_add_card_returns_new_list():
    cards = []
    new = d01.add_card(cards, " Документация ", " https://docs.python.org ", ["Python", "python", " Docs "])
    assert cards == [], "исходный список менять нельзя"
    assert new == [{"name": "Документация", "url": "https://docs.python.org", "tags": ["python", "docs"]}]


def test_add_card_no_tags():
    assert d01.add_card([], "a", "http://a")[0]["tags"] == []


def test_add_card_rejects_empty_and_duplicates():
    cards = d01.add_card([], "FastAPI", "https://fastapi.tiangolo.com", ["web"])
    with pytest.raises(ValueError):
        d01.add_card(cards, "  ", "http://x")
    with pytest.raises(ValueError):
        d01.add_card(cards, "x", "")
    with pytest.raises(ValueError):
        d01.add_card(cards, "fastapi", "http://other")


def test_filter_by_tag():
    cards = d01.add_card([], "A", "http://a", ["rag", "python"])
    cards = d01.add_card(cards, "B", "http://b", ["agents"])
    cards = d01.add_card(cards, "C", "http://c", ["RAG"])
    assert [c["name"] for c in d01.filter_by_tag(cards, " Rag ")] == ["A", "C"]
    assert d01.filter_by_tag(cards, "нет такого") == []


def test_save_and_load(tmp_path):
    path = tmp_path / "cards.json"
    assert d01.load_cards(path) == []
    cards = d01.add_card([], "Курс по агентам", "http://x", ["агенты"])
    d01.save_cards(cards, path)
    assert "Курс по агентам" in path.read_text(encoding="utf-8"), "кириллица должна быть читаемой в файле"
    assert d01.load_cards(path) == cards
