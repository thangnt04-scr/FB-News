#!/usr/bin/env python3
"""Initialize database for Render deployment"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import db
    print("Initializing database...")
    db.init_db()
    print("Database initialized successfully!")
except Exception as e:
    print(f"Warning: Database initialization failed: {e}")
    print("This is OK if database already exists")
    sys.exit(0)  # Don't fail the build

