"""День 1. Картотека ссылок: функции, списки, словари, JSON, файлы."""
import json
from pathlib import Path

def add_card(cards, name, url, tags=None):
    """Вернуть НОВЫЙ список с добавленной карточкой {"name", "url", "tags"}.
    - исходный список cards не изменять;
    - name и url обрезать по пробелам; пустой name или url -> ValueError;
    - карточка с таким именем уже есть (без учёта регистра) -> ValueError;
    - tags: привести к нижнему регистру, убрать дубли, сохранить порядок; None -> [].
    """
    name = name.strip()
    url = url.strip()
    if not name or not url:
        raise ValueError("имя и ссылка обязательны")
    for c in cards:
        if c["name"].lower() == name.lower():
            raise ValueError("такая карточка уже есть")
    clean = []
    for t in tags or []:
        t = t.strip().lower()
        if t and t not in clean:
            clean.append(t)
    return cards + [{"name": name, "url": url, "tags": clean}]

def filter_by_tag(cards, tag):
    """Вернуть карточки, у которых есть тег tag (без учёта регистра и пробелов по краям)."""
    tag = tag.strip().lower()
    result = []
    for c in cards:
        if tag in c["tags"]:
            result.append(c)
    return result

def save_cards(cards, path):
    """Сохранить карточки в JSON-файл: utf-8, кириллица читаемая (не \\u0441...), с отступами."""
    text = json.dumps(cards, ensure_ascii=False, indent=2)
    Path(path).write_text(text, encoding="utf-8")

def load_cards(path):
    """Прочитать карточки из файла. Файла нет -> пустой список."""
    p = Path(path)
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))
