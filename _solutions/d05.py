"""День 5. Внешние API и ошибки: таймауты, повторы, коды ответа."""
import time


class TransientError(Exception):
    """Временная ошибка: имеет смысл повторить запрос."""


def with_retries(fn, attempts=3, base_delay=0.5, sleep=time.sleep):
    """Вызвать fn(). При TransientError подождать и повторить, всего не больше attempts вызовов.
    Паузы растут вдвое: base_delay, 2*base_delay, 4*base_delay... (ждать через sleep(секунды)).
    После последней неудачной попытки не ждать, а пробросить TransientError.
    Любое другое исключение пробросить сразу, без повторов.
    """
    for i in range(attempts):
        try:
            return fn()
        except TransientError:
            if i == attempts - 1:
                raise
            sleep(base_delay * 2**i)


def fetch_json(url, get, timeout=10):
    """Запросить JSON. get(url, timeout=...) возвращает объект с .status_code и .json()
    (так устроены requests.get и httpx.get).
    - 200..299 -> вернуть .json();
    - 429 и 500..599 -> TransientError;
    - остальные коды -> ValueError с кодом в тексте.
    timeout обязательно передать в get.
    """
    resp = get(url, timeout=timeout)
    code = resp.status_code
    if 200 <= code < 300:
        return resp.json()
    if code == 429 or 500 <= code < 600:
        raise TransientError(f"временная ошибка {code}")
    raise ValueError(f"ошибка запроса {code}")
