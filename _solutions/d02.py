"""День 2. Первый вызов модели и секреты.

Во всём курсе модель передаётся в функции параметром llm. Так код не привязан
к одному провайдеру и тестируется без ключа и без денег.
"""


def load_settings(env):
    """env: словарь переменных окружения (в жизни os.environ).
    Вернуть {"api_key": ..., "model": ...} из LLM_API_KEY и LLM_MODEL.
    Нет ключа или модели (или пустая строка) -> RuntimeError с именем недостающей переменной в тексте.
    """
    out = {}
    for key, var in (("api_key", "LLM_API_KEY"), ("model", "LLM_MODEL")):
        value = (env.get(var) or "").strip()
        if not value:
            raise RuntimeError(f"не задана переменная {var}")
        out[key] = value
    return out


def mask(secret):
    """Спрятать секрет для логов: первые 4 символа + "..." + последние 4.
    Строка короче 12 символов -> "***" целиком.
    """
    if len(secret) < 12:
        return "***"
    return secret[:4] + "..." + secret[-4:]


def ask(prompt, llm, system=None):
    """Задать вопрос модели. llm(messages) -> строка.
    - собрать messages: сначала {"role": "system"} (если system задан), потом {"role": "user"};
    - пустой или пробельный prompt -> ValueError, модель не вызывать;
    - вернуть ответ без пробелов и переносов по краям.
    """
    if not prompt or not prompt.strip():
        raise ValueError("пустой prompt")
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    return llm(messages).strip()
