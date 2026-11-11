import pytest

import d06


def test_cosine():
    assert d06.cosine([1, 0], [1, 0]) == pytest.approx(1.0)
    assert d06.cosine([1, 0], [0, 1]) == pytest.approx(0.0)
    assert d06.cosine([1, 0], [-1, 0]) == pytest.approx(-1.0)
    assert d06.cosine([1, 2, 3], [2, 4, 6]) == pytest.approx(1.0)
    assert d06.cosine([0, 0], [1, 1]) == 0.0
    with pytest.raises(ValueError):
        d06.cosine([1, 2], [1, 2, 3])


def test_top_k():
    items = [("кот", [1, 0, 0]), ("пёс", [0.9, 0.1, 0]), ("банк", [0, 0, 1]), ("кредит", [0, 0.2, 0.9])]
    got = d06.top_k([1, 0, 0], items, k=2)
    assert [i for i, _ in got] == ["кот", "пёс"]
    assert got[0][1] == pytest.approx(1.0)
    assert len(d06.top_k([0, 0, 1], items, k=10)) == 4
    assert d06.top_k([0, 0, 1], items, k=1)[0][0] == "банк"


@pytest.mark.parametrize("n, size, overlap", [(1000, 300, 50), (300, 300, 50), (301, 300, 50), (10, 4, 1), (7, 100, 10)])
def test_chunk_text_properties(n, size, overlap):
    text = "".join(chr(1040 + i % 32) for i in range(n))
    chunks = d06.chunk_text(text, size=size, overlap=overlap)
    assert all(0 < len(c) <= size for c in chunks)
    for prev, nxt in zip(chunks, chunks[1:]):
        assert nxt.startswith(prev[-overlap:]), "следующий кусок начинается с хвоста предыдущего"
        assert len(nxt) > overlap, "последний кусок не должен быть пустым повтором"
    assert chunks[0] + "".join(c[overlap:] for c in chunks[1:]) == text


def test_chunk_text_edges():
    assert d06.chunk_text("") == []
    assert d06.chunk_text("коротко", size=100, overlap=10) == ["коротко"]
    with pytest.raises(ValueError):
        d06.chunk_text("abc", size=10, overlap=10)
