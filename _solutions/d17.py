"""День 17. Надёжность и безопасность агента."""
import json
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeout

_SECRET_WORDS = ("key", "token", "password", "secret")
_OPEN, _CLOSE = "<untrusted_data>", "</untrusted_data>"


class Tracer:
    """Пошаговый журнал работы агента: что вызвали, с чем, что вернулось, сколько заняло."""

    def __init__(self):
        """Завести пустой список records."""
        self.records = []

    def record(self, step, tool, args, result, ms):
        """Добавить запись {"step", "tool", "args", "result", "ms"}.
        В args значения ключей, в имени которых есть key, token, password или secret
        (в любом регистре), заменить на "***". Исходный словарь args не изменять.
        result сохранить как строку, обрезав до 500 символов.
        """
        safe = {k: ("***" if any(w in k.lower() for w in _SECRET_WORDS) else v) for k, v in args.items()}
        self.records.append({"step": step, "tool": tool, "args": safe, "result": str(result)[:500], "ms": ms})

    def to_jsonl(self, path):
        """Записать журнал в файл: одна запись = одна строка JSON, utf-8, кириллица читаемая."""
        with open(path, "w", encoding="utf-8") as f:
            for r in self.records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")


def call_with_timeout(fn, seconds, *args, **kwargs):
    """Вызвать fn(*args, **kwargs). Не успела за seconds секунд -> TimeoutError (встроенный).
    Успела -> вернуть результат. Исключение внутри fn пробросить как есть.
    """
    ex = ThreadPoolExecutor(max_workers=1)
    future = ex.submit(fn, *args, **kwargs)
    try:
        return future.result(timeout=seconds)
    except FutureTimeout:
        raise TimeoutError(f"не уложился в {seconds} с") from None
    finally:
        ex.shutdown(wait=False)


def guard_tool_call(name, args, dangerous, confirm):
    """Решить, можно ли выполнять инструмент. Вернуть True или False.
    dangerous: множество имён опасных инструментов (удаление, отправка, платежи).
    Обычный инструмент -> True, confirm не вызывать.
    Опасный -> спросить человека: вернуть bool(confirm(name, args)).
    """
    if name not in dangerous:
        return True
    return bool(confirm(name, args))


def wrap_untrusted(text):
    """Обернуть чужой текст (веб-страница, письмо, файл) в <untrusted_data>...</untrusted_data>,
    чтобы модель считала его данными, а не командами.
    Если внутри текста уже встречаются эти теги, обезвредить их (заменить на "[tag]"),
    иначе злоумышленник закроет блок раньше времени.
    """
    clean = text.replace(_OPEN, "[tag]").replace(_CLOSE, "[tag]")
    return f"{_OPEN}\n{clean}\n{_CLOSE}"
