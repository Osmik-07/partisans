#!/bin/bash
# deploy.sh — скрипт первичного деплоя на чистый Ubuntu VPS
# Запускать от root или sudo: bash deploy.sh

set -e

echo "=== NotSpyBot Deploy ==="

# 1. Зависимости системы
apt-get update -y
apt-get install -y docker.io docker-compose git curl

# 2. Клонируем / обновляем репозиторий
if [ -d "/opt/notspybot" ]; then
    echo "Updating existing repo..."
    cd /opt/notspybot && git pull
else
    echo "Cloning repo..."
    git clone https://github.com/YOUR_USERNAME/notspybot /opt/notspybot
    cd /opt/notspybot
fi

# 3. Копируем .env если не существует
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo "⚠️  ВАЖНО: заполни /opt/notspybot/.env перед запуском!"
    echo "   nano /opt/notspybot/.env"
    echo ""
    exit 1
fi

# 4. Запуск
docker-compose pull
docker-compose up -d --build

echo ""
echo "✅ Бот запущен!"
echo "Логи: docker-compose -f /opt/notspybot/docker-compose.yml logs -f bot"
