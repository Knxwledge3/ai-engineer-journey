"""День 14. Инструменты и память диалога."""
import ast
import inspect
import operator

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


def calculator(expression):
    """Безопасно посчитать выражение из чисел, скобок и + - * /. Вернуть число.
    Нельзя использовать eval: модель может прислать что угодно.
    Всё, что не число и не эти операции (имена, вызовы функций, **), -> ValueError.
    Деление на ноль -> ValueError.
    """

    def ev(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            v = ev(node.operand)
            return -v if isinstance(node.op, ast.USub) else v
        raise ValueError("недопустимое выражение")

    try:
        return ev(ast.parse(expression, mode="eval").body)
    except (SyntaxError, ZeroDivisionError) as e:
        raise ValueError(str(e)) from e


class Conversation:
    """Память диалога с ограничением длины, чтобы контекст не рос бесконечно."""

    def __init__(self, max_messages=20, system=None):
        """max_messages: сколько последних сообщений хранить (системное не считается)."""
        self.max_messages = max_messages
        self.system = system
        self._items = []

    def add(self, role, content):
        """Добавить сообщение {"role", "content"}; лишние старые сообщения отбросить."""
        self._items.append({"role": role, "content": content})
        self._items = self._items[-self.max_messages :]

    def messages(self):
        """Вернуть список для модели: системное сообщение (если задано) всегда первым,
        затем последние max_messages сообщений. Возвращать копию списка.
        """
        head = [{"role": "system", "content": self.system}] if self.system else []
        return head + list(self._items)


_TYPES = {str: "string", int: "integer", float: "number", bool: "boolean"}


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
    doc = (inspect.getdoc(fn) or "").split("\n")[0]
    props, required = {}, []
    for name, p in inspect.signature(fn).parameters.items():
        props[name] = {"type": _TYPES.get(p.annotation, "string")}
        if p.default is inspect.Parameter.empty:
            required.append(name)
    return {
        "name": fn.__name__,
        "description": doc,
        "parameters": {"type": "object", "properties": props, "required": required},
    }
