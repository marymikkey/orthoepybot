# orthoepybot

Telegram-бот для подготовки к заданию ЕГЭ по русскому языку на ударения (орфоэпия). Школьный проект, 2021.

Бот выдаёт задания двух типов, проверяет ответ и показывает объяснение. Задания и ответы лежат в `zadania.txt`, `zadka2.txt`, `otveti.txt`, `obiasnenie.txt`.

## Запуск

```bash
pip install -r requirements.txt
export BOT_TOKEN=<токен от @BotFather>
python main.py
```

Stack: Python, pyTelegramBotAPI, Heroku (Procfile).
