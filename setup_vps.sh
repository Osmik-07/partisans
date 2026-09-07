#!/bin/bash
# setup_vps.sh — первичная настройка VPS (без Docker)
set -e

echo "📦 Установка зависимостей..."
sudo apt update && sudo apt install -y python3.11 python3.11-venv python3-pip \
    postgresql postgresql-contrib redis-server git

echo "🗄 Настройка PostgreSQL..."
sudo -u postgres psql <<SQL
CREATE USER notspybot WITH PASSWORD 'changeme';
CREATE DATABASE notspybot OWNER notspybot;
SQL

echo "🐍 Создание venv..."
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "📋 Настрой .env перед запуском:"
cp .env.example .env
echo "  nano .env"

echo "🔄 Применение миграций (после настройки .env):"
echo "  alembic upgrade head"

echo "⚙️ Установка systemd сервиса..."
sudo cp notspybot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable notspybot

echo ""
echo "✅ Готово! После настройки .env запусти:"
echo "  sudo systemctl start notspybot"
echo "  sudo systemctl status notspybot"

echo ""
echo "ℹ️  Проверка и деактивация истёкших подписок, а также напоминания за 24ч"
echo "   выполняются автоматически внутри самого бота (bot/services/scheduler.py)."
echo "   Отдельный cron для этого не нужен."
