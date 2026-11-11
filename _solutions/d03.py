"""День 3. Промпты как код и первый eval."""
import string


def build_prompt(template, **values):
    """Подставить значения в шаблон вида "Переведи на {lang}: {text}".
    Не хватает переменной -> KeyError с её именем. Лишние значения игнорировать.
    """
    needed = [f for _, f, _, _ in string.Formatter().parse(template) if f]
    for name in needed:
        if name not in values:
            raise KeyError(name)
    return template.format(**values)


def few_shot(examples, query):
    """Собрать few-shot промпт. examples: список пар (вход, выход).
    Формат строго такой (между примерами пустая строка, в конце нет перевода строки):

    Вход: <вход1>
    Выход: <выход1>

    Вход: <query>
    Выход:
    """
    blocks = [f"Вход: {i}\nВыход: {o}" for i, o in examples]
    blocks.append(f"Вход: {query}\nВыход:")
    return "\n\n".join(blocks)


def run_eval(cases, fn):
    """Прогнать набор проверок. cases: список {"input": ..., "expected": строка}.
    fn(input) -> строка. Сравнение без учёта регистра и пробелов по краям.
    Если fn упала на примере, это провал примера, а не падение всего прогона.
    Вернуть {"total": n, "passed": m, "accuracy": m/n (0.0 при n == 0),
             "failed": [{"input", "expected", "got"}]}; для упавших got = "error: <текст>".
    """
    failed = []
    for c in cases:
        try:
            got = fn(c["input"])
        except Exception as e:  # noqa: BLE001
            got = f"error: {e}"
        if str(got).strip().lower() != c["expected"].strip().lower():
            failed.append({"input": c["input"], "expected": c["expected"], "got": got})
    total = len(cases)
    passed = total - len(failed)
    return {"total": total, "passed": passed, "accuracy": passed / total if total else 0.0, "failed": failed}
