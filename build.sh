#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
python -c "from db import init_db; init_db()"

echo "Build completed successfully!"

