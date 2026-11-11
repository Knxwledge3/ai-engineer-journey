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
    raise NotImplementedError('напиши меня')

def filter_by_tag(cards, tag):
    """Вернуть карточки, у которых есть тег tag (без учёта регистра и пробелов по краям)."""
    raise NotImplementedError('напиши меня')

def save_cards(cards, path):
    """Сохранить карточки в JSON-файл: utf-8, кириллица читаемая (не \\u0441...), с отступами."""
    raise NotImplementedError('напиши меня')

def load_cards(path):
    """Прочитать карточки из файла. Файла нет -> пустой список."""
    raise NotImplementedError('напиши меня')
