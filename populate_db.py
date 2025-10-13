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
    """Populate teams table"""
    print("\n⚽ Populating Teams...")

    # Get teams from Premier League (PL)
    data = make_api_request('competitions/PL/teams')

    if not data or 'teams' not in data:
        print("  ❌ Failed to fetch teams")
        return 0

    count = 0
    for team in data['teams'][:20]:  # Limit to 20 teams
        try:
            upsert_team(
                external_id=team.get('id'),
                league_external_id=2021,  # Premier League external ID
                name=team.get('name'),
                short_name=team.get('shortName', team.get('name')),
                founded=team.get('founded'),
                stadium=team.get('venue')
            )
            count += 1
            print(f"  ✅ Added: {team.get('name')}")
        except Exception as e:
            print(f"  ❌ Error inserting team: {str(e)}")

    print(f"✅ Teams populated: {count}")
    return count

def populate_players():
    """Populate players table"""
    print("\n👤 Populating Players...")

    # Get a few teams and their players
    team_ids = [57, 61, 65, 66, 73]  # Arsenal, Chelsea, Man City, Man Utd, Tottenham

    count = 0
    for team_id in team_ids:
        data = make_api_request(f'teams/{team_id}')

        if not data or 'squad' not in data:
            continue

        for player in data['squad'][:5]:  # Limit to 5 players per team
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
                print(f"  ✅ Added: {player.get('name')} ({player.get('position')})")
            except Exception as e:
                print(f"  ❌ Error inserting player: {str(e)}")

    print(f"✅ Players populated: {count}")
    return count

def populate_matches():
    """Populate matches table"""
    print("\n🏆 Populating Matches...")

    # Get recent Premier League matches
    data = make_api_request('competitions/PL/matches?status=FINISHED')

    if not data or 'matches' not in data:
        print("  ❌ Failed to fetch matches")
        return 0

    count = 0
    for match in data['matches'][:20]:  # Limit to 20 matches
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
                league_external_id=2021,  # Premier League
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
            print(f"  ✅ Added: {home_name} vs {away_name} ({score})")
        except Exception as e:
            print(f"  ❌ Error inserting match: {str(e)}")

    print(f"✅ Matches populated: {count}")
    return count

def create_admin_user():
    """Create default admin user"""
    print("\n👨‍💼 Creating Admin User...")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Simple password hash (in production, use proper hashing like bcrypt)
        import hashlib
        password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        
        cur.execute('''
            INSERT OR REPLACE INTO users (id, username, email, password_hash, role)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            1,
            'admin',
            'admin@football.com',
            password_hash,
            'admin'
        ))
        conn.commit()
        print("  ✅ Admin user created (username: admin, password: admin123)")
    except Exception as e:
        print(f"  ❌ Error creating admin user: {str(e)}")
    finally:
        conn.close()

def main():
    """Main function to populate all data"""
    print("=" * 60)
    print("🚀 POPULATING FOOTBALL DATABASE")
    print("=" * 60)
    print(f"API Key: {API_KEY[:10]}...")
    print(f"Base URL: {BASE_URL}")
    print("=" * 60)
    
    # Initialize database
    print("\n🔧 Initializing database...")
    init_db()
    
    # Populate data
    total = 0
    total += populate_leagues()
    total += populate_teams()
    total += populate_players()
    total += populate_matches()
    create_admin_user()
    
    print("\n" + "=" * 60)
    print(f"✅ DATABASE POPULATION COMPLETE!")
    print(f"📊 Total records inserted: {total}")
    print("=" * 60)
    
    # Verify data
    print("\n📋 Verifying data...")
    conn = get_db_connection()
    cur = conn.cursor()
    
    tables = ['leagues', 'teams', 'players', 'matches', 'users']
    for table in tables:
        cur.execute(f'SELECT COUNT(*) FROM {table}')
        count = cur.fetchone()[0]
        print(f"  {table}: {count} records")
    
    conn.close()
    print("\n✅ Done!")

if __name__ == '__main__':
    main()

