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
    app = FastAPI()

    def connect():
        con = sqlite3.connect(db_path)
        con.execute(
            "CREATE TABLE IF NOT EXISTS history("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, answer TEXT, created_at TEXT)"
        )
        return con

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/ask")
    def ask(body: AskIn):
        try:
            answer = llm([{"role": "user", "content": body.question}])
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=503, detail="модель недоступна") from e
        con = connect()
        with con:
            con.execute(
                "INSERT INTO history(question, answer, created_at) VALUES (?, ?, ?)",
                (body.question, answer, datetime.now(timezone.utc).isoformat()),
            )
        con.close()
        return {"answer": answer}

    @app.get("/history")
    def history(limit: int = Query(10, ge=1, le=100)):
        con = connect()
        rows = con.execute(
            "SELECT question, answer, created_at FROM history ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        con.close()
        return [{"question": q, "answer": a, "created_at": c} for q, a, c in rows]

    return app
