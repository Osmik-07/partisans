# 🐾 Partisans

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

## Автодеплой (GitHub Actions)

Пуш в `main` сам выкатывает изменения на сервер. GitHub Actions подключается по SSH ключом, который на сервере ограничен `authorized_keys`-командой на ровно один скрипт (`deploy/deploy.sh`) — что бы CI ни отправил, выполнится только он. Скрипт тянет код, собирает образ, прогоняет `alembic upgrade head` и только потом перезапускает бота. Если миграция упала, перезапуска не будет — бот продолжит работать на старой версии. Если код бота не менялся (правки README, `deploy/`, `.github/` и т.п.), образ остаётся прежним и бот не перезапускается: лишнее исключает `.dockerignore`.

Запустить деплой без пуша: Actions → Deploy → Run workflow. Ручные шаги выше нужны только для первого запуска сервера.

### Одноразовая настройка

1. Ключ, на своём компьютере:

   ```bash
   ssh-keygen -t ed25519 -f ~/.ssh/partisans_deploy -N "" -C partisans-deploy
   ```

2. На сервере добавить публичный ключ (`partisans_deploy.pub`) в `/root/.ssh/authorized_keys` одной строкой, путь — к папке проекта:

   ```text
   restrict,command="/root/partisans/deploy/deploy.sh" ssh-ed25519 AAAA... partisans-deploy
   ```

3. В репозитории на GitHub: Settings → Secrets and variables → Actions:
   - `VPS_HOST` — IP или домен сервера
   - `VPS_DEPLOY_KEY` — содержимое приватного ключа `~/.ssh/partisans_deploy`

4. Проверить на сервере, что `cd /root/partisans && git fetch origin main` проходит без запроса пароля и что `git status` чистый. Деплой делает `git reset --hard origin/main` и сотрёт ручные правки отслеживаемых файлов. `.env` в git не лежит и не затрагивается.

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

Кнопка **Статистика** в `/admin` показывает: количество пользователей, активных подписок и суммарный доход в USD.

Свой Telegram ID можно узнать у [@userinfobot](https://t.me/userinfobot).

---

## Тарифы

| Тариф | Срок | СБП | CryptoBot | Stars |
|---|---|---|---|---|
| Пробный | 3 дня | — | Бесплатно | — |
| Неделя | 7 дней | 99 ₽ | $1.00 | 50 ★ |
| Месяц | 30 дней | 149 ₽ | $2.00 | 100 ★ |
| Год | 365 дней | 799 ₽ | $10.00 | 500 ★ |
| Защита | разово | — | $100.00 | 5000 ★ |

Порядок покупки: **способ оплаты → тариф**. Цены показываются в валюте выбранного способа.

Оплата через СБП — заглушка, пока не подключён эквайер: экран «скоро», платёж не создаётся. Включается переменной `SBP_ENABLED` после интеграции.

Цены меняются в `.env` (`PRICE_*`). Те же цифры продублированы в `miniapp/legal.json` — это оферта, и `ops/publish_legal.py` не даст опубликовать документы, если они разойдутся с `bot/config.py`.

---

## Документы и поддержка

Политика конфиденциальности и Пользовательское соглашение живут в одном файле — `miniapp/legal.json`. Оттуда их берут:

- Mini App — показывает текст в модальном окне; без двух галочек привязать номер нельзя;
- Telegra.ph — публичные копии, на них ссылаются бот и эквайер.

Обновить публичные копии после правки `legal.json`:

```bash
python3 ops/publish_legal.py --dry-run   # проверить цены, ничего не публикуя
python3 ops/publish_legal.py             # обновить страницы на Telegra.ph
```

Скрипт правит те же страницы, а не создаёт новые: токен и адреса лежат в `ops/.telegraph_state.json` (в git не попадает — это доступ к страницам).

Контакт поддержки задаётся переменной `SUPPORT_CONTACT`, ссылки на документы — `PRIVACY_URL` и `TERMS_URL`. В боте всё это открывается кнопкой «Поддержка и документы».

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
