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
    raise NotImplementedError('напиши меня')

def recall_at_k(cases, retriever, k=3):
    """Доля вопросов, для которых нужный источник попал в первые k результатов.
    cases: список {"question", "expected_source"}. Пустой список -> 0.0.
    """
    raise NotImplementedError('напиши меня')
