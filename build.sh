#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Initialize database if needed
python -c "import db; db.init_db()" || true

