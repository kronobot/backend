.PHONY: run createmigrations migrate createsuperuser

run:
	docker compose up --build

createmigrations:
	docker compose exec app python manage.py makemigrations

migrate:
	docker compose exec app python manage.py migrate

createsuperuser:
	docker compose exec app python manage.py createsuperuser
