#!/usr/bin/env python3
"""
Populate database with football data from football-data.org API
"""
import os
import sys
import requests
import time
from datetime import datetime
from db import (
    get_db_connection,
    init_db,
    upsert_league,
    upsert_team,
    upsert_player,
    upsert_match
)

# API Configuration
API_KEY = os.getenv('FOOTBALL_DATA_API_KEY', '714b8b0227af4ae7bec7cd46e191cf3a')
BASE_URL = 'https://api.football-data.org/v4'
HEADERS = {'X-Auth-Token': API_KEY}

# Rate limiting: Free tier allows 10 requests per minute
REQUEST_DELAY = 6  # seconds between requests

# Configuration: Fetch ALL data or limited data
# For Render deployment, use limited data to avoid build timeout (15 min limit)
# For local development, set to True to fetch all data
FETCH_ALL_DATA = os.getenv('FETCH_ALL_DATA', 'False') == 'True'

def make_api_request(endpoint):
    """Make API request with rate limiting and error handling"""
    url = f"{BASE_URL}/{endpoint}"
    print(f"  Fetching: {endpoint}")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            time.sleep(REQUEST_DELAY)  # Rate limiting
            return response.json()
        elif response.status_code == 429:
            print(f"  ⚠️  Rate limit exceeded. Waiting 60 seconds...")
            time.sleep(60)
            return make_api_request(endpoint)
        else:
            print(f"  ❌ Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")
        return None

def populate_leagues():
    """Populate leagues table"""
    print("\n📊 Populating Leagues...")

    # Popular league codes and their IDs
    leagues_data = [
        ('PL', 2021),   # Premier League
        ('PD', 2014),   # La Liga
        ('BL1', 2002),  # Bundesliga
        ('SA', 2019),   # Serie A
        ('FL1', 2015),  # Ligue 1
        ('CL', 2001),   # Champions League
    ]

    count = 0
    for code, league_id in leagues_data:
        data = make_api_request(f'competitions/{code}')
        if data:
            try:
                upsert_league(
                    external_id=data.get('id', league_id),
                    name=data.get('name'),
                    country_code=data.get('area', {}).get('code', code)
                )
                count += 1
                print(f"  ✅ Added: {data.get('name')}")
            except Exception as e:
                print(f"  ❌ Error inserting league: {str(e)}")

    print(f"✅ Leagues populated: {count}")
    return count

def populate_teams():
    """Populate teams table from ALL leagues"""
    print("\n⚽ Populating Teams...")

    # Get teams from all major leagues
    league_codes = ['PL', 'PD', 'BL1', 'SA', 'FL1', 'CL']
    league_ids = {
        'PL': 2021,   # Premier League
        'PD': 2014,   # La Liga
        'BL1': 2002,  # Bundesliga
        'SA': 2019,   # Serie A
        'FL1': 2015,  # Ligue 1
        'CL': 2001,   # Champions League
    }

    count = 0
    for code in league_codes:
        print(f"\n  📊 Fetching teams from {code}...")
        data = make_api_request(f'competitions/{code}/teams')

        if not data or 'teams' not in data:
            print(f"  ❌ Failed to fetch teams from {code}")
            continue

        # Limit teams per league if not fetching all
        teams_to_process = data['teams'] if FETCH_ALL_DATA else data['teams'][:10]

        for team in teams_to_process:
            try:
                upsert_team(
                    external_id=team.get('id'),
                    league_external_id=league_ids.get(code),
                    name=team.get('name'),
                    short_name=team.get('shortName', team.get('name')),
                    founded=team.get('founded'),
                    stadium=team.get('venue')
                )
                count += 1
                print(f"  ✅ Added: {team.get('name')} ({code})")
            except Exception as e:
                print(f"  ❌ Error inserting team: {str(e)}")

    print(f"\n✅ Teams populated: {count}")
    return count

def populate_players():
    """Populate players table from ALL teams"""
    print("\n👤 Populating Players...")

    # Get all teams from database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT external_id, name FROM teams ORDER BY id")
    teams = cur.fetchall()
    conn.close()

    if not teams:
        print("  ⚠️  No teams found in database. Run populate_teams() first.")
        return 0

    count = 0
    total_teams = len(teams)

    for idx, team in enumerate(teams, 1):
        team_id = team['external_id']
        team_name = team['name']

        print(f"\n  [{idx}/{total_teams}] Fetching players from {team_name}...")
        data = make_api_request(f'teams/{team_id}')

        if not data or 'squad' not in data:
            print(f"  ⚠️  No squad data for {team_name}")
            continue

        # Fetch ALL players if FETCH_ALL_DATA is True
        players_to_process = data['squad'] if FETCH_ALL_DATA else data['squad'][:5]

        for player in players_to_process:
            try:
                upsert_player(
                    external_id=player.get('id'),
                    team_external_id=team_id,
                    name=player.get('name'),
                    nationality=player.get('nationality'),
                    position=player.get('position'),
                    shirt_number=player.get('shirtNumber'),
                    birthdate=player.get('dateOfBirth')
                )
                count += 1
                print(f"    ✅ {player.get('name')} ({player.get('position', 'N/A')})")
            except Exception as e:
                print(f"    ❌ Error: {str(e)}")

    print(f"\n✅ Players populated: {count}")
    return count

def populate_matches():
    """Populate matches table from ALL leagues"""
    print("\n🏆 Populating Matches...")

    # Get matches from all major leagues
    league_codes = ['PL', 'PD', 'BL1', 'SA', 'FL1', 'CL']
    league_ids = {
        'PL': 2021,   # Premier League
        'PD': 2014,   # La Liga
        'BL1': 2002,  # Bundesliga
        'SA': 2019,   # Serie A
        'FL1': 2015,  # Ligue 1
        'CL': 2001,   # Champions League
    }

    count = 0
    for code in league_codes:
        print(f"\n  📊 Fetching matches from {code}...")

        # Fetch finished matches
        data = make_api_request(f'competitions/{code}/matches?status=FINISHED')

        if not data or 'matches' not in data:
            print(f"  ❌ Failed to fetch matches from {code}")
            continue

        # Limit matches per league if not fetching all
        matches_to_process = data['matches'] if FETCH_ALL_DATA else data['matches'][:20]

        for match in matches_to_process:
            try:
                # Parse date
                match_date = match.get('utcDate', '')
                if match_date:
                    match_date = datetime.fromisoformat(match_date.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')

                # Get season info
                season = match.get('season', {})
                season_str = f"{season.get('startDate', '')[:4]}/{season.get('endDate', '')[:4]}" if season else "2024/2025"

                upsert_match(
                    external_id=match.get('id'),
                    league_external_id=league_ids.get(code),
                    season=season_str,
                    match_date=match_date,
                    home_team_ext_id=match.get('homeTeam', {}).get('id'),
                    away_team_ext_id=match.get('awayTeam', {}).get('id'),
                    home_score=match.get('score', {}).get('fullTime', {}).get('home'),
                    away_score=match.get('score', {}).get('fullTime', {}).get('away')
                )
                count += 1
                home_name = match.get('homeTeam', {}).get('name', 'Unknown')
                away_name = match.get('awayTeam', {}).get('name', 'Unknown')
                score = f"{match.get('score', {}).get('fullTime', {}).get('home', 0)}-{match.get('score', {}).get('fullTime', {}).get('away', 0)}"
                print(f"  ✅ {home_name} vs {away_name} ({score})")
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")

        print(f"  → {code}: {len(matches_to_process)} matches processed")

    print(f"\n✅ Matches populated: {count}")
    return count

def create_admin_user():
    """Create default admin user"""
    print("\n👨‍💼 Creating Admin User...")

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Check if admin already exists
        cur.execute("SELECT id FROM users WHERE username = 'admin'")
        existing_admin = cur.fetchone()
        
        if existing_admin:
            print("  ✅ Admin user already exists")
            return True

        # Use werkzeug password hashing (same as app.py)
        from werkzeug.security import generate_password_hash
        password_hash = generate_password_hash('admin123')

        cur.execute('''
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        ''', (
            'admin',
            'admin@football.com',
            password_hash,
            'admin'
        ))
        conn.commit()
        print("  ✅ Admin user created (username: admin, password: admin123)")
        return True
    except Exception as e:
        print(f"  ❌ Error creating admin user: {str(e)}")
        return False
    finally:
        conn.close()

def main():
    """Main function to populate all data"""
    print("=" * 70)
    print("🚀 POPULATING FOOTBALL DATABASE - FULL DATA MODE")
    print("=" * 70)
    print(f"API Key: {API_KEY[:10]}...")
    print(f"Base URL: {BASE_URL}")
    print(f"Fetch All Data: {FETCH_ALL_DATA}")
    print(f"Rate Limit: {REQUEST_DELAY}s delay between requests")
    print("=" * 70)

    if FETCH_ALL_DATA:
        print("\n⚠️  WARNING: Fetching ALL data will take significant time!")
        print("   - All teams from 6 leagues")
        print("   - All players from all teams")
        print("   - All finished matches from all leagues")
        print("   - Estimated time: 30-60 minutes (due to rate limiting)")
        print("\n   Press Ctrl+C to cancel, or wait 5 seconds to continue...")
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user")
            return

    start_time = time.time()

    # Initialize database
    print("\n🔧 Initializing database...")
    init_db()

    # Create admin user FIRST (critical for deployment)
    print("\n" + "=" * 70)
    print("CREATING ADMIN USER (PRIORITY)")
    print("=" * 70)
    admin_created = create_admin_user()
    if not admin_created:
        print("❌ CRITICAL: Failed to create admin user!")
        return

    # Populate data
    print("\n" + "=" * 70)
    print("STARTING DATA POPULATION")
    print("=" * 70)

    total = 0
    leagues_count = populate_leagues()
    total += leagues_count

    teams_count = populate_teams()
    total += teams_count

    players_count = populate_players()
    total += players_count

    matches_count = populate_matches()
    total += matches_count

    elapsed_time = time.time() - start_time

    print("\n" + "=" * 70)
    print(f"✅ DATABASE POPULATION COMPLETE!")
    print("=" * 70)
    print(f"📊 Total records inserted: {total}")
    print(f"⏱️  Time elapsed: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
    print("=" * 70)

    # Verify data
    print("\n📋 FINAL VERIFICATION:")
    print("-" * 70)
    conn = get_db_connection()
    cur = conn.cursor()

    tables = ['leagues', 'teams', 'players', 'matches', 'users']
    for table in tables:
        cur.execute(f'SELECT COUNT(*) FROM {table}')
        count = cur.fetchone()[0]
        print(f"  {table.upper():15} : {count:6} records")

    conn.close()
    print("-" * 70)
    print("\n✅ Done!")

if __name__ == '__main__':
    main()

