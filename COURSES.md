# Курсы: что открывать и когда

Сверено по открытым источникам 11 ноября 2026. Названия и содержание курсов меняются, поэтому перед началом проверь, что курс на месте и не устарел. Длительность и точный состав разделов смотри на странице курса.

## Главное правило

Курс — справочник под тему дня, а не сериал. Порядок такой: читаешь README дня, пробуешь кату сам, застрял или сдал — открываешь нужный раздел. Не больше часа в день.

## Основа: курсы Anthropic

Ты работаешь с Claude API, поэтому главный источник теории — бесплатные курсы самой Anthropic на anthropic.skilljar.com (Anthropic Academy). В первом плане их не было.

| Курс | Зачем тебе |
|---|---|
| Claude Platform 101 | Вход с нуля: как строить на платформе Claude, если раньше работал только в чате. |
| Building with the Claude API | Основной курс. В программе есть кэширование промптов, MCP, Claude Code, агенты и рабочие процессы. |
| Claude Code 101 | Работа с ИИ-агентом для кода: файл CLAUDE.md, субагенты, skills, MCP, hooks. |

## По дням

| День | Тема | Что открыть |
|---|---|---|
| 1 | Python: данные и файлы | AI Python for Beginners (DeepLearning.AI): только уроки про списки, словари и файлы, когда застрял |
| 2 | Первый вызов модели | Claude Platform 101: начало; quickstart в документации Claude API |
| 3 | Промпты и eval | Building with the Claude API: разделы про промпты; руководство по промптам в документации |
| 4 | Структурированный вывод | Документация Pydantic; раздел о структурированном выводе в документации Claude API |
| 5 | Внешние API и ошибки | Курс не нужен: статья про коды HTTP и exponential backoff |
| 6 | Эмбеддинги | Hugging Face LLM Course, глава 1 (по желанию) |
| 7 | FastAPI | Официальный FastAPI Tutorial: первые три раздела |
| 8-9 | RAG и его качество | RAG from Scratch (LangChain): части про indexing, retrieval, generation |
| 10 | Деплой | Docker: Get Started; документация хостинга |
| 11 | Telegram-бот | Документация Telegram Bot API |
| 12 | Вебхуки и n8n | Документация n8n: Quickstart, Webhook, HTTP Request |
| 13-14 | Агент и инструменты | Building with the Claude API: разделы про tool use и «Agents and workflows»; статья Anthropic «Building effective agents» |
| 15 | MCP | Building with the Claude API: раздел Model Context Protocol. Нужно глубже: Hugging Face MCP Course (бесплатный, сделан вместе с Anthropic) |
| 16 | Фреймворк и агент для кода | Claude Code 101 |
| 17 | Надёжность и безопасность | OWASP Top 10 for LLM Applications: prompt injection |
| 18 | Evals для агента | Evaluating AI Agents (DeepLearning.AI и Arize): первые модули |
| 19 | Стоимость | Building with the Claude API: раздел Prompt caching; актуальная страница цен |
| 20-21 | Продукт и демо | Книга «Спроси маму» (The Mom Test): первые три главы |

## Что стало с курсами из первого плана

| Курс из первого плана | Решение | Почему |
|---|---|---|
| AI Python for Beginners (11,5 ч) | Оставлен как справочник | Смотреть целиком — три дня без своего кода |
| Intro to Large Language Models (1 ч) | По желанию | Полезен для общего понимания, на навык не влияет |
| Hugging Face LLM Course, глава 1 | По желанию, день 6 | Остальной курс про обучение моделей, тебе пока не нужно |
| RAG from Scratch | Оставлен, по частям | Хорошо объясняет устройство RAG |
| Building and Evaluating Advanced RAG | Убран | Курс старый и завязан на конкретные библиотеки; оценку RAG ты делаешь руками в день 9 |
| IBM: два коротких видео про агентов | Убраны | Обзорные; то же самое ты поймёшь, написав цикл агента в день 13 |
| Hugging Face Agents Course | По желанию после дня 14 | Теперь есть курсы Anthropic под твой стек |
| LangChain: Chat with Your Data | Убран | Фреймворк выбираем в день 16 по актуальному состоянию |
| Evaluating AI Agents (Arize) | Оставлен, день 18 | |
| Evaluating and Debugging GenAI (W&B) | Убран | Перекрывается днями 17-18 |
| 27 AI Engineering Projects | Убран | Тему даёт не видео, а разговоры с компаниями |
| Generative AI for Software Development (31 ч) | Отложен | Слишком длинный для текущей цели |
| LLMOps (Google Cloud) | Убран | Про дообучение моделей |

## Дополнительно, если останется время

- **MCP: Build Rich-Context AI Apps with Anthropic** (DeepLearning.AI): короткое введение в MCP, альтернатива разделу в основном курсе.
- **Claude Code: A Highly Agentic Coding Assistant** (DeepLearning.AI): к дню 16.
- **Agent Skills with Anthropic** (DeepLearning.AI): как выносить логику агента в переиспользуемые навыки. После дня 18.

## Чего в списке нет намеренно

- Платных курсов и буткемпов. Всё нужное для этого плана есть бесплатно.
- Курсов «всё об ИИ за 40 часов». Для твоей цели они дают ощущение прогресса без навыка.
