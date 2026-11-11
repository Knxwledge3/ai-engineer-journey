"""День 4. Структурированный вывод: из текста в проверенные данные."""
import json
import re
from typing import Optional

from pydantic import BaseModel, model_validator


class Vacancy(BaseModel):
    """Вакансия. Поля: title (обязательное), company, salary_min, salary_max,
    skills (список строк, по умолчанию пустой), remote (по умолчанию False).
    Если заданы обе границы зарплаты и salary_min > salary_max -> ошибка валидации.
    """

    title: str
    company: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    skills: list[str] = []
    remote: bool = False

    @model_validator(mode="after")
    def check_salary(self):
        """Проверить, что salary_min <= salary_max."""
        if self.salary_min is not None and self.salary_max is not None and self.salary_min > self.salary_max:
            raise ValueError("salary_min больше salary_max")
        return self


def parse_json_block(text):
    """Достать JSON-объект из ответа модели и вернуть словарь.
    Модель может обернуть JSON в ```json ... ``` или добавить слова до и после.
    JSON не найден или сломан -> ValueError.
    """
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    raw = m.group(1) if m else text
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("JSON не найден")
    try:
        data = json.loads(raw[start : end + 1])
    except json.JSONDecodeError as e:
        raise ValueError(f"сломанный JSON: {e}") from e
    return data


def extract(text, llm, max_attempts=3):
    """Извлечь Vacancy из текста вакансии. llm(messages) -> строка.
    Если ответ не парсится или не проходит валидацию, спросить модель ещё раз,
    добавив в messages её прошлый ответ и текст ошибки. После max_attempts неудач -> ValueError.
    """
    messages = [
        {"role": "system", "content": "Верни только JSON с полями title, company, salary_min, salary_max, skills, remote."},
        {"role": "user", "content": text},
    ]
    error = None
    for _ in range(max_attempts):
        raw = llm(list(messages))
        try:
            return Vacancy(**parse_json_block(raw))
        except ValueError as e:
            error = e
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": f"Ошибка: {e}. Верни только исправленный JSON."})
    raise ValueError(f"не удалось извлечь данные: {error}")
