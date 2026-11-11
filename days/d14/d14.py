"""День 14. Инструменты и память диалога."""
import ast
import inspect
import operator

def calculator(expression):
    """Безопасно посчитать выражение из чисел, скобок и + - * /. Вернуть число.
    Нельзя использовать eval: модель может прислать что угодно.
    Всё, что не число и не эти операции (имена, вызовы функций, **), -> ValueError.
    Деление на ноль -> ValueError.
    """
    raise NotImplementedError('напиши меня')

class Conversation:
    """Память диалога с ограничением длины, чтобы контекст не рос бесконечно."""

    def __init__(self, max_messages=20, system=None):
        """max_messages: сколько последних сообщений хранить (системное не считается)."""
        raise NotImplementedError('напиши меня')

    def add(self, role, content):
        """Добавить сообщение {"role", "content"}; лишние старые сообщения отбросить."""
        raise NotImplementedError('напиши меня')

    def messages(self):
        """Вернуть список для модели: системное сообщение (если задано) всегда первым,
        затем последние max_messages сообщений. Возвращать копию списка.
        """
        raise NotImplementedError('напиши меня')

def tool_spec(fn):
    """Построить описание инструмента для модели из обычной функции Python:
    {"name": имя функции,
     "description": первая строка докстринга ("" если его нет),
     "parameters": {"type": "object",
                    "properties": {параметр: {"type": ...}},
                    "required": [параметры без значения по умолчанию]}}
    Типы из аннотаций: str -> "string", int -> "integer", float -> "number", bool -> "boolean",
    без аннотации или другой тип -> "string".
    """
    raise NotImplementedError('напиши меня')
