import d13


def scripted(responses):
    log = []

    def llm(messages, tool_specs):
        log.append({"messages": [dict(m) for m in messages], "specs": tool_specs})
        return responses[min(len(log) - 1, len(responses) - 1)]

    return llm, log


def call(name, args, id="c1"):
    return {"text": None, "tool_calls": [{"id": id, "name": name, "args": args}]}


TOOLS = {
    "add": {"fn": lambda a, b: a + b, "description": "Сложить два числа", "schema": {"type": "object"}},
    "boom": {"fn": lambda: 1 / 0, "description": "Всегда падает", "schema": {"type": "object"}},
}


def test_no_tools_needed():
    llm, log = scripted([{"text": "Привет!", "tool_calls": []}])
    out = d13.run_agent("привет", llm, TOOLS, system="Ты помощник")
    assert out == {"answer": "Привет!", "steps": [], "stopped": "final"}
    assert log[0]["messages"][0] == {"role": "system", "content": "Ты помощник"}
    assert log[0]["messages"][-1] == {"role": "user", "content": "привет"}
    assert {s["name"] for s in log[0]["specs"]} == {"add", "boom"}
    assert all("description" in s for s in log[0]["specs"])


def test_tool_result_goes_back_to_model():
    llm, log = scripted([call("add", {"a": 2, "b": 2}), {"text": "Будет 4", "tool_calls": []}])
    out = d13.run_agent("сколько 2+2?", llm, TOOLS)
    assert out["answer"] == "Будет 4" and out["stopped"] == "final"
    assert out["steps"] == [{"tool": "add", "args": {"a": 2, "b": 2}, "result": 4}]
    assert len(log) == 2
    tool_msgs = [m for m in log[1]["messages"] if m["role"] == "tool"]
    assert len(tool_msgs) == 1
    assert tool_msgs[0]["content"] == "4" and tool_msgs[0]["tool_call_id"] == "c1" and tool_msgs[0]["name"] == "add"
    assert any(m["role"] == "assistant" and m.get("tool_calls") for m in log[1]["messages"])


def test_unknown_tool_and_tool_error_do_not_crash():
    llm, log = scripted([call("нет_такого", {}), call("boom", {}, id="c2"), {"text": "не вышло", "tool_calls": []}])
    out = d13.run_agent("сделай", llm, TOOLS)
    assert out["stopped"] == "final" and out["answer"] == "не вышло"
    assert out["steps"][0]["result"] == "error: unknown tool нет_такого"
    assert str(out["steps"][1]["result"]).startswith("error:")
    last_tool = [m for m in log[2]["messages"] if m["role"] == "tool"][-1]
    assert last_tool["content"].startswith("error:"), "модель должна увидеть ошибку и иметь шанс исправиться"


def test_two_tools_in_one_turn():
    both = {"text": None, "tool_calls": [
        {"id": "a", "name": "add", "args": {"a": 1, "b": 2}},
        {"id": "b", "name": "add", "args": {"a": 10, "b": 20}},
    ]}
    llm, log = scripted([both, {"text": "3 и 30", "tool_calls": []}])
    out = d13.run_agent("посчитай", llm, TOOLS)
    assert [s["result"] for s in out["steps"]] == [3, 30]
    assert [m["tool_call_id"] for m in log[1]["messages"] if m["role"] == "tool"] == ["a", "b"]


def test_max_steps_stops_infinite_loop():
    llm, log = scripted([call("add", {"a": 1, "b": 1})])
    out = d13.run_agent("зациклись", llm, TOOLS, max_steps=3)
    assert out["stopped"] == "max_steps"
    assert len(log) == 3 and len(out["steps"]) == 3
