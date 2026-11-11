import pytest

import d14


def test_calculator_math():
    assert d14.calculator("2+2*3") == 8
    assert d14.calculator("(1 + 2) / 4") == pytest.approx(0.75)
    assert d14.calculator("-5 + 10.5") == pytest.approx(5.5)


@pytest.mark.parametrize("bad", ["__import__('os').system('dir')", "open('x')", "a + 1", "2 +", "1/0", "'a' * 3"])
def test_calculator_rejects_everything_else(bad):
    with pytest.raises(ValueError):
        d14.calculator(bad)


def test_conversation_trims_but_keeps_system():
    c = d14.Conversation(max_messages=3, system="Ты помощник")
    for i in range(5):
        c.add("user" if i % 2 == 0 else "assistant", f"m{i}")
    msgs = c.messages()
    assert msgs[0] == {"role": "system", "content": "Ты помощник"}
    assert [m["content"] for m in msgs[1:]] == ["m2", "m3", "m4"]
    msgs.append("мусор")
    assert len(c.messages()) == 4, "messages() возвращает копию"


def test_conversation_without_system():
    c = d14.Conversation(max_messages=2)
    c.add("user", "привет")
    assert c.messages() == [{"role": "user", "content": "привет"}]


def test_tool_spec():
    def get_weather(city: str, days: int = 1, metric: bool = True, note=None):
        """Узнать погоду в городе.

        Длинное описание, которое в спецификацию не идёт.
        """

    spec = d14.tool_spec(get_weather)
    assert spec["name"] == "get_weather"
    assert spec["description"] == "Узнать погоду в городе."
    p = spec["parameters"]
    assert p["type"] == "object"
    assert p["properties"] == {
        "city": {"type": "string"}, "days": {"type": "integer"},
        "metric": {"type": "boolean"}, "note": {"type": "string"},
    }
    assert p["required"] == ["city"]


def test_tool_spec_no_docstring():
    def price(amount: float):
        pass

    spec = d14.tool_spec(price)
    assert spec["description"] == ""
    assert spec["parameters"]["properties"] == {"amount": {"type": "number"}}
