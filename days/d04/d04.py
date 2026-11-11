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

    @model_validator(mode='after')
    def check_salary(self):
        """Проверить, что salary_min <= salary_max."""
        raise NotImplementedError('напиши меня')

def parse_json_block(text):
    """Достать JSON-объект из ответа модели и вернуть словарь.
    Модель может обернуть JSON в ```json ... ``` или добавить слова до и после.
    JSON не найден или сломан -> ValueError.
    """
    raise NotImplementedError('напиши меня')

def extract(text, llm, max_attempts=3):
    """Извлечь Vacancy из текста вакансии. llm(messages) -> строка.
    Если ответ не парсится или не проходит валидацию, спросить модель ещё раз,
    добавив в messages её прошлый ответ и текст ошибки. После max_attempts неудач -> ValueError.
    """
    raise NotImplementedError('напиши меня')
