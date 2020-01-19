
build/backend:
	docker build ./backend -f ./backend/Dockerfile --target=default -t jaaxman-backend

build/backend-dev:
	docker-compose build backend

build/nginx:
	docker build ./backend -f ./backend/Dockerfile.nginx -t jaaxman-nginx

up:
	docker-compose up

stop:
	docker-compose stop

run/fetchrss:
	docker-compose run --rm backend python manage.py fetchrss

run/registerrss:
	docker-compose run --rm backend python manage.py registerrss

.PHONY: test
test: test/backend

test/backend:
	docker-compose run --rm -e RUN_MODE=test backend python manage.py test

.PHONY: lint
lint/flake8:
	docker-compose run --rm backend flake8 .

lint/isort:
	docker-compose run --rm backend isort -rc -c .

lint/eslint:
	docker-compose run --rm frontend npm run lint
