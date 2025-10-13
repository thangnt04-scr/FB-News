#!/usr/bin/env bash
set -euo pipefail

# Load env if present
if [ -f /app/.env ]; then
  set -a
  source /app/.env
  set +a
fi

# Ensure DB exists and migrate schema
python - <<'PY'
import db
try:
    db.init_db()
    print("DB initialized")
except Exception as e:
    print("DB init error:", e)
PY

# Optionally create default users
if [ "${CREATE_DEFAULT_USERS:-1}" = "1" ]; then
  python /app/create_admin.py || true
fi

# Run the app
if [ "${FLASK_DEBUG:-false}" = "true" ]; then
  exec python /app/app.py
else
  exec gunicorn --workers ${WEB_CONCURRENCY:-2} --bind 0.0.0.0:${PORT:-5000} app:app --timeout 120
fi
