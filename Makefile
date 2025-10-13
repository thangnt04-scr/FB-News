# Makefile for Dev, Docker and Security Scans

.PHONY: install install-dev run lint format test docker-build docker-run scan-deps scan-sast scan-image scan-all

install:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

install-dev:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt

run:
	FLASK_SECRET_KEY=$${FLASK_SECRET_KEY:-dev} python app.py

lint:
	. .venv/bin/activate && flake8 .

format:
	. .venv/bin/activate && black .

test:
	. .venv/bin/activate && pytest -q --disable-warnings --maxfail=1 -k "not test_system"

scan-deps:
	. .venv/bin/activate && pip-audit -r requirements.txt || true
	. .venv/bin/activate && safety check -r requirements.txt --full-report || true

scan-sast:
	. .venv/bin/activate && bandit -r . -x tests || true

# Basic image scan using trivy if available
scan-image:
	@which trivy >/dev/null 2>&1 && trivy image --ignore-unfixed --severity HIGH,CRITICAL football-info:web || echo "Install trivy to scan Docker images"

scan-all: lint test scan-deps scan-sast
