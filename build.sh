#!/usr/bin/env bash
# exit on error
set -o errexit

echo "========================================="
echo "Starting build process..."
echo "========================================="

# Show environment info
echo "🔍 Environment Info:"
echo "  - RENDER: ${RENDER:-not set}"
echo "  - FETCH_ALL_DATA: ${FETCH_ALL_DATA:-not set}"
echo "  - FOOTBALL_DATA_API_KEY: ${FOOTBALL_DATA_API_KEY:0:10}..."
echo "  - PORT: ${PORT:-not set}"
echo "========================================="

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
echo "🔧 Initializing database..."
python -c "from db import init_db; init_db()"

# Check database path
echo "🔍 Checking database path..."
python -c "from db import DB_PATH; print(f'Database path: {DB_PATH}')"

# Create admin user first (critical for deployment)
echo "👨‍💼 Creating admin user..."
python create_admin.py

# Populate database with football data
echo "📊 Populating database with football data..."
python populate_db.py

# Verify data was populated
echo "🔍 Verifying database population..."
python verify_data.py

echo "========================================="
echo "✅ Build completed successfully!"
echo "========================================="

