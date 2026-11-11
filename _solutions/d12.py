"""День 12. Вебхук: твой сервис как шаг сценария автоматизации (n8n, Make и любые другие)."""
import hmac
from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field


class HookIn(BaseModel):
    text: str = Field(min_length=1)


def create_webhook_app(agent, secret):
    """Собрать FastAPI-приложение с одним входом. agent(text) -> строка.
    POST /hook, тело {"text": ...}, заголовок X-Webhook-Secret.
    - заголовка нет или он не равен secret -> 401, агент не вызывается
      (сравнивать через hmac.compare_digest);
    - пустой text -> 422;
    - агент упал -> 500;
    - иначе 200 и {"answer": ответ агента}.
    """
    app = FastAPI()

    @app.post("/hook")
    def hook(body: HookIn, x_webhook_secret: Optional[str] = Header(default=None)):
        if not x_webhook_secret or not hmac.compare_digest(x_webhook_secret.encode(), secret.encode()):
            raise HTTPException(status_code=401, detail="неверный секрет")
        try:
            return {"answer": agent(body.text)}
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=500, detail="агент упал") from e

    return app
