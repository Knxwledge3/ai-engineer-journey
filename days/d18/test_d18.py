import d18


def agent(text):
    if text == "погода":
        return {"answer": "В Алматы +5", "steps": [{"tool": "weather"}]}
    if text == "удали":
        return {"answer": "Удалил", "steps": [{"tool": "search"}, {"tool": "delete_file"}]}
    if text == "цикл":
        return {"answer": "", "steps": [{"tool": "search"}] * 6}
    if text == "упади":
        raise RuntimeError("нет сети")
    return {"answer": "Не знаю", "steps": []}


SCENARIOS = [
    {"name": "погода", "input": "погода", "expect_tools": ["weather"], "expect_in_answer": ["алматы"], "max_steps": 2},
    {"name": "запрет удаления", "input": "удали", "expect_tools": ["search"], "forbid_tools": ["delete_file"]},
    {"name": "зацикливание", "input": "цикл", "max_steps": 3, "expect_in_answer": ["готово"]},
    {"name": "падение", "input": "упади", "expect_tools": ["weather"]},
    {"name": "без проверок", "input": "привет"},
]


def test_report():
    r = d18.run_scenarios(SCENARIOS, agent)
    assert r["total"] == 5 and r["passed"] == 2
    by = {x["name"]: x for x in r["results"]}
    assert [x["name"] for x in r["results"]] == [s["name"] for s in SCENARIOS]
    assert by["погода"] == {"name": "погода", "passed": True, "reasons": []}
    assert by["без проверок"]["passed"] is True
    assert by["запрет удаления"]["passed"] is False and len(by["запрет удаления"]["reasons"]) == 1
    assert "delete_file" in by["запрет удаления"]["reasons"][0]
    assert len(by["зацикливание"]["reasons"]) == 2, "по одной причине на каждую нарушенную проверку"
    assert by["падение"]["passed"] is False and "нет сети" in by["падение"]["reasons"][0]


def test_missing_expected_tool():
    r = d18.run_scenarios([{"name": "x", "input": "привет", "expect_tools": ["weather", "search"]}], agent)
    assert r["passed"] == 0 and len(r["results"][0]["reasons"]) == 2


def test_empty():
    assert d18.run_scenarios([], agent) == {"total": 0, "passed": 0, "results": []}
