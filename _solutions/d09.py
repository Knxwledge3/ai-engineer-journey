"""День 9. Качество RAG: честное "не знаю" и измерение поиска."""


def answer_guarded(question, retriever, llm, min_score=0.3, k=3):
    """Ответ с защитой от выдумок. retriever.search(question, k=k) -> список
    {"text", "source", "score"} по убыванию score.
    - оставить только куски со score >= min_score;
    - если таких нет: модель НЕ вызывать, вернуть
      {"answer": текст, начинающийся с "Не знаю", "sources": [], "grounded": False};
    - иначе вызвать llm(messages) с текстами оставшихся кусков и вопросом и вернуть
      {"answer": ..., "sources": [уникальные источники оставшихся кусков], "grounded": True}.
    """
    hits = [h for h in retriever.search(question, k=k) if h["score"] >= min_score]
    if not hits:
        return {"answer": "Не знаю: в документах нет ответа на этот вопрос.", "sources": [], "grounded": False}
    context = "\n\n".join(h["text"] for h in hits)
    messages = [
        {"role": "system", "content": "Отвечай только по контексту."},
        {"role": "user", "content": f"Контекст:\n{context}\n\nВопрос: {question}"},
    ]
    sources = []
    for h in hits:
        if h["source"] not in sources:
            sources.append(h["source"])
    return {"answer": llm(messages), "sources": sources, "grounded": True}


def recall_at_k(cases, retriever, k=3):
    """Доля вопросов, для которых нужный источник попал в первые k результатов.
    cases: список {"question", "expected_source"}. Пустой список -> 0.0.
    """
    if not cases:
        return 0.0
    ok = 0
    for c in cases:
        found = [h["source"] for h in retriever.search(c["question"], k=k)]
        ok += c["expected_source"] in found
    return ok / len(cases)
