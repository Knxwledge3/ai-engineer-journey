"""День 8. RAG своими руками: поиск по своим документам и ответ с источниками."""
import math


def _cosine(a, b):
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return 0.0 if na == 0 or nb == 0 else sum(x * y for x, y in zip(a, b)) / (na * nb)


class Retriever:
    """Хранилище кусков текста с поиском по смыслу.
    embed(text) -> вектор (список чисел). В жизни это вызов модели эмбеддингов.
    """

    def __init__(self, embed):
        """Запомнить функцию embed, завести пустое хранилище."""
        self.embed = embed
        self.items = []

    def add(self, doc_id, text, source):
        """Добавить кусок: посчитать его вектор один раз при добавлении и сохранить."""
        self.items.append({"id": doc_id, "text": text, "source": source, "vec": self.embed(text)})

    def search(self, query, k=3):
        """Вернуть до k кусков по убыванию близости к запросу:
        список {"id", "text", "source", "score"}. Пустое хранилище -> [].
        """
        q = self.embed(query)
        hits = [
            {"id": it["id"], "text": it["text"], "source": it["source"], "score": _cosine(q, it["vec"])}
            for it in self.items
        ]
        return sorted(hits, key=lambda h: -h["score"])[:k]


def answer(question, retriever, llm, k=3):
    """Ответить на вопрос по найденным кускам. llm(messages) -> строка.
    - найти k кусков, вставить их тексты и сам вопрос в промпт;
    - вернуть {"answer": ответ модели, "sources": источники найденных кусков
      без повторов, в порядке убывания близости}.
    """
    hits = retriever.search(question, k=k)
    context = "\n\n".join(f"[{h['source']}]\n{h['text']}" for h in hits)
    messages = [
        {"role": "system", "content": "Отвечай только по контексту. Если ответа в нём нет, так и скажи."},
        {"role": "user", "content": f"Контекст:\n{context}\n\nВопрос: {question}"},
    ]
    sources = []
    for h in hits:
        if h["source"] not in sources:
            sources.append(h["source"])
    return {"answer": llm(messages), "sources": sources}
