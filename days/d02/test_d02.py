import pytest

import d02


def test_load_settings_ok():
    env = {"LLM_API_KEY": " sk-123 ", "LLM_MODEL": "some-model", "OTHER": "x"}
    assert d02.load_settings(env) == {"api_key": "sk-123", "model": "some-model"}


@pytest.mark.parametrize("env, missing", [
    ({"LLM_MODEL": "m"}, "LLM_API_KEY"),
    ({"LLM_API_KEY": "k"}, "LLM_MODEL"),
    ({"LLM_API_KEY": "  ", "LLM_MODEL": "m"}, "LLM_API_KEY"),
])
def test_load_settings_missing(env, missing):
    with pytest.raises(RuntimeError) as e:
        d02.load_settings(env)
    assert missing in str(e.value)


def test_mask():
    assert d02.mask("sk-ant-1234567890abcd") == "sk-a...abcd"
    assert d02.mask("short") == "***"
    assert "1234567890" not in d02.mask("sk-ant-1234567890abcd")


def test_ask_builds_messages():
    seen = []

    def llm(messages):
        seen.append(messages)
        return "  Привет!\n"

    assert d02.ask("Скажи привет", llm, system="Отвечай кратко") == "Привет!"
    assert seen[0] == [
        {"role": "system", "content": "Отвечай кратко"},
        {"role": "user", "content": "Скажи привет"},
    ]
    d02.ask("Ещё раз", llm)
    assert seen[1] == [{"role": "user", "content": "Ещё раз"}]


def test_ask_empty_prompt_does_not_call_model():
    def llm(messages):
        raise AssertionError("модель не должна вызываться")

    with pytest.raises(ValueError):
        d02.ask("   ", llm)
