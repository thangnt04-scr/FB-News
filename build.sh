#!/usr/bin/env bash
# exit on error
set -o errexit

echo "========================================="
echo "Starting build process..."
echo "========================================="

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
echo "🔧 Initializing database..."
python -c "from db import init_db; init_db()"

# Populate database with football data
echo "📊 Populating database with football data..."
python populate_db.py

echo "========================================="
echo "✅ Build completed successfully!"
echo "========================================="

