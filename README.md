# 👁 NotSpyBot

Telegram Business Bot для перехвата удалённых сообщений, правок и исчезающих фото.  
Монетизация через **CryptoBot** (крипта) и **Telegram Stars**.

---

## Деплой на сервер

### 1. Зайти на сервер по SSH

```bash
ssh user@server_ip
```

### 2. Убедиться, что Docker и Compose установлены

```bash
docker --version
docker compose version
```

Если Docker не установлен:

```bash
curl -fsSL https://get.docker.com | sh
```

### 3. Скопировать проект на сервер

```bash
git clone <ссылка_на_репозиторий>
cd notspybot
```

### 4. Создать .env

```bash
cp .env.example .env
nano .env
```

### 5. Заполнить .env

```env
BOT_TOKEN=твой_токен_от_BotFather
ADMIN_IDS=твой_telegram_id

TELEGRAM_API_ID=твой_api_id
TELEGRAM_API_HASH=твой_api_hash
USERBOT_SESSION_SECRET=длинная_случайная_строка

DB_HOST=db
DB_PORT=5432
DB_NAME=notspybot
DB_USER=notspybot
DB_PASS=strongpassword

REDIS_URL=redis://redis:6379/0

CRYPTOBOT_TOKEN=токен_от_CryptoBot
CRYPTOBOT_WEBHOOK_SECRET=любая_произвольная_строка

WEBHOOK_HOST=
```

`WEBHOOK_HOST` оставь пустым — бот запустится в polling-режиме, домен не нужен.

### 6. Собрать образы

```bash
docker compose build --no-cache
```

### 7. Поднять БД и Redis

```bash
docker compose up -d db redis
```

### 8. Применить миграции БД

```bash
docker compose run --rm bot alembic upgrade head
```

### 9. Запустить бота

```bash
docker compose up -d bot
```

### 10. Проверить что всё работает

```bash
docker compose logs -f bot   # логи в реальном времени
docker compose ps            # статус контейнеров
```

---

## Настройка Telegram

### BotFather

1. Открой [@BotFather](https://t.me/BotFather)
2. `/newbot` → введи имя и username → скопируй токен в `BOT_TOKEN`
3. `/mybots` → выбери бота → **Bot Settings** → **Business Bot** → **Enable**

### Подключение бота к своему аккаунту

Требуется **Telegram Premium**.

Настройки → Telegram для бизнеса → Чат-боты → найди бота → подключи → разреши доступ ко всем чатам.

### CryptoBot

1. Открой [@CryptoBot](https://t.me/CryptoBot)
2. **My Apps** → **Create App** → скопируй токен в `CRYPTOBOT_TOKEN`
3. Придумай любую строку для `CRYPTOBOT_WEBHOOK_SECRET` (например `secret123`)

---

## Админ-панель

Доступна только для ID из `ADMIN_IDS` в `.env`.

| Команда | Действие |
|---|---|
| `/admin` | Открыть панель |
| `/ban 123456789` | Заблокировать пользователя |
| `/unban 123456789` | Разблокировать пользователя |
| `/userinfo 123456789` | Информация о пользователе и его подписке |
| `/broadcast Текст` | Рассылка всем незаблокированным пользователям |

Кнопка **📊 Статистика** в `/admin` показывает: количество пользователей, активных подписок и суммарный доход в USD.

Свой Telegram ID можно узнать у [@userinfobot](https://t.me/userinfobot).

---

## Тарифы

| Тариф | Срок | Цена |
|---|---|---|
| 🎁 Пробный | 3 дня | Бесплатно |
| ⚡️ Неделя | 7 дней | $1.50 |
| 🔥 Месяц | 30 дней | $3.00 |
| 👑 Год | 365 дней | $15.00 |

Цены и длительность пробного периода меняются в `.env` — переменные `PRICE_TRIAL_DAYS`, `PRICE_WEEK_USD`, `PRICE_MONTH_USD`, `PRICE_YEAR_USD`.

---

## Полезные команды

```bash
# Перезапустить после изменений
docker compose build --no-cache
docker compose up -d

# Остановить
docker compose down

# Посмотреть логи
docker compose logs -f bot

# Выполнить команду внутри контейнера
docker compose exec bot <команда>
```
