"""День 17. Надёжность и безопасность агента."""
import json
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeout
_OPEN, _CLOSE = ('<untrusted_data>', '</untrusted_data>')

class Tracer:
    """Пошаговый журнал работы агента: что вызвали, с чем, что вернулось, сколько заняло."""

    def __init__(self):
        """Завести пустой список records."""
        raise NotImplementedError('напиши меня')

    def record(self, step, tool, args, result, ms):
        """Добавить запись {"step", "tool", "args", "result", "ms"}.
        В args значения ключей, в имени которых есть key, token, password или secret
        (в любом регистре), заменить на "***". Исходный словарь args не изменять.
        result сохранить как строку, обрезав до 500 символов.
        """
        raise NotImplementedError('напиши меня')

    def to_jsonl(self, path):
        """Записать журнал в файл: одна запись = одна строка JSON, utf-8, кириллица читаемая."""
        raise NotImplementedError('напиши меня')

def call_with_timeout(fn, seconds, *args, **kwargs):
    """Вызвать fn(*args, **kwargs). Не успела за seconds секунд -> TimeoutError (встроенный).
    Успела -> вернуть результат. Исключение внутри fn пробросить как есть.
    """
    raise NotImplementedError('напиши меня')

def guard_tool_call(name, args, dangerous, confirm):
    """Решить, можно ли выполнять инструмент. Вернуть True или False.
    dangerous: множество имён опасных инструментов (удаление, отправка, платежи).
    Обычный инструмент -> True, confirm не вызывать.
    Опасный -> спросить человека: вернуть bool(confirm(name, args)).
    """
    raise NotImplementedError('напиши меня')

def wrap_untrusted(text):
    """Обернуть чужой текст (веб-страница, письмо, файл) в <untrusted_data>...</untrusted_data>,
    чтобы модель считала его данными, а не командами.
    Если внутри текста уже встречаются эти теги, обезвредить их (заменить на "[tag]"),
    иначе злоумышленник закроет блок раньше времени.
    """
    raise NotImplementedError('напиши меня')
