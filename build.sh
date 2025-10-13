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

# Populate database with football data
echo "📊 Populating database with football data..."
python populate_db.py

# Verify data was populated
echo "🔍 Verifying database population..."
python -c "import sqlite3; from db import DB_PATH; conn = sqlite3.connect(DB_PATH); cur = conn.cursor(); cur.execute('SELECT COUNT(*) FROM leagues'); leagues = cur.fetchone()[0]; cur.execute('SELECT COUNT(*) FROM teams'); teams = cur.fetchone()[0]; cur.execute('SELECT COUNT(*) FROM players'); players = cur.fetchone()[0]; cur.execute('SELECT COUNT(*) FROM matches'); matches = cur.fetchone()[0]; cur.execute('SELECT COUNT(*) FROM users'); users = cur.fetchone()[0]; print(f'  - Leagues: {leagues}'); print(f'  - Teams: {teams}'); print(f'  - Players: {players}'); print(f'  - Matches: {matches}'); print(f'  - Users: {users}'); conn.close()"

echo "========================================="
echo "✅ Build completed successfully!"
echo "========================================="

