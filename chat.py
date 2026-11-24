import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["LLM_API_KEY"])
model = os.environ["LLM_MODEL"]

history = []
print("Пиши вопрос. Пустая строка — выход.")

while True:
    text = input("Ты: ")
    if not text.strip():
        break
    history.append({"role": "user", "content": text})
    resp = client.messages.create(
        model=model,
        max_tokens=1000,
        system="Ты менеджер кофейни в Алматы. Отвечай клиентам вежливо и коротко. Капучино 1500 тенге, латте 1700, раф 1900. Работаем с 8 до 22.",
        messages=history,
    )
    reply = resp.content[0].text
    history.append({"role": "assistant", "content": reply})
    print("Claude:", reply)