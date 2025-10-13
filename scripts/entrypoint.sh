#!/usr/bin/env bash
set -euo pipefail

# Initialize database if missing
python - <<'PY'
import os
import db

# Ensure DB path directory exists
from pathlib import Path
path = Path(os.environ.get('FOOTBALL_DB', 'footballinfor.db'))
path.parent.mkdir(parents=True, exist_ok=True)

print("Initializing database schema (idempotent)...")
db.init_db()
PY

# Create default admin if desired
if [[ "${CREATE_DEFAULT_USERS:-1}" == "1" ]]; then
  echo "Creating default users if absent..."
  python create_admin.py || true
fi

exec "$@"
