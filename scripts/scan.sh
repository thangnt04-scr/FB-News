#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip >/dev/null 2>&1 || true
pip install -r requirements.txt -r requirements-dev.txt

echo "Running flake8..."
flake8 .

echo "Running pytest..."
pytest -q -k "not test_system"

echo "Running bandit..."
bandit -r -x tests .

echo "Running pip-audit..."
pip-audit -r requirements.txt

echo "All scans completed."
