import pytest
from fastapi.testclient import TestClient

import d12



@pytest.fixture
def setup():
    calls = []

    def agent(text):
        calls.append(text)
        if text == "упади":
            raise RuntimeError("сбой")
        return f"сделано: {text}"

    return TestClient(d12.create_webhook_app(agent, "s3cret"), raise_server_exceptions=False), calls


def test_ok(setup):
    client, calls = setup
    r = client.post("/hook", json={"text": "составь сводку"}, headers={"X-Webhook-Secret": "s3cret"})
    assert r.status_code == 200 and r.json() == {"answer": "сделано: составь сводку"}
    assert calls == ["составь сводку"]


@pytest.mark.parametrize("headers", [{}, {"X-Webhook-Secret": "wrong"}, {"X-Webhook-Secret": ""}])
def test_unauthorized_never_reaches_agent(setup, headers):
    client, calls = setup
    assert client.post("/hook", json={"text": "привет"}, headers=headers).status_code == 401
    assert calls == []


def test_validation(setup):
    client, calls = setup
    assert client.post("/hook", json={"text": ""}, headers={"X-Webhook-Secret": "s3cret"}).status_code == 422
    assert calls == []


def test_agent_failure_is_500(setup):
    client, _ = setup
    assert client.post("/hook", json={"text": "упади"}, headers={"X-Webhook-Secret": "s3cret"}).status_code == 500
