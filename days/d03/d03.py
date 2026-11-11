"""День 3. Промпты как код и первый eval."""
import string

def build_prompt(template, **values):
    """Подставить значения в шаблон вида "Переведи на {lang}: {text}".
    Не хватает переменной -> KeyError с её именем. Лишние значения игнорировать.
    """
    raise NotImplementedError('напиши меня')

def few_shot(examples, query):
    """Собрать few-shot промпт. examples: список пар (вход, выход).
    Формат строго такой (между примерами пустая строка, в конце нет перевода строки):

    Вход: <вход1>
    Выход: <выход1>

    Вход: <query>
    Выход:
    """
    raise NotImplementedError('напиши меня')

def run_eval(cases, fn):
    """Прогнать набор проверок. cases: список {"input": ..., "expected": строка}.
    fn(input) -> строка. Сравнение без учёта регистра и пробелов по краям.
    Если fn упала на примере, это провал примера, а не падение всего прогона.
    Вернуть {"total": n, "passed": m, "accuracy": m/n (0.0 при n == 0),
             "failed": [{"input", "expected", "got"}]}; для упавших got = "error: <текст>".
    """
    raise NotImplementedError('напиши меня')
