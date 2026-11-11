"""День 11. Telegram-бот и ежедневный дайджест: логика отдельно от транспорта."""


def parse_command(text):
    """Разобрать сообщение. Вернуть (команда, аргумент).
    "/ask что такое RAG" -> ("ask", "что такое RAG")
    "/start@MyBot"       -> ("start", "")      имя бота после @ отбросить
    "/HELP"              -> ("help", "")       команда в нижнем регистре
    "просто текст"       -> ("", "просто текст")
    Пробелы по краям убрать.
    """
    text = text.strip()
    if not text.startswith("/"):
        return "", text
    head, _, arg = text[1:].partition(" ")
    return head.split("@")[0].lower(), arg.strip()


def split_message(text, limit=4096):
    """Разбить длинный текст на части не длиннее limit (у Telegram предел 4096 символов).
    Склейка частей обязана дать исходный текст. Пустой текст -> []. limit <= 0 -> ValueError.
    Со звёздочкой: старайся резать по переводу строки, а не посреди слова.
    """
    if limit <= 0:
        raise ValueError("limit должен быть больше нуля")
    parts = []
    while text:
        cut = limit
        if len(text) > limit:
            nl = text.rfind("\n", 0, limit)
            if nl > 0:
                cut = nl + 1
        parts.append(text[:cut])
        text = text[cut:]
    return parts


def build_digest(items, llm, max_items=5):
    """Собрать дайджест. items: список {"title", "url"}. llm(messages) -> строка.
    - пустой список -> вернуть "Сегодня новостей нет.", модель не вызывать;
    - взять первые max_items, один раз вызвать модель, передав в промпте их заголовки;
    - вернуть: сводка модели + пустая строка + "Источники:" + по одной ссылке на строку.
    """
    if not items:
        return "Сегодня новостей нет."
    top = items[:max_items]
    titles = "\n".join(f"- {i['title']}" for i in top)
    summary = llm([{"role": "user", "content": f"Сделай короткую сводку по заголовкам:\n{titles}"}])
    return summary.strip() + "\n\nИсточники:\n" + "\n".join(i["url"] for i in top)
