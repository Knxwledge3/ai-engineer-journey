import pytest
from fastapi.testclient import TestClient

import d07


@pytest.fixture
def client(tmp_path):
    def llm(messages):
        q = messages[-1]["content"]
        if q == "упади":
            raise RuntimeError("нет связи")
        return f"ответ: {q}"

    return TestClient(d07.create_app(llm, str(tmp_path / "history.db")))


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200 and r.json() == {"status": "ok"}


def test_ask(client):
    r = client.post("/ask", json={"question": "что такое RAG?"})
    assert r.status_code == 200
    assert r.json() == {"answer": "ответ: что такое RAG?"}


def test_ask_validation(client):
    assert client.post("/ask", json={"question": ""}).status_code == 422
    assert client.post("/ask", json={}).status_code == 422


def test_history_newest_first(client):
    for q in ["первый", "второй", "третий"]:
        client.post("/ask", json={"question": q})
    items = client.get("/history").json()
    assert [i["question"] for i in items] == ["третий", "второй", "первый"]
    assert items[0]["answer"] == "ответ: третий" and items[0]["created_at"]
    assert [i["question"] for i in client.get("/history", params={"limit": 2}).json()] == ["третий", "второй"]
    assert client.get("/history", params={"limit": 0}).status_code == 422


def test_model_failure_is_503_and_not_saved(client):
    assert client.post("/ask", json={"question": "упади"}).status_code == 503
    assert client.get("/history").json() == []


def test_history_survives_restart(tmp_path):
    db = str(tmp_path / "h.db")
    TestClient(d07.create_app(lambda m: "a", db)).post("/ask", json={"question": "q"})
    assert len(TestClient(d07.create_app(lambda m: "a", db)).get("/history").json()) == 1
