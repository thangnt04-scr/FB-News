.PHONY: install dev-install run lint test bandit audit scan-all docker-build docker-up docker-down docker-logs docker-sh

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt -r requirements-dev.txt

run:
	python app.py

lint:
	flake8 .

test:
	pytest -q -k "not test_system"

bandit:
	bandit -r -x tests .

audit:
	pip-audit -r requirements.txt

scan-all: lint test bandit audit

docker-build:
	docker build -t football-info:local .

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down -v || true

docker-logs:
	docker compose logs -f --tail=200 web

docker-sh:
	docker compose exec web /bin/sh
