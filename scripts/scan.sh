#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

echo "== Running flake8 =="
flake8 . || true

echo "== Running bandit =="
bandit -r . -x tests || true

echo "== Running pip-audit =="
pip-audit -r requirements.txt || true

echo "== Running safety =="
safety check -r requirements.txt --full-report || true
