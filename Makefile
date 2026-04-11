.PHONY: up down logs restart migrate shell

up:
	docker-compose up -d --build

down:
	docker-compose down

logs:
	docker-compose logs -f bot

restart:
	docker-compose restart bot

# Создать новую миграцию
# make migrate msg="add column xyz"
migrate:
	docker-compose run --rm bot alembic revision --autogenerate -m "$(msg)"

# Применить миграции
upgrade:
	docker-compose run --rm bot alembic upgrade head

# Откатить последнюю миграцию
downgrade:
	docker-compose run --rm bot alembic downgrade -1

# Python shell внутри контейнера
shell:
	docker-compose run --rm bot python

# Запуск без Docker (локально)
run-local:
	python -m bot.main
