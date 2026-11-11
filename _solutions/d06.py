"""День 6. Эмбеддинги: близость векторов, поиск, нарезка текста."""
import math


def cosine(a, b):
    """Косинусная близость двух векторов (списков чисел).
    Разная длина -> ValueError. Если один из векторов нулевой -> 0.0.
    """
    if len(a) != len(b):
        raise ValueError("векторы разной длины")
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def top_k(query_vec, items, k=3):
    """items: список пар (id, вектор). Вернуть k пар (id, близость) по убыванию близости."""
    scored = [(i, cosine(query_vec, v)) for i, v in items]
    return sorted(scored, key=lambda p: -p[1])[:k]


def chunk_text(text, size=500, overlap=50):
    """Нарезать текст на куски по size символов с перекрытием overlap.
    - каждый следующий кусок начинается с последних overlap символов предыдущего;
    - куски не длиннее size; последний кусок не должен целиком лежать внутри предыдущего;
    - пустой текст -> []; overlap >= size или size <= 0 -> ValueError.
    """
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("нужно 0 <= overlap < size")
    chunks, step, i = [], size - overlap, 0
    while i < len(text):
        chunks.append(text[i : i + size])
        if i + size >= len(text):
            break
        i += step
    return chunks
