# db.py
import os
import sqlite3
from pathlib import Path

# Use /tmp for database on Render (ephemeral but writable)
# In production, should use PostgreSQL instead of SQLite
if os.environ.get('RENDER'):
    DB_PATH = '/tmp/footballinfor.db'
else:
    DB_PATH = os.environ.get("FOOTBALL_DB", str(Path(__file__).with_name("footballinfor.db")))

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    # foreign keys ON
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    print(f"Initializing database at: {DB_PATH}")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS leagues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        country_code TEXT,
        external_id INTEGER UNIQUE
    );
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        league_id INTEGER,
        name TEXT NOT NULL,
        short_name TEXT,
        founded_year INTEGER,
        stadium TEXT,
        external_id INTEGER UNIQUE,
        FOREIGN KEY (league_id) REFERENCES leagues(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_id INTEGER,
        name TEXT NOT NULL,
        nationality TEXT,
        position TEXT,
        shirt_number INTEGER,
        birthdate TEXT,
        height_cm INTEGER,
        weight_kg INTEGER,
        external_id INTEGER UNIQUE,
        FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        league_id INTEGER,
        season TEXT,
        match_date TEXT,
        home_team_id INTEGER,
        away_team_id INTEGER,
        home_score INTEGER,
        away_score INTEGER,
        external_id INTEGER UNIQUE,
        FOREIGN KEY (league_id) REFERENCES leagues(id) ON DELETE CASCADE,
        FOREIGN KEY (home_team_id) REFERENCES teams(id) ON DELETE CASCADE,
        FOREIGN KEY (away_team_id) REFERENCES teams(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()
    print(f"Database initialized successfully at: {DB_PATH}")
    print("Tables created: leagues, teams, players, matches, users")

# Upsert helpers (simple patterns)
def upsert_league(external_id, name, country_code):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO leagues(external_id, name, country_code) VALUES(?,?,?)",
                (external_id, name, country_code))
    # update if name changed
    cur.execute("UPDATE leagues SET name=?, country_code=? WHERE external_id=?",
                (name, country_code, external_id))
    conn.commit()
    conn.close()

def upsert_team(external_id, league_external_id, name, short_name=None, founded=None, stadium=None):
    conn = get_db_connection()
    cur = conn.cursor()
    # find local league id
    cur.execute("SELECT id FROM leagues WHERE external_id=?", (league_external_id,))
    row = cur.fetchone()
    league_id = row["id"] if row else None
    cur.execute("""INSERT OR IGNORE INTO teams(external_id, league_id, name, short_name, founded_year, stadium)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (external_id, league_id, name, short_name, founded, stadium))
    cur.execute("""UPDATE teams SET league_id=?, name=?, short_name=?, founded_year=?, stadium=?
                   WHERE external_id=?""",
                (league_id, name, short_name, founded, stadium, external_id))
    conn.commit()
    conn.close()

def upsert_player(external_id, team_external_id, name, nationality=None, position=None, shirt_number=None, birthdate=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM teams WHERE external_id=?", (team_external_id,))
    t = cur.fetchone()
    team_id = t["id"] if t else None
    cur.execute("""INSERT OR IGNORE INTO players(external_id, team_id, name, nationality, position, shirt_number, birthdate)
                   VALUES(?, ?, ?, ?, ?, ?, ?)""",
                (external_id, team_id, name, nationality, position, shirt_number, birthdate))
    cur.execute("""UPDATE players SET team_id=?, name=?, nationality=?, position=?, shirt_number=?, birthdate=?
                   WHERE external_id=?""",
                (team_id, name, nationality, position, shirt_number, birthdate, external_id))
    conn.commit()
    conn.close()

def upsert_match(external_id, league_external_id, season, match_date,
                 home_team_ext_id, away_team_ext_id, home_score, away_score):
    conn = get_db_connection()
    cur = conn.cursor()
    # resolve local ids
    cur.execute("SELECT id FROM leagues WHERE external_id=?", (league_external_id,))
    lr = cur.fetchone()
    league_id = lr["id"] if lr else None
    cur.execute("SELECT id FROM teams WHERE external_id=?", (home_team_ext_id,))
    hr = cur.fetchone()
    home_id = hr["id"] if hr else None
    cur.execute("SELECT id FROM teams WHERE external_id=?", (away_team_ext_id,))
    ar = cur.fetchone()
    away_id = ar["id"] if ar else None
    cur.execute("""INSERT OR IGNORE INTO matches(external_id, league_id, season, match_date, home_team_id, away_team_id, home_score, away_score)
                   VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                (external_id, league_id, season, match_date, home_id, away_id, home_score, away_score))
    cur.execute("""UPDATE matches SET league_id=?, season=?, match_date=?, home_team_id=?, away_team_id=?, home_score=?, away_score=?
                   WHERE external_id=?""",
                (league_id, season, match_date, home_id, away_id, home_score, away_score, external_id))
    conn.commit()
    conn.close()

# User management functions
def create_user(username, email, password_hash, role='user'):
    """Tạo user mới"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users(username, email, password_hash, role) VALUES(?,?,?,?)",
                   (username, email, password_hash, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_by_username(username):
    """Lấy user theo username"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_id(user_id):
    """Lấy user theo ID"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cur.fetchone()
    conn.close()
    return dict(user) if user else None

def get_all_users():
    """Lấy tất cả users (cho admin)"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email, role, created_at FROM users ORDER BY created_at DESC")
    users = [dict(row) for row in cur.fetchall()]
    conn.close()
    return users

def update_user_role(user_id, new_role):
    """Cập nhật role của user"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET role=? WHERE id=?", (new_role, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    """Xóa user"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
