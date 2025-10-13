# syntax=docker/dockerfile:1.7
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy app
COPY . /app

# Non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Runtime env
ENV FLASK_SECRET_KEY=change-me-in-prod \
    FOOTBALL_DB=/app/data/footballinfor.db \
    PYTHONPATH=/app \
    GUNICORN_WORKERS=1

# Create data dir
RUN mkdir -p /app/data

# Expose port
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import requests; import sys;\n\nimport os;\nurl='http://localhost:5000';\n\nimport urllib.request as u;\n\ntry:\n    u.urlopen(url, timeout=3)\n    sys.exit(0)\nexcept Exception:\n    sys.exit(1)" || exit 1

# Entrypoint initializes DB and creates admin if needed, then runs app via Gunicorn
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
CMD ["sh", "-lc", "exec gunicorn -w ${GUNICORN_WORKERS:-1} -b 0.0.0.0:${PORT:-5000} app:app"]
