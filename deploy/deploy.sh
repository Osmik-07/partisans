#!/usr/bin/env bash
# Выполняется на VPS через forced command из authorized_keys — GitHub Actions
# не может передать сюда ничего, кроме самого подключения.
#
# Всё тело — в функции не для красоты: ниже мы делаем git reset, который
# переписывает ЭТОТ ЖЕ файл прямо во время выполнения. Bash дочитывает скрипт
# с диска по мере исполнения, поэтому в «плоском» виде он после обновления
# продолжал бы читать новый файл со старого смещения — то есть пропускал или
# коверкал команды. Функция разбирается целиком до первого вызова, и подмена
# файла на текущий запуск уже не влияет.
set -euo pipefail

main() {
  # Папку проекта берём от самого скрипта, чтобы не зависеть от пути на сервере.
  cd "$(dirname "${BASH_SOURCE[0]}")/.."
  export GIT_TERMINAL_PROMPT=0

  if docker compose version >/dev/null 2>&1; then
    dc="docker compose"
  else
    dc="docker-compose"
  fi

  echo "==> git pull"
  git fetch origin main
  git reset --hard origin/main

  echo "==> сборка образа"
  $dc build bot

  # Миграции гоним новым образом, пока ещё работает старый бот: если миграция
  # упадёт, set -e остановит деплой до рестарта и бот останется на старой версии.
  echo "==> миграции БД"
  $dc run --rm -T bot alembic upgrade head

  echo "==> рестарт бота"
  $dc up -d

  # restart: unless-stopped маскирует падение на старте: контейнер то «running»,
  # то «restarting». Если за 6 секунд StartedAt сменился — бот перезапускался сам.
  echo "==> проверка"
  cid="$($dc ps -q bot)"
  started="$(docker inspect -f '{{.State.StartedAt}}' "$cid")"
  sleep 6
  state="$(docker inspect -f '{{.State.Status}} {{.State.StartedAt}}' "$cid")"
  if [ "$state" != "running $started" ]; then
    echo "!! бот не поднялся ($state), последние логи:"
    $dc logs --tail 40 bot
    exit 1
  fi

  # Каждая сборка оставляет старый образ без тега — чистим, чтобы не забить диск.
  docker image prune -f >/dev/null

  echo "==> готово: $(git rev-parse --short HEAD)"
}

main "$@"
