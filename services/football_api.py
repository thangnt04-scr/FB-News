import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Read API key from environment instead of hard-coding
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

BASE = "https://api.football-data.org/v4"
# Only construct headers if the key is available. We will validate in _get.
HEADERS = {"X-Auth-Token": API_KEY} if API_KEY else None

# Delay để tránh bị 429
API_DELAY = 6  # giây

def _get(url, params=None):
    """HTTP GET helper with basic rate limiting and key validation.

    Requires the environment variable FOOTBALL_DATA_API_KEY to be set
    (or provided via a .env file). This avoids committing secrets.
    """
    if not HEADERS or not API_KEY:
        raise RuntimeError(
            "Missing FOOTBALL_DATA_API_KEY. Set it in your environment or .env file."
        )
    time.sleep(API_DELAY)
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()

def fetch_competitions():
    """Lấy danh sách giải đấu"""
    return _get(f"{BASE}/competitions")

def fetch_teams_for_competition(comp_id, season=2023):
    """Lấy danh sách đội trong 1 giải"""
    return _get(f"{BASE}/competitions/{comp_id}/teams", {"season": season})

def fetch_team(team_id):
    """Lấy chi tiết 1 đội (bao gồm cầu thủ/squad)"""
    return _get(f"{BASE}/teams/{team_id}")

def fetch_matches_for_competition(comp_id, season=2023):
    """Lấy danh sách trận đấu của 1 giải"""
    return _get(f"{BASE}/competitions/{comp_id}/matches", {"season": season})
