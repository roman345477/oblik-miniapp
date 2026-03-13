# ОБЛІК — Telegram Mini App

Трекер робочих годин для Telegram.

## Файли

```
bot.py          — сервер + бот
index.html      — Mini App (весь UI)
requirements.txt
Procfile
```

## Деплой на Railway

### 1. Створи новий проект

- railway.app → New Project → Deploy from GitHub repo
- Або: New Project → Empty Project → Add Service → GitHub Repo

### 2. Підключи репо

Завантаж ці 4 файли в GitHub репо і підключи його.

### 3. Налаштуй змінні (Variables)

```
BOT_TOKEN = <токен від @BotFather>
```

**APP_URL можна не вказувати** — він підтягнеться автоматично з `RAILWAY_PUBLIC_DOMAIN`.

Якщо не підтягнувся — додай вручну:
```
APP_URL = https://твій-домен.up.railway.app
```

### 4. Згенеруй домен

Settings → Networking → Generate Domain

### 5. Перевір

1. Відкрий `https://твій-домен.up.railway.app` в браузері — має показати ОБЛІК
2. Напиши боту `/start` — з'явиться кнопка "Відкрити ОБЛІК"
3. Кнопка меню зліва від поля вводу теж відкриє додаток

### Логи

Deployments → останній деплой → View Logs

Має бути:
```
APP_URL = https://...
🌐 HTTP server on port ...
✅ Menu button → https://...
🤖 Bot started
```
