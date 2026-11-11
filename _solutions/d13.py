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
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user_text})
    specs = [
        {"name": n, "description": t.get("description", ""), "parameters": t.get("schema", {})}
        for n, t in tools.items()
    ]
    steps = []
    for _ in range(max_steps):
        resp = llm(list(messages), specs)
        calls = resp.get("tool_calls") or []
        if not calls:
            return {"answer": resp.get("text") or "", "steps": steps, "stopped": "final"}
        messages.append({"role": "assistant", "content": resp.get("text") or "", "tool_calls": calls})
        for call in calls:
            name, args = call["name"], call.get("args") or {}
            if name not in tools:
                result = f"error: unknown tool {name}"
            else:
                try:
                    result = tools[name]["fn"](**args)
                except Exception as e:  # noqa: BLE001
                    result = f"error: {e}"
            messages.append({"role": "tool", "tool_call_id": call.get("id"), "name": name, "content": str(result)})
            steps.append({"tool": name, "args": args, "result": result})
    return {"answer": "", "steps": steps, "stopped": "max_steps"}
