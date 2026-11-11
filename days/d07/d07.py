"""День 7. Свой API-сервис на FastAPI с историей в SQLite."""
import sqlite3
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

class AskIn(BaseModel):
    question: str = Field(min_length=1)

def create_app(llm, db_path):
    """Собрать приложение FastAPI. llm(messages) -> строка, db_path: путь к файлу SQLite.
    - GET  /health            -> {"status": "ok"}
    - POST /ask {"question"}  -> {"answer": ...}; пара вопрос-ответ сохраняется в таблицу;
                                 пустой вопрос -> 422; модель упала -> 503, в историю не писать
    - GET  /history?limit=10  -> список {"question", "answer", "created_at"}, новые сверху;
                                 limit от 1 до 100
    Таблицу создать, если её нет.
    """
    raise NotImplementedError('напиши меня')
