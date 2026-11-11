import pytest

import d04

GOOD = '{"title": "AI Engineer", "company": "Acme", "salary_min": 800000, "salary_max": 1200000, "skills": ["Python", "RAG"], "remote": true}'


def test_vacancy_defaults_and_validation():
    v = d04.Vacancy(title="Аналитик")
    assert (v.company, v.salary_min, v.skills, v.remote) == (None, None, [], False)
    with pytest.raises(ValueError):
        d04.Vacancy(title="x", salary_min=500, salary_max=100)
    with pytest.raises(ValueError):
        d04.Vacancy(company="без названия")


def test_parse_json_block_variants():
    assert d04.parse_json_block(GOOD)["title"] == "AI Engineer"
    assert d04.parse_json_block(f"Вот результат:\n```json\n{GOOD}\n```\nГотово.")["company"] == "Acme"
    assert d04.parse_json_block(f"Конечно! {GOOD} Надеюсь, помог.")["remote"] is True
    for bad in ("никакого json тут нет", '{"title": "x", }'):
        with pytest.raises(ValueError):
            d04.parse_json_block(bad)


def test_extract_first_try():
    v = d04.extract("текст вакансии", lambda m: GOOD)
    assert isinstance(v, d04.Vacancy)
    assert v.skills == ["Python", "RAG"] and v.salary_max == 1200000


def test_extract_retries_with_error_feedback():
    answers = ["извините, не могу", '{"title": "x", "salary_min": 9, "salary_max": 1}', GOOD]
    sizes = []

    def llm(messages):
        sizes.append(len(messages))
        return answers[len(sizes) - 1]

    v = d04.extract("текст вакансии", llm)
    assert v.title == "AI Engineer"
    assert len(sizes) == 3
    assert sizes[0] < sizes[1] < sizes[2], "при повторе модель должна видеть свой прошлый ответ и ошибку"


def test_extract_gives_up():
    calls = []

    def llm(messages):
        calls.append(1)
        return "не json"

    with pytest.raises(ValueError):
        d04.extract("текст", llm, max_attempts=2)
    assert len(calls) == 2
