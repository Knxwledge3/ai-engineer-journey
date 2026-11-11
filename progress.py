"""Твой прогресс по курсу.

  python progress.py        таблица по всем дням
  python progress.py diag   результат диагностики и рекомендация
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent
TITLES = {
    "d01": "Python: данные и файлы",
    "d02": "Первый вызов модели и секреты",
    "d03": "Промпты как код и первый eval",
    "d04": "Структурированный вывод",
    "d05": "Внешние API и ошибки",
    "d06": "Эмбеддинги и нарезка текста",
    "d07": "FastAPI и SQLite",
    "d08": "RAG своими руками",
    "d09": "Качество RAG",
    "d10": "Проект 1: RAG-сервис в интернете",
    "d11": "Telegram-бот и расписание",
    "d12": "Автоматизация: вебхуки и n8n",
    "d13": "Агент своими руками",
    "d14": "Инструменты и память диалога",
    "d15": "MCP: стандартный разъём для инструментов",
    "d16": "Фреймворк и работа с ИИ-агентом для кода",
    "d17": "Надёжность и безопасность",
    "d18": "Evals для агента",
    "d19": "Деньги, git на рабочем уровне, CI",
    "d20": "Продукт: сборка и запуск",
    "d21": "Демо, разбор и следующий этап"
}


class Collector:
    def __init__(self):
        self.stats = {}
        self.broken = set()

    def _key(self, nodeid):
        return Path(nodeid.split("::")[0]).parent.name

    def pytest_runtest_logreport(self, report):
        if report.when == "call" or (report.when == "setup" and report.outcome != "passed"):
            s = self.stats.setdefault(self._key(report.nodeid), {"ok": 0, "all": 0, "names": []})
            s["all"] += 1
            s["ok"] += report.outcome == "passed"
            if report.outcome == "passed":
                s["names"].append(report.nodeid.split("::")[-1])

    def pytest_collectreport(self, report):
        if report.failed:
            self.broken.add(self._key(report.nodeid))


def run(path):
    c = Collector()
    pytest.main(["-q", "--tb=no", "--no-header", "-p", "no:cacheprovider", str(path)], plugins=[c])
    return c


def bar(ok, total, width=10):
    filled = round(width * ok / total) if total else 0
    return "[" + "#" * filled + "." * (width - filled) + "]"


def show_days():
    c = run(ROOT / "days")
    print("\n\nПРОГРЕСС ПО КУРСУ\n")
    done = 0
    for did, title in TITLES.items():
        n = int(did[1:])
        if did in c.broken:
            status = "ошибка в файле (синтаксис или импорт)"
        elif did in c.stats:
            s = c.stats[did]
            status = f"{bar(s['ok'], s['all'])} {s['ok']}/{s['all']}"
            if s["ok"] == s["all"]:
                status += "  СДАНО"
                done += 1
        else:
            status = "чек-лист в README (ручная проверка)"
        print(f"  День {n:>2}  {title:<45} {status}")
    auto = len(c.stats) + len(c.broken)
    print(f"\n  Ката сдано: {done} из {auto}. Дни с чек-листом отмечай сам в PLAN.md.\n")


def show_diag():
    c = run(ROOT / "diagnostic")
    s = c.stats.get("diagnostic", {"ok": 0, "all": 8, "names": []})
    passed = {n.split("_")[1] for n in s["names"]}
    print(f"\n\nДИАГНОСТИКА: {s['ok']} из 8\n")
    topics = {"1": "словари и циклы", "2": "строки", "3": "обработка ошибок", "4": "файлы и JSON",
              "5": "классы", "6": "функции как аргументы, исключения", "7": "сортировка с ключом",
              "8": "формат диалога с моделью"}
    for k, t in topics.items():
        print(f"  {'+' if k in passed else '-'} задача {k}: {t}")
    ok = s["ok"]
    print()
    if "diagnostic" in c.broken:
        print("  В diag.py синтаксическая ошибка, тесты не запустились. Исправь и повтори.")
    elif ok <= 3:
        print("  Уровень: старт. Иди по плану с Дня 1 без сокращений, темп 1 день = 1 день.")
        print("  Дни 1-9 пиши только руками, без ИИ-автодополнения.")
    elif ok <= 6:
        print("  Уровень: база есть. День 1 сделай за полдня, в тот же день начни День 2.")
        print("  Несданные темы выше повтори по 20 минут каждую перед соответствующим днём.")
    else:
        print("  Уровень: уверенный. Дни 1 и 2 сдай за один день, дни 4 и 5 тоже за один.")
        print("  Реальный срок курса для тебя: 16-18 дней. Освободившееся время отдай продукту.")
    print()


if __name__ == "__main__":
    show_diag() if len(sys.argv) > 1 and sys.argv[1] == "diag" else show_days()
