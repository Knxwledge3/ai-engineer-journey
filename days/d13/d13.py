"""День 13. Агент своими руками: цикл "модель -> инструмент -> модель".

Формат в этом курсе (нейтральный к провайдеру):
  llm(messages, tool_specs) -> {"text": строка или None,
                                "tool_calls": [{"id": ..., "name": ..., "args": {...}}]}
  tools = {имя: {"fn": функция, "description": строка, "schema": {...}}}
"""

def run_agent(user_text, llm, tools, max_steps=5, system=None):
    """Запустить агента.
    Цикл: вызвать llm. Нет tool_calls -> это финальный ответ. Есть -> выполнить каждый
    инструмент fn(**args), добавить в messages сообщение
    {"role": "tool", "tool_call_id": id, "name": имя, "content": str(результат)} и вызвать llm снова.
    Перед результатами добавить сообщение ассистента с его tool_calls.
    - неизвестный инструмент: не падать, результат = "error: unknown tool <имя>";
    - инструмент упал: не падать, результат = "error: <текст исключения>";
    - не больше max_steps вызовов llm; если лимит исчерпан, stopped = "max_steps".
    Вернуть {"answer": текст, "steps": [{"tool", "args", "result"}], "stopped": "final" | "max_steps"}.
    """
    raise NotImplementedError('напиши меня')
