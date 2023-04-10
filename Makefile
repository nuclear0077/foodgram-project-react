start:
	cd ./infra/ && \
	cp .env.example .env && \
	docker-compose up -d --build && \
    sleep 2; \
	docker-compose exec db createdb -U postgres foodgram && \
	docker-compose exec backend python manage.py migrate && \
	docker-compose exec backend python manage.py load_ingredients && \
	docker-compose exec backend python manage.py load_tags && \
	docker-compose exec backend python manage.py collectstatic --no-input
drop:
	cd ./infra/ && \
	docker-compose down -v
stop:
	cd ./infra/ && \
	docker-compose down
run:
	cd ./infra/ && \
	docker-compose up -d
start_with_load_dump:
	cd ./infra/ && \
	cp .env.example .env && \
	docker-compose up -d --build && \
    sleep 2; \
	docker-compose exec db createdb -U postgres foodgram && \
	docker-compose exec backend python manage.py migrate && \
	docker-compose exec backend python manage.py loaddata ./data/fixtures.json && \
	docker-compose exec backend python manage.py collectstatic --no-input
format:
	pre-commit run --all-files
