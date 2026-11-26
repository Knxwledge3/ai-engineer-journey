import os
import httpx
import anthropic
from dotenv import load_dotenv

load_dotenv()
TG = "https://api.telegram.org/bot" + os.environ["TELEGRAM_TOKEN"]
client = anthropic.Anthropic(api_key=os.environ["LLM_API_KEY"])
MODEL = os.environ["LLM_MODEL"]

SYSTEM = (
    "Ты помощник Ерса по поиску клиентов среди малого бизнеса в Казахстане. "
    "Помогаешь выбрать нишу, понять, какие задачи бизнеса можно автоматизировать, "
    "и подготовить первое сообщение владельцу. Отвечай по-русски, коротко. "
    "Никогда не выдумывай названия компаний, телефоны и сайты: если не знаешь, так и скажи."
    "Отвечай не длиннее 15 строк"
)

histories = {}
offset = 0
print("Бот запущен. Остановить: Ctrl+C")

while True:
    r = httpx.get(TG + "/getUpdates", params={"offset": offset, "timeout": 30}, timeout=40)
    for upd in r.json().get("result", []):
        offset = upd["update_id"] + 1
        msg = upd.get("message")
        if not msg or "text" not in msg:
            continue
        chat_id = msg["chat"]["id"]
        text = msg["text"]

        if text == "/start":
            histories[chat_id] = []
            reply = "Привет! Я помогаю искать клиентов. Расскажи, какой бизнес ищем."
        else:
            history = histories.setdefault(chat_id, [])
            history.append({"role": "user", "content": text})
            try:
                resp = client.messages.create(
                    model=MODEL, max_tokens=1500, system=SYSTEM, messages=history[-20:]
                )
                reply = resp.content[0].text
                history.append({"role": "assistant", "content": reply})
            except Exception as e:
                reply = "Ошибка, попробуй ещё раз."
                print("Ошибка:", e)

        httpx.post(TG + "/sendMessage", json={"chat_id": chat_id, "text": reply})